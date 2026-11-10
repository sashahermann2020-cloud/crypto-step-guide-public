#!/usr/bin/env python3
"""Validate indexability and SEO metadata in the generated static site."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE_URL = "https://crypto-step-guide.com"
HOST = urlsplit(SITE_URL).netloc
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ERRORS = []
LANG_PREFIXES = {"es", "pt", "en"}
CYRILLIC = re.compile("[\u0400-\u04FF]")
RU_LINK = re.compile(r'<a\b[^>]*\blang="ru"[^>]*>.*?</a>', re.S)
NON_VISIBLE = re.compile(r"<(script|style)\b.*?</\1>", re.S)


def expected_lang(slug):
    """Language variants live under /es/, /pt/ and /en/; everything else is Russian."""
    first = slug.split("/")[0]
    return first if first in LANG_PREFIXES else "ru"


def check(condition, message):
    if not condition:
        ERRORS.append(message)


class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title_parts = []
        self.in_title = False
        self.h1_count = 0
        self.descriptions = []
        self.robots = []
        self.canonicals = []
        self.alternates = []
        self.og_urls = []
        self.og_images = []
        self.jsonld_raw = []
        self._jsonld_buffer = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            name = (attrs.get("name") or "").lower()
            prop = (attrs.get("property") or "").lower()
            content = attrs.get("content") or ""
            if name == "description":
                self.descriptions.append(content)
            elif name == "robots":
                self.robots.append(content.lower())
            elif prop == "og:url":
                self.og_urls.append(content)
            elif prop == "og:image":
                self.og_images.append(content)
        elif tag == "link":
            rel = set((attrs.get("rel") or "").lower().split())
            href = attrs.get("href") or ""
            if "canonical" in rel:
                self.canonicals.append(href)
            if "alternate" in rel and attrs.get("hreflang"):
                self.alternates.append((attrs["hreflang"].lower(), href))
        elif tag == "script" and (attrs.get("type") or "").lower() == "application/ld+json":
            self._jsonld_buffer = []

        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self._jsonld_buffer is not None:
            self.jsonld_raw.append("".join(self._jsonld_buffer))
            self._jsonld_buffer = None

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self._jsonld_buffer is not None:
            self._jsonld_buffer.append(data)

    @property
    def title(self):
        return " ".join(" ".join(self.title_parts).split())


def page_path(slug):
    return DIST / (Path(slug) / "index.html") if slug else DIST / "index.html"


def schema_types(data):
    types = set()

    def visit(value):
        if isinstance(value, dict):
            item_type = value.get("@type")
            if isinstance(item_type, str):
                types.add(item_type)
            elif isinstance(item_type, list):
                types.update(item_type)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(data)
    return types


def schema_objects(data):
    objects = []

    def visit(value):
        if isinstance(value, dict):
            if "@type" in value:
                objects.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(data)
    return objects


def main():
    seo_path = ROOT / "content" / "seo.json"
    seo_model = json.loads(seo_path.read_text(encoding="utf-8"))
    expected_slugs = {""} | set(seo_model["pages"])

    sitemap_path = DIST / "sitemap.xml"
    check(sitemap_path.is_file(), "dist/sitemap.xml is missing")
    if not sitemap_path.is_file():
        return fail()

    try:
        sitemap = ET.parse(sitemap_path).getroot()
    except ET.ParseError as exc:
        ERRORS.append(f"dist/sitemap.xml is invalid XML: {exc}")
        return fail()

    check(sitemap.tag == SITEMAP_NS + "urlset", "sitemap root is not a standard urlset")
    entries = sitemap.findall(SITEMAP_NS + "url")
    urls = [entry.findtext(SITEMAP_NS + "loc", default="").strip() for entry in entries]
    check(bool(urls), "sitemap contains no URLs")
    check(len(urls) == len(set(urls)), "sitemap contains duplicate URLs")

    sitemap_slugs = set()
    title_to_url = {}
    for url in urls:
        parsed_url = urlsplit(url)
        check(parsed_url.scheme == "https" and parsed_url.netloc == HOST,
              f"sitemap URL is outside the canonical HTTPS host: {url}")
        check(not parsed_url.query and not parsed_url.fragment,
              f"sitemap URL contains a query or fragment: {url}")
        slug = unquote(parsed_url.path).strip("/")
        sitemap_slugs.add(slug)
        html_path = page_path(slug)
        check(html_path.is_file(), f"sitemap URL has no generated HTML page: {url}")
        if not html_path.is_file():
            continue

        parser = SEOParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        lang = expected_lang(slug)
        check(parser.lang == lang, f"{url}: html lang is {parser.lang!r}, expected {lang!r}")
        if lang != "ru":
            visible = RU_LINK.sub("", NON_VISIBLE.sub("", html_path.read_text(encoding="utf-8")))
            check(not CYRILLIC.search(visible),
                  f"{url}: language variant contains Cyrillic text outside the link to the Russian version")
            check(any(a == lang and urljoin(SITE_URL + "/", h) == url for a, h in parser.alternates),
                  f"{url}: missing self-referencing hreflang={lang}")
        check(bool(parser.title), f"{url}: title is missing")
        check(parser.title not in title_to_url,
              f"{url}: title duplicates {title_to_url.get(parser.title, '')}")
        title_to_url[parser.title] = url
        check(len(parser.descriptions) == 1 and bool(parser.descriptions[0].strip()),
              f"{url}: expected one non-empty meta description")
        check(parser.h1_count == 1, f"{url}: expected exactly one H1")
        check(len(parser.canonicals) == 1, f"{url}: expected exactly one canonical")
        if len(parser.canonicals) == 1:
            canonical = urljoin(SITE_URL + "/", parser.canonicals[0])
            check(canonical == url, f"{url}: canonical points to {canonical}")
        check(len(parser.og_urls) == 1 and parser.og_urls[0] == url,
              f"{url}: og:url does not match the canonical URL")
        check(len(parser.og_images) == 1, f"{url}: expected one og:image")
        for og_image in parser.og_images:
            og_target = urlsplit(og_image)
            check(og_target.netloc == HOST and og_target.path.endswith(".png")
                  and (DIST / og_target.path.lstrip("/")).is_file(),
                  f"{url}: og:image is missing or not a local PNG: {og_image}")
        check(bool(parser.robots) and all("noindex" not in value for value in parser.robots),
              f"{url}: page is missing indexable robots metadata")

        for language, alternate in parser.alternates:
            if language == "ru":
                check(urljoin(SITE_URL + "/", alternate) == url,
                      f"{url}: Russian hreflang does not point to this page")

        types = set()
        entities = []
        for raw in parser.jsonld_raw:
            try:
                parsed = json.loads(raw)
                types.update(schema_types(parsed))
                entities.extend(schema_objects(parsed))
            except json.JSONDecodeError as exc:
                ERRORS.append(f"{url}: invalid JSON-LD: {exc}")
        check("WebPage" in types or "AboutPage" in types or "Article" in types,
              f"{url}: JSON-LD is missing a page entity")
        if slug:
            check("BreadcrumbList" in types, f"{url}: JSON-LD is missing BreadcrumbList")
        organizations = [node for node in entities if node.get("@type") == "Organization"]
        free_types = {"WebSite", "WebPage", "AboutPage", "Article"}
        pages_ld = [node for node in entities
                    if free_types & set(node["@type"] if isinstance(node["@type"], list) else [node["@type"]])]
        check(any(node.get("@type") == "WebSite" for node in pages_ld) and any(node.get("@type") != "WebSite" for node in pages_ld),
              f"{url}: JSON-LD must contain WebSite and a page entity")
        check(all(node.get("isAccessibleForFree") is True for node in pages_ld),
              f"{url}: WebSite, WebPage and Article JSON-LD must declare isAccessibleForFree=true (the site is free)")
        check(all(node.get("description") for node in organizations), f"{url}: Organization schema is missing description")
        check(any(node.get("logo") for node in organizations),
              f"{url}: Organization schema is missing logo")
        check((DIST / "assets" / "csg-logo.svg").is_file(),
              f"{url}: Organization logo asset is missing")
        if slug.startswith("articles/"):
            check("Article" in types, f"{url}: article page is missing Article schema")
            articles = [node for node in entities if node.get("@type") == "Article"]
            images = [img for node in articles for img in node.get("image", [])]
            check(bool(images), f"{url}: Article schema is missing image")
            for img in images:
                check((DIST / urlsplit(img).path.lstrip("/")).is_file(),
                      f"{url}: Article image asset is missing: {img}")

        for href in parser.links:
            target = urlsplit(urljoin(url, href))
            if target.scheme not in {"http", "https"} or target.netloc != HOST:
                continue
            target_slug = unquote(target.path).strip("/")
            if target.path.endswith("/") or not target.path:
                local_path = page_path(target_slug)
            else:
                local_path = DIST / target_slug
            check(local_path.is_file(), f"{url}: broken internal link {href}")

    check(sitemap_slugs == expected_slugs,
          "sitemap route set differs from content/seo.json: "
          f"missing={sorted(expected_slugs - sitemap_slugs)}, "
          f"extra={sorted(sitemap_slugs - expected_slugs)}")

    not_found = DIST / "404.html"
    check(not_found.is_file(), "dist/404.html is missing (unknown paths would return the home page with 200)")
    if not_found.is_file():
        parser = SEOParser()
        parser.feed(not_found.read_text(encoding="utf-8"))
        check(not parser.canonicals, "404.html must not declare a canonical URL")
        check(any("noindex" in value for value in parser.robots), "404.html must be noindex")

    robots_path = DIST / "robots.txt"
    check(robots_path.is_file(), "dist/robots.txt is missing")
    if robots_path.is_file():
        robots = robots_path.read_text(encoding="utf-8")
        lowered = robots.lower()
        check("user-agent: *" in lowered and "allow: /" in lowered,
              "robots.txt must allow general crawler access")
        check(f"sitemap: {SITE_URL}/sitemap.xml".lower() in lowered,
              "robots.txt must point to the canonical sitemap")

    key_path = ROOT / ".indexnow-key"
    check(key_path.is_file(), ".indexnow-key is missing")
    if key_path.is_file():
        key = key_path.read_text(encoding="utf-8").strip()
        hosted_key = DIST / f"{key}.txt"
        check(bool(key), ".indexnow-key is empty")
        check(hosted_key.is_file(), "IndexNow verification file is missing from dist")
        if hosted_key.is_file():
            check(hosted_key.read_text(encoding="utf-8").strip() == key,
                  "IndexNow verification file does not match .indexnow-key")

    if len(urls) != len(expected_slugs):
        ERRORS.append(f"expected {len(expected_slugs)} public routes, found {len(urls)}")
    if ERRORS:
        return fail()
    print(f"SEO output valid: {len(urls)} canonical, indexable pages; sitemap, robots, JSON-LD, internal links, and IndexNow key pass.")


def fail():
    for error in ERRORS:
        print(f"ERROR: {error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

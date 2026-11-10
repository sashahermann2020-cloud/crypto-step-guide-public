#!/usr/bin/env python3
"""Submit already-published Crypto Step Guide URLs through the IndexNow protocol."""
import argparse
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE_URL = "https://crypto-step-guide.com"
HOST = "crypto-step-guide.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def read_sitemap_urls():
    path = DIST / "sitemap.xml"
    root = ET.parse(path).getroot()
    urls = [node.text.strip() for node in root.findall(f".//{SITEMAP_NS}loc")
            if node.text and node.text.strip()]
    if not urls:
        raise ValueError("dist/sitemap.xml contains no URLs")
    for url in urls:
        if not url.startswith(SITE_URL + "/") and url != SITE_URL + "/":
            raise ValueError(f"Refusing URL outside {SITE_URL}: {url}")
    return urls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all-sitemap", action="store_true",
                       help="submit every canonical URL in the current sitemap")
    group.add_argument("--url", action="append",
                       help="submit one published canonical URL; repeat for several URLs")
    args = parser.parse_args()

    try:
        sitemap_urls = read_sitemap_urls()
        urls = sitemap_urls if args.all_sitemap else list(dict.fromkeys(args.url or []))
        invalid = [url for url in urls if url not in sitemap_urls]
        if invalid:
            raise ValueError("URLs must be present in the current sitemap: " + ", ".join(invalid))

        key_path = ROOT / ".indexnow-key"
        key = key_path.read_text(encoding="utf-8").strip()
        hosted_key = DIST / f"{key}.txt"
        if not key or not hosted_key.is_file():
            raise ValueError("IndexNow key or generated key file is missing")
        if hosted_key.read_text(encoding="utf-8").strip() != key:
            raise ValueError("Generated IndexNow key file does not match .indexnow-key")

        payload = {
            "host": HOST,
            "key": key,
            "keyLocation": f"{SITE_URL}/{key}.txt",
            "urlList": urls,
        }
        request = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                status = response.status
                detail = response.read().decode("utf-8", errors="replace").strip()
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace").strip()
            print(f"IndexNow rejected the request: HTTP {error.code} {detail}", file=sys.stderr)
            return 1

        if status not in {200, 202}:
            print(f"IndexNow returned HTTP {status}: {detail}", file=sys.stderr)
            return 1
        print(f"IndexNow accepted {len(urls)} URL(s) (HTTP {status}).")
        print("Acceptance requests crawling; it does not confirm indexing or search position.")
        if detail:
            print(detail)
        return 0
    except (OSError, ValueError, ET.ParseError) as error:
        print(f"IndexNow submission failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

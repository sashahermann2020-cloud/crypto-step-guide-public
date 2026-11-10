#!/usr/bin/env python3
"""Build Open Graph preview images (assets/og/*.png) for every public page.

Run locally when a page title changes or a page is added:

    python3 scripts/build_og_images.py

The generated PNG files are committed, so the Cloudflare Pages build
(`python3 generate.py`) stays dependency-free.

Local requirements: Pillow, fontTools with brotli (to read woff2 fonts) and
`rsvg-convert` (to rasterise SVG article covers). The project's fonts in
/fonts/ contain only Cyrillic glyphs, so Latin glyphs (USDT, Bitcoin, HUMO…)
come from the Latin subsets of the same families. Get them once with

    npm pack @fontsource-variable/literata @fontsource-variable/commissioner

unpack both archives into one folder and pass it as OG_LATIN_FONTS
(the script looks for *-latin-wght-normal.woff2 files anywhere inside).
Colours come from theme.css tokens; the mark repeats assets/csg-logo.svg.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og"
W, H = 1200, 630

# theme.css tokens
PAPER = "#f7f5ef"
INK = "#1e2a2f"
MUTED = "#5d696d"
LINE = "#d4d1c7"
PRIMARY = "#466b67"
ACCENT = "#a84f2a"
SAND = "#e7dfd3"
SAGE = "#e8efe9"
# assets/csg-logo.svg
LOGO_BG = "#102631"
LOGO_LINE = "#f4f6f3"
LOGO_DOT = "#e65f2b"

ARTICLE_COVERS = {
    "articles/kak-poyavilas-kriptovalyuta": "crypto-origins.svg",
    "articles/seti-usdt-trc20-erc20": "usdt-networks.svg",
    "articles/zamorozka-usdt": "usdt-freeze.svg",
}

SECTION = {
    "": "Справочник для начинающих",
    "start": "Основы", "usdt": "Основы", "bitcoin": "Основы",
    "wallet": "Хранение", "transfer": "Переводы", "sell-usdt": "Продажа USDT",
    "articles": "Статьи", "english-terms": "Криптословарь",
    "about": "О проекте", "legal": "Правовая информация", "privacy": "Конфиденциальность",
    "service-status": "Проверка сервисов",
}


def og_name(slug):
    return (slug.replace("/", "-") or "home") + ".png"


def static_font(tmp, src_path, weight):
    src = TTFont(src_path)
    src.flavor = None
    inst = instancer.instantiateVariableFont(src, {"wght": weight})
    path = Path(tmp) / f"{Path(src_path).stem}-{weight}.ttf"
    inst.save(path)
    return str(path), set(inst.getBestCmap())


class Chain:
    """Cyrillic project font first, then the Latin subset of the same family."""

    def __init__(self, parts, size):
        self.fonts = [(ImageFont.truetype(path, size), cmap) for path, cmap in parts]

    def runs(self, text):
        out = []
        for ch in text:
            font = next((f for f, cmap in self.fonts if ord(ch) in cmap), self.fonts[0][0])
            if out and out[-1][0] is font:
                out[-1][1] += ch
            else:
                out.append([font, ch])
        return out

    def length(self, draw, text):
        return sum(draw.textlength(t, font=f) for f, t in self.runs(text))

    def draw(self, draw, xy, text, fill):
        x, y = xy
        ascent = max(f.getmetrics()[0] for f, _ in self.fonts)
        for f, t in self.runs(text):
            draw.text((x, y + ascent), t, font=f, fill=fill, anchor="ls")
            x += draw.textlength(t, font=f)


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if font.length(draw, trial) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_logo(draw, x, y, size):
    s = size / 64
    draw.rounded_rectangle([x, y, x + size, y + size], radius=int(10 * s), fill=LOGO_BG)
    pts = [(12, 44), (26, 44), (26, 32), (40, 32), (40, 20), (52, 20)]
    draw.line([(x + px * s, y + py * s) for px, py in pts], fill=LOGO_LINE, width=int(5 * s), joint="curve")
    for cx, cy in ((12, 44), (52, 20)):
        r = 5 * s
        draw.ellipse([x + cx * s - r, y + cy * s - r, x + cx * s + r, y + cy * s + r], fill=LOGO_DOT)


def title_card(fonts, slug, title):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # quiet background shapes, as in the article covers
    d.ellipse([-140, 430, 260, 830], fill=SAND)
    d.ellipse([960, -150, 1320, 210], fill=SAGE)

    draw_logo(d, 80, 72, 64)
    fonts["brand"].draw(d, (164, 78), "Crypto Step Guide", INK)
    section = SECTION.get(slug) or "Покупка USDT"
    fonts["eyebrow"].draw(d, (164, 117), section.upper(), MUTED)

    size = 72
    while True:
        font = Chain(fonts["title"], size)
        lines = wrap(d, title, font, W - 160)
        if len(lines) <= 3 or size <= 48:
            break
        size -= 4
    line_h = int(size * 1.16)
    block = line_h * len(lines)
    top = 200 + (300 - block) // 2
    for i, line in enumerate(lines):
        font.draw(d, (80, top + i * line_h), line, INK)

    d.rectangle([80, 540, 140, 545], fill=ACCENT)
    fonts["url"].draw(d, (80, 556), "crypto-step-guide.com", PRIMARY)
    d.line([(0, H - 1), (W, H - 1)], fill=LINE)
    return img


def main():
    seo = json.loads((ROOT / "content" / "seo.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    rsvg = shutil.which("rsvg-convert")
    latin_dir = os.environ.get("OG_LATIN_FONTS")
    if not latin_dir:
        raise SystemExit("Set OG_LATIN_FONTS to the folder with the Latin font subsets (see docstring)")
    latin = {p.name.split("-latin")[0]: p for p in Path(latin_dir).rglob("*-latin-wght-normal.woff2")}
    missing = {"literata", "commissioner"} - set(latin)
    if missing:
        raise SystemExit(f"Latin font subsets not found for: {sorted(missing)}")
    with tempfile.TemporaryDirectory() as tmp:
        def family(name, weight):
            return [static_font(tmp, ROOT / "fonts" / f"{name}-cyrillic-wght-normal.woff2", weight),
                    static_font(tmp, latin[name], weight)]
        title = family("literata", 620)
        bold = family("commissioner", 650)
        body = family("commissioner", 500)
        fonts = {"title": title, "brand": Chain(bold, 30), "eyebrow": Chain(bold, 17), "url": Chain(body, 24)}
        written = 0
        for slug, page in seo["pages"].items():
            target = OUT / og_name(slug)
            cover = ARTICLE_COVERS.get(slug)
            if cover:
                if not rsvg:
                    raise SystemExit("rsvg-convert is required to rasterise article covers")
                subprocess.run([rsvg, "-w", "1200", "-h", "675", "-o", str(target),
                                str(ROOT / "assets" / cover)], check=True)
            else:
                title_card(fonts, slug, page["content_title"]).save(target, optimize=True)
            written += 1
    print(f"Wrote {written} images to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

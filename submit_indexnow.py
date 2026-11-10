"""Send changed site URLs to IndexNow after the production domain is live."""

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="Absolute production URLs that changed")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    site_url = os.environ.get("SITE_URL", "https://crypto-step-guide.com").rstrip("/")
    key_file_source = Path(__file__).parent / ".indexnow-key"
    key = os.environ.get("INDEXNOW_KEY", "").strip()
    if not key and key_file_source.exists():
        key = key_file_source.read_text(encoding="utf-8").strip()
    if not site_url or not key:
        raise SystemExit("Set SITE_URL and INDEXNOW_KEY before using IndexNow.")

    host = urlparse(site_url).netloc
    if not host or any(urlparse(url).netloc != host for url in args.urls):
        raise SystemExit("Every submitted URL must use the SITE_URL host.")

    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{site_url}/{key}.txt",
        "urlList": args.urls,
    }
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    key_file = Path(__file__).parent / "dist" / f"{key}.txt"
    if not key_file.exists() or key_file.read_text(encoding="utf-8").strip() != key:
        raise SystemExit("Publish the matching IndexNow key file before submitting URLs.")

    request = Request(
        "https://api.indexnow.org/IndexNow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        print(f"IndexNow response: {response.status}")


if __name__ == "__main__":
    main()

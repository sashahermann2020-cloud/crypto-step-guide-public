"""Validate sell (off-ramp) routes and the generated /sell-usdt/ page.

Checks the data contract from content/sell-routes.schema.json without third-party
packages, plus product rules: P2P routes are never "ready" unless the buyer is a
licensed partner, Russia and Belarus carry a visible legal notice, and every
published route, step and source reaches the built page.
"""
import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "content/sell-routes.json").read_text(encoding="utf-8"))
schema = json.loads((ROOT / "content/sell-routes.schema.json").read_text(encoding="utf-8"))
services = json.loads((ROOT / "content/service-reviews.json").read_text(encoding="utf-8"))["services"]
page = (ROOT / "dist/sell-usdt/index.html").read_text(encoding="utf-8")
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def is_date(value):
    try:
        datetime.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


route_schema = schema["$defs"]["route"]
country_schema = schema["$defs"]["country"]
check(data.get("schema_version") == 1, "schema_version must be 1")
check(is_date(data.get("last_reviewed_on")), "last_reviewed_on must be an ISO date")
countries = data.get("countries", {})
for required in schema["properties"]["countries"]["required"]:
    check(required in countries, f"missing country {required}")

ids = set()
total = 0
for country, cfg in countries.items():
    extra = set(cfg) - set(country_schema["properties"])
    check(not extra, f"{country}: unknown keys {sorted(extra)}")
    check(bool(cfg.get("label")), f"{country}: label required")
    routes = cfg.get("routes", [])
    check(bool(routes) or bool(cfg.get("no_route")), f"{country}: needs routes or a no_route explanation")
    check(not (routes and cfg.get("no_route")), f"{country}: no_route must not coexist with routes")
    if country in ("russia", "belarus"):
        check(bool(cfg.get("legal_notice")), f"{country}: legal_notice is mandatory")
    if cfg.get("legal_notice"):
        check(html.escape(cfg["legal_notice"], quote=True) in page, f"{country}: legal notice not rendered")
    if cfg.get("no_route"):
        check(html.escape(cfg["no_route"], quote=True) in page, f"{country}: no_route text not rendered")
    check(f'id="sell-{country}"' in page, f"{country}: section anchor missing")
    for r in routes:
        total += 1
        rid = r.get("id", "?")
        missing = [k for k in route_schema["required"] if k not in r]
        check(not missing, f"{rid}: missing {missing}")
        extra = set(r) - set(route_schema["properties"])
        check(not extra, f"{rid}: unknown keys {sorted(extra)}")
        check(re.fullmatch(route_schema["properties"]["id"]["pattern"], rid) is not None, f"{rid}: bad id")
        check(rid not in ids, f"{rid}: duplicate id")
        ids.add(rid)
        check(rid[:2] == {"kazakhstan": "kz", "kyrgyzstan": "kg", "uzbekistan": "uz", "russia": "ru", "ukraine": "ua", "belarus": "by", "serbia": "rs"}.get(country, rid[:2]), f"{rid}: id prefix does not match {country}")
        check(r.get("status") in route_schema["properties"]["status"]["enum"], f"{rid}: bad status")
        check(r.get("method") in route_schema["properties"]["method"]["enum"], f"{rid}: bad method")
        check(re.fullmatch(r"[A-Z]{3}", r.get("currency", "")) is not None, f"{rid}: bad currency")
        check(is_date(r.get("last_source_reviewed")), f"{rid}: bad last_source_reviewed")
        check(r.get("transaction_tested") is False, f"{rid}: transaction_tested may change only after a real test")
        check(r.get("service_id") in services, f"{rid}: unknown service_id {r.get('service_id')}")
        check(len(r.get("steps", [])) >= 2, f"{rid}: at least two steps")
        if country in ("russia", "belarus", "ukraine", "serbia", "kyrgyzstan", "uzbekistan"):
            check(r.get("status") == "conditional", f"{rid}: {country} routes stay conditional")
        if r.get("method") == "p2p" and r.get("status") == "ready":
            check("лиценз" in (r.get("evidence_scope", "") + r.get("label", "")).lower(), f"{rid}: a ready P2P route needs a licensed counterparty")
        check(f'id="{rid}"' in page, f"{rid}: card not rendered")
        for text in r.get("steps", []) + r.get("checks_before_sale", []) + [r.get("payout", ""), r.get("evidence_scope", "")]:
            check(html.escape(text, quote=True) in page, f"{rid}: text not rendered: {text[:40]}")
        for src in r.get("sources", []):
            check(src.get("url", "").startswith("https://"), f"{rid}: source must be https")
            check(html.escape(src.get("url", ""), quote=True) in page, f"{rid}: source not rendered {src.get('url')}")
            check(bool(src.get("label")), f"{rid}: source label required")

# A P2P seller must never be told to release coins before the money is visible.
for country, cfg in countries.items():
    for r in cfg.get("routes", []):
        if r.get("method") == "p2p":
            joined = " ".join(r["steps"]).lower()
            check("только после" in joined, f"{r['id']}: P2P steps must say to release only after the money arrives")

check('href="/sell-usdt/"' in (ROOT / "dist/index.html").read_text(encoding="utf-8"), "header must link to /sell-usdt/")
check("<script>" not in page, "/sell-usdt/ must stay static")

if errors:
    raise SystemExit("Sell routes invalid:\n" + "\n".join(errors))
print(f"Sell routes valid: {total} routes in {len(countries)} countries; legal notices, steps and sources rendered on /sell-usdt/.")

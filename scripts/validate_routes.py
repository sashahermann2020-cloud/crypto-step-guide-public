import re
#!/usr/bin/env python3
"""Integrity checks for the published route model and page wiring."""
import ast
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "content/routes.json").read_text(encoding="utf-8"))
assert data.get("schema_version") == 1, "Unsupported route schema version"
review_date = date.fromisoformat(data["last_reviewed_on"])
countries = data["routes_by_country"]
assert set(countries) == {"ukraine", "belarus", "russia", "kazakhstan", "kyrgyzstan", "uzbekistan", "serbia"}
services = json.loads((ROOT / "content/service-reviews.json").read_text(encoding="utf-8"))["services"]
required = {
    "id", "name", "status", "label", "currency", "payment", "service", "source",
    "steps", "last_source_reviewed", "transaction_tested", "evidence_scope",
    "service_id", "methods", "funding_mode", "purchase_step_count",
    "checks_before_payment", "sources", "allowed_destinations",
}
allowed_methods = {"bank", "card", "local", "p2p"}
allowed_destinations = {"trust", "tronlink", "other", "exchange"}
seen = set()

for country, routes in countries.items():
    assert isinstance(routes, list), f"{country}: expected a route list"
    for route in routes:
        missing = required - route.keys()
        assert not missing, f"{country}/{route.get('id')}: missing {sorted(missing)}"
        assert route["status"] in {"ready", "conditional", "blocked"}, route["id"]
        assert route["source"].startswith("https://"), route["id"]
        assert route["steps"] and all(step.strip() for step in route["steps"]), route["id"]
        assert 1 <= route["purchase_step_count"] <= len(route["steps"]), route["id"]
        assert route["methods"] and set(route["methods"]) <= allowed_methods, route["id"]
        assert route["funding_mode"] in {"balance", "p2p", "direct"}, route["id"]
        if route.get("fixed_destination"):
            assert route["fixed_destination"] == "personal_wallet", route["id"]
            assert set(route["allowed_destinations"]) <= {"trust", "tronlink", "other"}, route["id"]
        assert route["checks_before_payment"] and all(x.strip() for x in route["checks_before_payment"]), route["id"]
        assert route["allowed_destinations"] and set(route["allowed_destinations"]) <= allowed_destinations, route["id"]
        assert route["sources"] and route["source"] in {s["url"] for s in route["sources"]}, route["id"]
        assert all(s.get("label", "").strip() and s.get("url", "").startswith("https://") for s in route["sources"]), route["id"]
        if "purchase_url" in route:
            assert route["purchase_url"].startswith("https://"), route["id"]
            assert route.get("purchase_label", "").strip(), route["id"]
            assert route["purchase_url"] in {s["url"] for s in route["sources"]}, route["id"]
        assert route["service_id"] in services, f"{route['id']}: unknown service_id"
        reviewed = date.fromisoformat(route["last_source_reviewed"])
        assert reviewed <= review_date, f"{route['id']}: review date is in the future"
        assert route["transaction_tested"] is False, f"{route['id']}: this project has not run live transactions"
        assert route["id"] not in seen, f"Duplicate route id: {route['id']}"
        seen.add(route["id"])

russia = countries["russia"]
assert len(russia) == 1 and russia[0]["id"] == "ru-bybit-p2p"
ru = russia[0]
assert ru["status"] == "conditional"
assert ru["allowed_destinations"] == ["exchange"] and ru["wallet_withdrawal_blocked"] is True
assert "некастодиальный" in ru["evidence_scope"] and "17 октября" in ru["evidence_scope"]
assert "https://www.cbr.ru/rbr/rbr_fr/doc?id=51682" in {s["url"] for s in ru["sources"]}

kz_routes = {r["id"]: r for r in countries["kazakhstan"]}
assert len(kz_routes) == 8
assert {k for k in kz_routes if k.startswith("kz-ausu-")} == {"kz-ausu-card", "kz-ausu-iban", "kz-ausu-cash-shymkent"}
assert kz_routes["kz-binance-p2p-maker"]["methods"] == ["p2p"]
assert kz_routes["kz-binance-p2p-maker"]["status"] == "ready"
assert kz_routes["kz-bybit-bank"]["status"] == "ready"
assert "не требуется иметь отдельный счёт именно в Bank CenterCredit" in " ".join(kz_routes["kz-bybit-bank"]["checks_before_payment"])
assert "именно в Bank CenterCredit" in " ".join(kz_routes["kz-bybit-bank"]["checks_before_payment"])
uz = countries["uzbekistan"]
assert len(uz) == 3 and {r["id"] for r in uz} == {"uz-asterium", "uz-citypay-online", "uz-voluto-cash-tashkent"}
assert uz[0]["status"] == "ready" and uz[0]["network"] == "TRON (TRC-20)"
assert any("napp.uz" in s["url"] for s in uz[0]["sources"])
serbia_routes = {r["id"]: r for r in countries["serbia"]}
assert set(serbia_routes) == {"rs-ecd-wallet-rsd", "rs-ecd-atm-cash"}
assert all(r["status"] == "conditional" for r in serbia_routes.values())
assert serbia_routes["rs-ecd-wallet-rsd"]["methods"] == ["bank"]
assert "ERC-20" in serbia_routes["rs-ecd-atm-cash"]["network"]
assert serbia_routes["rs-ecd-atm-cash"]["fixed_destination"] == "personal_wallet"
assert "tronlink" not in serbia_routes["rs-ecd-atm-cash"]["allowed_destinations"]
assert all(r["transaction_tested"] is False for rs in countries.values() for r in rs)

template = (ROOT / "buy-usdt-page.html").read_text(encoding="utf-8")
finder = (ROOT / "where-to-buy-page.html").read_text(encoding="utf-8")
generator = (ROOT / "generate.py").read_text(encoding="utf-8")
assert "__ROUTE_DATA_JSON__" in template, "Buy USDT page must render the canonical route model"
assert "wallet_withdrawal_blocked" in template and "wallet-guidance" in template
assert "r.purchase_url" in template and "r.purchase_label" in template, "Published route plans must render their official purchase CTA"
assert "__WIZARD_DATA_JSON__" in template, "Buy USDT page must embed the wizard model"
assert "__ROUTE_SUMMARY_HTML__" in finder and "/buy-usdt/#wizard" in finder, "Where-to-buy must list routes statically and lead into the wizard"
assert "ROUTE_CONTENT" in generator and "WIZARD_CONTENT" in generator
assert "where_to_buy_body" in generator and "buy_usdt_body" in generator
assert "По FAQ Банка России" in template and "ООО «Развитие финансовых технологий»" in template
assert "Sberbank" not in template and "Т-Инвест Лаб" not in template


# Beginner wizard: every published route is reachable and every answer leads somewhere explainable.
wizard = json.loads((ROOT / "content/wizard.json").read_text(encoding="utf-8"))
assert wizard.get("schema_version") == 1
assert set(wizard["countries"]) == set(countries), "Wizard must cover exactly the route countries"
no_route_countries = set()
reachable = set()
for country, cfg in wizard["countries"].items():
    ids = {r["id"] for r in countries[country]}
    if cfg.get("no_route"):
        no_route_countries.add(country)
        no = cfg["no_route"]
        assert not countries[country] and not cfg["payments"], f"{country}: no_route state cannot have routes or payment options"
        assert country in {"ukraine", "belarus"} and no.get("status") == "research"
        assert all(no.get(k) for k in ("short_hint", "title", "message"))
        assert no.get("next_steps") and all(x.strip() for x in no["next_steps"])
        assert no.get("sources") and all(s.get("label", "").strip() and s.get("url", "").startswith("https://") for s in no["sources"])
        continue
    assert cfg["payments"], f"{country}: wizard needs at least one payment option"
    assert cfg.get("payment_unknown"), f"{country}: wizard needs a 'Не знаю' explanation"
    payment_ids = {p["id"] for p in cfg["payments"]}
    for pay in cfg["payments"]:
        assert pay.get("title") and pay.get("hint"), f"{country}/{pay['id']}: title and hint required"
        if pay.get("choices"):
            assert pay.get("question") and pay.get("unknown") and pay.get("answer_label")
            for ch in pay["choices"]:
                if ch.get("route"):
                    assert ch["route"] in ids, f"{country}: unknown route {ch['route']}"
                    assert ch.get("why"), f"{ch['route']}: wizard must explain why"
                    reachable.add(ch["route"])
                    if ch.get("alternative"):
                        assert ch["alternative"] in ids
                else:
                    assert ch.get("message") and ch.get("redirect_payment") in payment_ids, f"{country}/{ch['id']}: dead end needs a message and redirect"
        elif pay.get("route"):
            assert pay["route"] in ids and pay.get("why")
            reachable.add(pay["route"])
        else:
            assert pay.get("message"), f"{country}/{pay['id']}: unavailable option needs an explanation"
assert no_route_countries == set(), f"All MVP countries now have published route scenarios; found no-route states {sorted(no_route_countries)}"
assert {r["id"] for r in countries["ukraine"]} == {"ua-bybit-p2p"}
assert {r["id"] for r in countries["belarus"]} == {"by-dzengi", "by-free2ex"}
for route_id in ("ua-bybit-p2p", "by-dzengi", "by-free2ex"):
    route = next(r for rs in countries.values() for r in rs if r["id"] == route_id)
    assert route["status"] == "conditional" and route["purchase_url"] and route["purchase_label"]
    assert any("неяс" in check.lower() or "подтвердите" in check.lower() for check in route["checks_before_payment"])
for route in countries["belarus"]:
    checks = " ".join(route["checks_before_payment"]).lower()
    assert "публичные интернет-ресурсы" in checks and "1zf" in checks
assert sum(map(len, countries.values())) == 18
kg = countries["kyrgyzstan"]
assert [r["id"] for r in kg] == ["kg-dantepay-elqr"] and kg[0]["status"] == "conditional"
assert any("fsa.gov.kg" in s["url"] for s in kg[0]["sources"]), "Kyrgyz route must cite the official register"
assert "tronlink" not in kg[0]["allowed_destinations"], "DantePay does not publish a TRON-only network"
published = {r["id"] for rs in countries.values() for r in rs if r["status"] != "blocked"}
assert published <= reachable, f"Routes not reachable from the wizard: {sorted(published - reachable)}"
assert "Условный сценарий – только до баланса сервиса" in next(p["hint"] for p in wizard["countries"]["russia"]["payments"] if p.get("route") == "ru-bybit-p2p")
assert {o["id"] for o in wizard["storage"]["options"]} == {"own", "exchange"} and wizard["storage"].get("unknown")
assert {w["id"] for w in wizard["wallets"]} == {"trust", "tronlink"}
assert all(w["url"].startswith("https://") for w in wizard["wallets"])
assert all(set(w.get("app_store_countries",[])) <= set(wizard["countries"]) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", w.get("app_store_checked_on","2000-01-01")) for w in wizard["wallets"]), "wallet app_store_countries must be known countries with a check date"
assert wizard["wallet_setup_steps"] and wizard["network_rule_default"] and wizard["network_rule_tronlink"]
for country in ("ukraine", "belarus"):
    assert not wizard["countries"][country].get("no_route"), f"{country}: active route must replace the old no_route state"
    assert wizard["countries"][country]["payments"], f"{country}: payment selection is required"
assert any(p.get("route") == "ua-bybit-p2p" for p in wizard["countries"]["ukraine"]["payments"])
assert any(ch.get("route") == "by-dzengi" for p in wizard["countries"]["belarus"]["payments"] for ch in p.get("choices", []))
assert any(ch.get("route") == "by-free2ex" for p in wizard["countries"]["belarus"]["payments"] for ch in p.get("choices", []))
print(f"Wizard data valid: {len(reachable)} reachable routes, {sum(len(c['payments']) for c in wizard['countries'].values())} payment options.")

print(f"Route data valid: {sum(map(len, countries.values()))} routes across {len(countries)} country states; {len(no_route_countries)} have no published route.")

# Language variants (es/pt/en): reference pages in the language of the country, outside the Russian wizard.
variants = data["language_variants"]
assert variants.get("schema_version") == 1
assert date.fromisoformat(variants["last_reviewed_on"]) <= date.today()
vc = variants["countries"]
expected_variants = {
    "argentina": ("es", "es/argentina", {"ar-lemon", "ar-ripio", "ar-belo"}),
    "venezuela": ("es", "es/venezuela", {"ve-crixto"}),
    "espana": ("es", "es/espana", {"es-bit2me"}),
    "brasil": ("pt", "pt/brasil", {"br-foxbit", "br-mb"}),
    "india": ("en", "en/india", {"in-coindcx"}),
    "nigeria": ("en", "en/nigeria", {"ng-quidax"}),
}
assert set(vc) == set(expected_variants), "Language variants must cover exactly the six agreed countries"
variant_required = required - {"service_id", "allowed_destinations"}
variant_ids = set()
for country, (lang, slug, ids) in expected_variants.items():
    entry = vc[country]
    assert entry["language"] == lang and entry["slug"] == slug, f"{country}: language/slug mismatch"
    assert {r["id"] for r in entry["routes"]} == ids, f"{country}: unexpected route ids"
    for route in entry["routes"]:
        missing = variant_required - route.keys()
        assert not missing, f"{country}/{route.get('id')}: missing {sorted(missing)}"
        assert route["status"] == "conditional", f"{route['id']}: language-variant routes stay conditional until verified in a real session"
        assert route["transaction_tested"] is False, route["id"]
        assert route["source"].startswith("https://") and route["source"] in {s["url"] for s in route["sources"]}, route["id"]
        assert all(s.get("label", "").strip() and s["url"].startswith("https://") for s in route["sources"]), route["id"]
        assert route["steps"] and all(x.strip() for x in route["steps"]) and route["checks_before_payment"], route["id"]
        assert 1 <= route["purchase_step_count"] <= len(route["steps"]), route["id"]
        assert route["evidence_scope"].strip() and route["label"].strip(), route["id"]
        assert date.fromisoformat(route["last_source_reviewed"]) <= date.fromisoformat(variants["last_reviewed_on"]), route["id"]
        assert route["id"] not in seen and route["id"] not in variant_ids, f"Duplicate route id: {route['id']}"
        variant_ids.add(route["id"])
lang_copy = json.loads((ROOT / "content/language-variants.json").read_text(encoding="utf-8"))
assert lang_copy.get("schema_version") == 1
assert set(lang_copy["countries"]) == set(vc) and set(lang_copy["languages"]) == {"es", "pt", "en"}
ui_keys = set(lang_copy["languages"]["es"]["ui"])
for lang, cfg in lang_copy["languages"].items():
    assert set(cfg["ui"]) == ui_keys, f"{lang}: interface strings differ from the Spanish set"
    assert all(isinstance(v, str) and v.strip() for v in cfg["ui"].values()), lang
    assert cfg["countries"] == [k for k, (l, _, _) in expected_variants.items() if l == lang], lang
    assert cfg["hub"].get("h1") and cfg["hub"].get("intro") and cfg["hub"].get("note"), lang
for country, cfg in lang_copy["countries"].items():
    assert cfg["language"] == vc[country]["language"], country
    assert cfg["intro"].strip() and cfg["alerts"] and cfg["law"] and cfg["next"].strip(), country
    assert all(x["url"].startswith("https://") and x["text"].strip() for x in cfg["law"] + cfg["tax_links"]), country
# Language variants must not leak into the Russian route model or wizard.
wizard_text = (ROOT / "content/wizard.json").read_text(encoding="utf-8")
assert not (variant_ids & {r["id"] for rs in countries.values() for r in rs}), "variant ids clash with wizard routes"
assert not any(i in wizard_text for i in variant_ids), "wizard must not reference language-variant routes"
print(f"Language variants valid: {len(variant_ids)} routes in {len(vc)} countries (es, pt, en).")

# Every public page has SEO metadata in the model used by the generator.
seo = json.loads((ROOT / "content/seo.json").read_text(encoding="utf-8"))
assert seo.get("schema_version") == 1
module = ast.parse(generator)
expected_slugs = None
for node in module.body:
    if isinstance(node, ast.Assign):
        if any(isinstance(target, ast.Name) and target.id == "slugs" for target in node.targets):
            expected_slugs = ast.literal_eval(node.value)
            break
assert expected_slugs is not None, "Site generator must declare its route list"
assert set(seo["pages"]) == set(expected_slugs), "SEO model must cover every generated page"
for slug, page in seo["pages"].items():
    assert all(isinstance(page.get(k), str) and page[k].strip()
               for k in ("content_title", "title", "description")), f"Invalid SEO metadata: {slug}"
assert "SEO_CONTENT=json.loads" in generator, "Generator must consume the SEO model"
print(f"SEO metadata valid: {len(seo['pages'])} generated pages.")

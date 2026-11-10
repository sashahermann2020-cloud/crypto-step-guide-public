"""Validate published metadata, model consistency and local link targets."""
import json, re
import html
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.canonical=[];self.h1=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if attrs.get('id'):self.ids.add(attrs['id'])
        if tag=='a' and attrs.get('href'):self.links.append(attrs['href'])
        if tag=='h1':self.h1+=1
        if tag=='link' and attrs.get('rel')=='canonical':self.canonical.append(attrs['href'])

pages={p.relative_to(DIST).as_posix():Page(p.read_text()) for p in DIST.rglob('*.html') if p.relative_to(DIST).as_posix()!='404.html'}
# 404.html is served by Cloudflare Pages with HTTP 404; it must not compete with real pages in search.
not_found_path=DIST/'404.html'
assert not_found_path.is_file(),'404.html is missing'
not_found_text=not_found_path.read_text()
not_found=Page(not_found_text)
assert not not_found.canonical,'404.html must not have a canonical URL'
assert 'name="robots" content="noindex' in not_found_text,'404.html must be noindex'
assert not_found.h1==1,'404.html: missing or duplicated main heading'
assert all(h.startswith(('/','#')) or urlsplit(h).scheme for h in not_found.links),'404.html links must be root-relative'
pages['404.html']=not_found
errors=[]
for path,page in pages.items():
    text=(DIST/path).read_text()
    if path=='404.html':
        for href in page.links:
            target=urlsplit(href).path.lstrip('/')
            target=(target.rstrip('/')+'/index.html') if target else 'index.html'
            if not urlsplit(href).scheme and not href.startswith('#') and not (DIST/target).exists():errors.append(f'404.html: missing {href}')
        continue
    assert not re.search(r'__[A-Z_]+__',text),f'Unresolved template: {path}'
    assert page.h1==1,f'Missing or duplicated main heading: {path}'
    slug=path.removesuffix('index.html')
    assert page.canonical==['https://crypto-step-guide.com/'+slug],path
    for href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=(u.path.lstrip('/') if u.path.startswith('/') else slug+u.path) if u.path else path
        if target.endswith('/') or not Path(target).suffix:target=target.rstrip('/')+'/index.html' if target.rstrip('/') else 'index.html'
        if not (DIST/target).exists():errors.append(f'{path}: missing {href}');continue
        # #country=…&route=… — состояние мастера, а не якорь: проверяется тестом scripts/test_route_wizard.mjs.
        if u.fragment and target in pages and not u.fragment.startswith('country=') and unquote(u.fragment) not in pages[target].ids:errors.append(f'{path}: missing anchor {href}')
assert not errors,'\n'.join(errors)
data=json.loads((ROOT/'content/routes.json').read_text())
service_data=json.loads((ROOT/'content/service-reviews.json').read_text())
status=(DIST/'service-status/index.html').read_text()
buy=(DIST/'buy-usdt/index.html').read_text()
finder=(DIST/'where-to-buy/index.html').read_text()
buy_embedded=re.search(r'<script type="application/json" id="route-data">(.*?)</script>',buy,re.S)
wizard_data=json.loads((ROOT/'content/wizard.json').read_text())
wizard_embedded=re.search(r'<script type="application/json" id="wizard-data">(.*?)</script>',buy,re.S)
assert buy_embedded and wizard_embedded
assert json.loads(buy_embedded.group(1))['routes_by_country']==data['routes_by_country']
assert json.loads(wizard_embedded.group(1))==wizard_data
assert 'id="route-data"' not in finder and '<script>' not in finder, 'where-to-buy must be static'
for routes in data['routes_by_country'].values():
    for route in routes:
        # The buy wizard embeds the canonical model; where-to-buy links every published route into it.
        assert f'"id":"{route["id"]}"' in buy
        assert route['last_source_reviewed'] in buy
        if route['status']!='blocked':
            assert f'route={route["id"]}' in finder and f'#country=' in finder, route['id']
russia_bybit = data['routes_by_country']['russia'][0]
assert russia_bybit['service'] in status
assert 'личный некастодиальный кошелёк' in status
assert 'RUB → USDT → личный кошелёк не подтверждён' in buy
route_count=sum(map(len, data['routes_by_country'].values()))
assert route_count == 18
for country, expected in (('ukraine', {'ua-bybit-p2p'}), ('belarus', {'by-dzengi','by-free2ex'})):
    routes=data['routes_by_country'][country]
    assert {r['id'] for r in routes} == expected
    assert wizard_data['countries'][country]['payments']
    assert 'no_route' not in wizard_data['countries'][country]
    assert f'id="{country}"' in buy
    for route in routes:
        assert route['status']=='conditional'
        assert route['purchase_url'] in buy, route['id']
        assert html.escape(route['purchase_url'],quote=True) in finder, route['id']
        assert f'route={route["id"]}' in finder
        assert all(html.escape(source['url'],quote=True) in finder for source in route['sources'])
ua_section=buy[buy.find('id="ukraine"'):buy.find('id="belarus"')]
by_section=buy[buy.find('id="belarus"'):buy.find('id="kazakhstan"')]
assert 'Bybit P2P' in ua_section and 'WhiteBIT P2P Express остаётся' in ua_section
assert 'Условный маршрут' in ua_section and '/buy-usdt/#country=ukraine' in ua_section
assert 'Dzengi' in by_section and 'FREE2EX' in by_section
assert 'не регистрируйтесь и не вносите деньги' in by_section
assert '/buy-usdt/#country=belarus' in by_section
status_page=(DIST/'service-status/index.html').read_text()
assert 'Bybit P2P' in status_page and 'Dzengi' in status_page and 'FREE2EX' in status_page
assert 'BYNEX / ERPBEL' in status_page and 'WhiteBIT P2P Express' in status_page
assert 'применимость' in status_page
sitemap=ET.parse(DIST/'sitemap.xml')
locations=[x.text for x in sitemap.findall('.//{*}loc')]
assert set(locations)=={p.canonical[0] for k,p in pages.items() if k!='404.html'}
# Language variants: every route, its sources and the official links are rendered on the page in the language of the country.
for country,entry in data['language_variants']['countries'].items():
    page_html=(DIST/entry['slug']/'index.html').read_text()
    assert f'<html lang="{entry["language"]}"' in page_html,entry['slug']
    for route in entry['routes']:
        assert f'id="{route["id"]}"' in page_html,route['id']
        assert html.escape(route['payment'],quote=True) in page_html,route['id']
        assert all(html.escape(x,quote=True) in page_html for x in route['steps']),route['id']
        assert all(html.escape(x,quote=True) in page_html for x in route['checks_before_payment']),route['id']
        assert all(html.escape(source['url'],quote=True) in page_html for source in route['sources']),route['id']
        assert html.escape(route['evidence_scope'],quote=True) in page_html,route['id']
    # variant pages must not appear in the Russian wizard data embedded on /buy-usdt/
    assert not any(route['id'] in buy for route in entry['routes']),country
print(f'Build valid: {len(pages)-1} pages + 404, sitemap, canonical URLs, local links and {route_count} synchronized routes.')

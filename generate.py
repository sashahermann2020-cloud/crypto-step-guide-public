from pathlib import Path
import html
import hashlib
import json
import os
import shutil
D=Path(__file__).parent/'dist'
SEO_CONTENT=json.loads((Path(__file__).parent/'content/seo.json').read_text(encoding='utf-8'))
ROUTE_CONTENT=json.loads((Path(__file__).parent/'content/routes.json').read_text(encoding='utf-8'))
SERVICE_REVIEW_CONTENT=json.loads((Path(__file__).parent/'content/service-reviews.json').read_text(encoding='utf-8'))
WIZARD_CONTENT=json.loads((Path(__file__).parent/'content/wizard.json').read_text(encoding='utf-8'))
SELL_CONTENT=json.loads((Path(__file__).parent/'content/sell-routes.json').read_text(encoding='utf-8'))
LANG_CONTENT=json.loads((Path(__file__).parent/'content/language-variants.json').read_text(encoding='utf-8'))
BASE_URL=os.environ.get('SITE_URL','https://crypto-step-guide.com').rstrip('/')
UPDATED='2026-10-16'
MODIFIED={'':'2026-11-07','about':'2026-11-07','sell-usdt':'2026-11-06','articles/zamorozka-usdt':'2026-11-06','articles':'2026-11-06','articles/seti-usdt-trc20-erc20':'2026-10-21','buy':'2026-10-30','buy-usdt':'2026-10-30','where-to-buy':'2026-10-30','service-status':'2026-10-30','buy-usdt-kazakhstan-card':'2026-10-27','buy-usdt-shymkent-cash':'2026-10-27','buy-usdt-uzbekistan-card':'2026-10-27','buy-usdt-tashkent-cash':'2026-10-27','buy-usdt-serbia-bank':'2026-10-27','buy-usdt-serbia-crypto-atm':'2026-10-27','wallet':'2026-10-21','transfer':'2026-10-21','legal':'2026-11-06','privacy':'2026-11-06','es':'2026-11-10','pt':'2026-11-10','en':'2026-11-10','es/argentina':'2026-11-10','es/venezuela':'2026-11-10','es/espana':'2026-11-10','pt/brasil':'2026-11-10','en/india':'2026-11-10','en/nigeria':'2026-11-10'}
PUBLISHED='2026-09-11'
pages=[
('start','Разобраться с нуля','Как устроена криптовалюта','Начните с основных различий, прежде чем выбирать сервис или переводить деньги.','Основы',[
('Определите свою задачу','Покупка для хранения, оплата и перевод другому человеку требуют разной подготовки. Запишите, какой результат вам нужен.','Вы можете объяснить, зачем вам нужна криптовалюта.'),
('Разделите монету, кошелёк и сеть','Монета является активом, кошелёк даёт доступ к нему, а сеть проводит перевод. Название монеты само по себе не определяет сеть.','Вам известны актив и сеть, которые принимает получатель.'),
('Оцените возможную потерю','Цена может измениться. Ошибочный перевод часто нельзя отменить. Начните с изучения инструкции и не используйте деньги, необходимые для повседневных расходов.','Вы понимаете риски до покупки.')],'wallet'),
('wallet','Выбрать кошелёк','Криптокошелёк: как выбрать','Сначала решите, кто будет управлять доступом к вашим средствам.','Хранение',[
('Выберите способ управления','В кастодиальном сервисе доступом к активам управляет компания. В самостоятельном кошельке ответственность за ключи лежит на вас. Удобство восстановления и риски у этих вариантов различаются.','Вы знаете, кто контролирует ключи и как восстанавливается доступ.'),
('Проверьте совместимость','Кошелёк должен поддерживать нужную монету и конкретную сеть. Скачивайте приложение по ссылке с официального сайта разработчика, сверив издателя.','В кошельке есть нужный актив в нужной сети.'),
('Подготовьте восстановление','Если кошелёк выдаёт секретную фразу, сохраните её офлайн и никому не передавайте. Не вводите её на сайтах по просьбе поддержки. Для аккаунта сервиса включите доступную двухфакторную защиту.','Вы знаете способ восстановления и храните его отдельно от устройства.')],'buy'),
('usdt','Понять USDT','Что такое USDT','Простое объяснение USDT: как токен связан с долларом, в каких сетях работает и какие риски нужно проверить до покупки или перевода.','Основы',[
('Поймите привязку к доллару','USDT выпускает компания Tether. Токен ориентирован на стоимость одного доллара США, но его рыночная цена может отклоняться. Это не банковский долларовый вклад.','Вы отличаете токен от денег на банковском счёте.'),
('Уточните сеть','USDT существует в разных сетях. Перед получением выясните, какую сеть поддерживает ваш кошелёк или сервис. Чем отличаются TRC-20, ERC-20 и BEP-20, объясняет статья <a href="/articles/seti-usdt-trc20-erc20/">«Почему у USDT несколько сетей и как выбрать нужную»</a>.','Отправитель и получатель выбрали одну и ту же сеть.'),
('Учтите ограничения','Есть риски эмитента, платформы и сети. Доступность покупки зависит от страны и сервиса. Перед операцией проверьте условия конкретной площадки.','Вы проверили доступность и не воспринимаете привязку как гарантию.')],'buy-usdt'),
('buy','Купить криптовалюту','Первая покупка: порядок действий','Подготовка, проверка условий и контроль результата.','Покупка',[
('Выберите актив под задачу','Для перевода узнайте у получателя точное название актива и сеть. Для покупки с целью хранения сначала разберитесь в риске изменения цены. Низкая цена одной монеты не означает выгодную покупку.','Вы знаете, какой актив нужен и почему.'),
('Проверьте площадку','Уточните доступность для вашей страны проживания, способы оплаты, условия идентификации и вывода. Переходите на официальный сайт самостоятельно.','Вы прочитали условия пополнения и вывода до внесения денег.'),
('Сравните итоговую сумму','Посмотрите, сколько спишут, сколько криптовалюты зачислят и сколько будет стоить дальнейший вывод. Не ориентируйтесь только на надпись «без комиссии».','Вам понятна полная стоимость операции.'),
('Проверьте зачисление','После первой покупки откройте историю операций и баланс. Сохраните подтверждение и сведения о стоимости покупки.','Операция завершена, актив зачислен, подтверждение сохранено.')],'transfer'),
('buy-usdt','Купить USDT','Как подготовиться к покупке USDT','Пройдите проверки до внесения денег. Доступность USDT различается по странам и площадкам.','Покупка',[
('Уточните назначение','Если USDT нужен для оплаты, запросите у получателя монету, сеть и сумму. Не покупайте по сообщению незнакомца с обещанием дохода.','Вы проверили получателя и назначение платежа.'),
('Проверьте доступность','На официальном сайте выбранного сервиса выясните, доступна ли покупка USDT для вашего места проживания. Изучите условия идентификации и последующего вывода.','Покупка и нужный способ вывода доступны вашему аккаунту.'),
('Посмотрите итог перед оплатой','Проверьте валюту списания, сумму USDT к получению и все показанные комиссии. Если нужен перевод, отдельно уточните стоимость вывода и поддерживаемую сеть.','Сеть подходит получателю, итоговая стоимость понятна.'),
('Сохраните результат','Проверьте завершение покупки в истории и появление USDT на балансе. Сохраните подтверждение операции.','Количество USDT соответствует подтверждённой покупке.')],'transfer'),
('bitcoin','Купить Bitcoin','Нужно ли покупать целый биткоин?','Нет, можно купить часть Bitcoin. Объясняем, как определить сумму расходов и выбрать способ хранения.','Покупка',[
('Задайте сумму в привычной валюте','При покупке вы можете указать сумму в евро и получить соответствующую долю BTC. Цена целой монеты не равна минимальной сумме входа.','Вы понимаете, сколько евро тратите, а не только сколько BTC получаете.'),
('Проверьте условия покупки','Уточните минимальную сумму, итоговый курс, комиссии и возможность вывода BTC в свой кошелёк. Цена биткоина может существенно меняться.','Вы знаете сумму списания и условия вывода.'),
('Проверьте результат','После покупки сверьте баланс BTC и историю операции. Если планируете самостоятельное хранение, сначала изучите кошелёк и резервное восстановление.','Подтверждение сохранено, способ хранения понятен.')],'wallet'),
('transfer','Перевести криптовалюту','Как перевести криптовалюту: адрес, сеть и комиссия','Пошаговая проверка адреса, сети, комиссии и результата перед переводом Bitcoin или USDT на другой кошелёк.','Переводы',[
('Получите реквизиты','Попросите получателя указать актив, сеть и адрес. Уточните, требуется ли дополнительный идентификатор memo или tag.','Все реквизиты получены из надёжного канала.'),
('Сверьте сеть с обеих сторон','Не выбирайте сеть только по низкой комиссии. Она должна поддерживаться отправителем и получателем. Одинаковый формат адреса ещё не доказывает совместимость.','Актив и сеть совпадают на обеих сторонах.'),
('Проверьте расходы','В самостоятельном кошельке комиссия может оплачиваться отдельным активом сети. У сервиса может быть собственная комиссия вывода. Проверьте минимальную сумму зачисления.','Хватает средств на комиссию, получатель получит нужную сумму.'),
('Отправьте тест и дождитесь получения','Для нового адреса можно сначала отправить сумму выше установленного минимума. До решения посчитайте комиссию тестового и основного переводов. Сверьте полный адрес перед подтверждением и дождитесь фактического зачисления.','Получатель подтвердил зачисление в нужной сети.')],'buy-usdt')]
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--surface);font:18px/1.65 Arial,sans-serif}a{color:var(--primary);text-underline-offset:4px}.en-term{font-weight:600;text-decoration-style:dotted;text-decoration-thickness:1px}a:focus-visible,summary:focus-visible{outline:3px solid var(--primary);outline-offset:5px}header{border-bottom:1px solid var(--line)}nav{max-width:1160px;margin:auto;display:flex;align-items:center;justify-content:space-between;padding:24px 28px;gap:20px}.brand{color:var(--ink);text-decoration:none;font-size:21px;font-weight:700;letter-spacing:-.5px}.brand b{color:var(--primary);margin-right:10px}nav .links{display:flex;gap:28px;font-size:15px}nav .links a{color:var(--muted);text-decoration:none}main{max-width:1160px;margin:auto;padding:56px 28px 72px}.eyebrow{font-size:13px;letter-spacing:1.8px;font-weight:700;color:var(--muted);text-transform:uppercase}h1{font-size:clamp(32px,4.4vw,52px);line-height:1.15;letter-spacing:-1.8px;margin:18px 0}h2{font-size:28px;line-height:1.3;letter-spacing:-.6px}h3{font-size:21px;line-height:1.35}p{margin:12px 0 20px}.intro{max-width:670px;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:36px 0}.card{border:1px solid var(--line);border-radius:12px;padding:26px 28px;text-decoration:none;color:inherit;position:relative;transition:background .15s,border-color .15s}.card:hover{background:var(--surface);border-color:var(--primary)}.card .num{color:var(--primary);font:14px monospace}.card h2{margin:12px 0 8px;font-size:25px}.card p{color:var(--muted);font-size:16px;margin:0 35px 0 0}.card .arrow{position:absolute;right:25px;bottom:25px;color:var(--primary)}.start{background:var(--surface);border-color:var(--surface)}.note{padding:20px 24px;background:var(--surface);border-radius:9px;font-size:16px}.warning{border-left:3px solid var(--warning);background:var(--warning-soft)}.secondary{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:24px}.secondary a{border-top:1px solid var(--line);padding:18px 0;text-decoration:none;font-size:17px}.secondary span{display:block;color:var(--muted);font-size:14px}.footer{border-top:1px solid var(--line);padding:26px 28px;max-width:1160px;margin:auto;display:flex;justify-content:space-between;gap:24px;color:var(--muted);font-size:14px}.footer-links{display:flex;flex-wrap:wrap;gap:18px}.footer a{color:var(--muted)}.layout{display:grid;grid-template-columns:230px minmax(0,740px);gap:64px}.toc{font-size:15px;position:sticky;top:24px;align-self:start}.toc a{display:block;margin:14px 0;color:var(--muted);text-decoration:none}.toc a:hover{color:var(--primary)}.back{font-size:14px;display:inline-block;margin-bottom:24px;text-decoration:none}.step{padding:32px 0;border-bottom:1px solid var(--line);scroll-margin-top:24px}.step h2{display:flex;gap:18px;font-size:25px}.step h2 span{color:var(--primary);font:16px monospace;padding-top:6px}.check{font-size:16px;color:var(--muted);background:var(--surface);padding:16px 20px;border-radius:8px}.check strong{display:block;color:var(--ink)}.meta{font-size:14px;color:var(--muted)}.next{display:block;margin-top:32px;padding:24px;background:var(--surface);border-radius:10px;text-decoration:none}.sources{font-size:15px;margin-top:32px}.sources a{display:block;margin:7px 0}details{border-bottom:1px solid var(--line);padding:18px 0}summary{cursor:pointer;font-weight:600}details p{color:var(--muted);font-size:17px}.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:10px;background:white;z-index:2}@media(max-width:760px){nav{padding:18px 20px;flex-wrap:wrap}.brand{font-size:18px}nav .links{width:100%;justify-content:space-between;gap:10px;font-size:14px}main{padding:32px 20px 48px}.grid,.secondary,.layout{grid-template-columns:1fr}.layout{gap:20px}.toc{position:static;background:var(--surface);padding:16px 20px;border-radius:9px}.toc a{margin:8px 0}h1{letter-spacing:-.8px}.card{padding:22px}.footer{flex-direction:column;gap:10px}.footer-links{gap:12px 18px}.secondary{gap:0}}
'''
css+='''.journey-nav{margin-top:64px;padding-top:34px;border-top:1px solid var(--line)}.journey-head{margin-bottom:18px}.journey-head h2{margin:6px 0 0}.journey-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.journey-step{display:block;min-width:0;padding:16px;border:1px solid var(--line);border-radius:10px;color:var(--ink);text-decoration:none}.journey-step:hover{border-color:var(--primary);background:var(--surface)}.journey-step small{display:block;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em}.journey-step strong{display:block;margin-top:5px;font-size:15px;line-height:1.35}.journey-step[aria-current="step"]{border-color:var(--primary);background:var(--surface)}.journey-step[aria-current="step"] small{color:var(--primary)}@media(max-width:900px){.journey-steps{grid-template-columns:repeat(2,1fr)}}@media(max-width:500px){.journey-steps{grid-template-columns:1fr}nav .links{justify-content:flex-start;flex-wrap:wrap;column-gap:18px;row-gap:8px}}'''
css+='''.journey-nav{display:block;max-width:none;padding:34px 0 0;align-items:initial;justify-content:initial;gap:0}.articles-page{max-width:900px}.article-list{display:grid;gap:16px;margin:34px 0}.article-card{display:block;border:1px solid var(--line);border-radius:12px;padding:26px 28px;color:var(--ink);text-decoration:none}.article-card:hover{border-color:var(--primary);background:var(--surface)}.article-card h2{margin:7px 0 10px;font-size:26px}.article-card p{margin:0;color:var(--muted)}.article-meta{font-size:14px;color:var(--muted)}.article-body{max-width:760px;margin:auto}.article-body .lead{font-size:21px;line-height:1.55;color:var(--muted)}.article-summary{margin:28px 0;padding:20px 22px;border-left:4px solid var(--primary);background:var(--surface)}.article-summary p{margin:6px 0 0}.article-body h2{margin-top:46px}.article-body .sources{margin-top:48px;padding-top:28px;border-top:1px solid var(--line)}.article-body .related{margin-top:40px;padding:24px;background:var(--surface);border-radius:10px}.article-body .related a{display:block;margin:9px 0}@media(max-width:760px){nav .links{flex-wrap:wrap;justify-content:flex-start}.article-card{padding:22px}.article-body .lead{font-size:19px}}'''
css+='''.article-cover{margin:24px 0 30px}.article-cover img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:12px}.article-cover figcaption{margin-top:8px;color:var(--muted);font-size:14px}'''
(D/'style.css').write_text(css)
(D/'theme.css').write_text((Path(__file__).parent/'theme.css').read_text())
THEME_VERSION=hashlib.sha256((D/'theme.css').read_bytes()).hexdigest()[:12]
STYLE_VERSION=hashlib.sha256((D/'style.css').read_bytes()).hexdigest()[:12]
(D/'fonts').mkdir(exist_ok=True)
for font_file in (Path(__file__).parent/'fonts').glob('*'):
 if font_file.is_file():
  shutil.copy2(font_file,D/'fonts'/font_file.name)
(D/'assets').mkdir(parents=True,exist_ok=True)
ARTICLES={'articles/kak-poyavilas-kriptovalyuta':{'cover':'crypto-origins.svg','published':'2026-10-01'},'articles/seti-usdt-trc20-erc20':{'cover':'usdt-networks.svg','published':'2026-10-21'},'articles/zamorozka-usdt':{'cover':'usdt-freeze.svg','published':'2026-11-06'}}
for asset_file in ('csg-logo.svg',*(a['cover'] for a in ARTICLES.values())):
 shutil.copy2(Path(__file__).parent/'assets'/asset_file,D/'assets'/asset_file)
# Open Graph previews are pre-built by scripts/build_og_images.py and committed.
(D/'assets'/'og').mkdir(exist_ok=True)
for og_file in (Path(__file__).parent/'assets'/'og').glob('*.png'):
 shutil.copy2(og_file,D/'assets'/'og'/og_file.name)
def og_image_path(slug):
 name=slug.replace('/','-') or 'home'
 if not (Path(__file__).parent/'assets'/'og'/f'{name}.png').exists():
  name='where-to-buy'
 return f"/assets/og/{name}.png"
def page_url(slug):
 return f'{BASE_URL}/{slug}/' if slug else f'{BASE_URL}/'
import re
GLOSSARY_SOURCE=(Path(__file__).parent/'english-terms-page.html').read_text(encoding='utf-8')
def glossary_entries():
 entries=[]
 for m in re.finditer(r'<dt id="term-([a-z0-9-]+)">(.*?)</dt>\s*<dd>(.*?)</dd>',GLOSSARY_SOURCE,re.S):
  clean=lambda x:html.unescape(re.sub(r'<[^>]+>','',x)).strip()
  entries.append((m.group(1),clean(m.group(2)),clean(m.group(3))))
 return entries
def glossary_graph(url):
 set_id=f'{url}#glossary'
 return {'@type':'DefinedTermSet','@id':set_id,'name':'Криптословарь','inLanguage':'ru','url':url,'hasDefinedTerm':[{'@type':'DefinedTerm','@id':f'{url}#term-{i}','name':name,'description':text,'url':f'{url}#term-{i}','inDefinedTermSet':{'@id':set_id}} for i,name,text in glossary_entries()]}
# Автоссылки на словарь: первое вхождение термина на странице, только в тексте абзацев и списков.
# Только безопасные термины с однозначным смыслом; ссылки, заголовки, кнопки, скрипты и стили не трогаются.
AUTO_TERMS=[
 ('blockchain',r'блокчейн(?:а|у|е|ом|ы|ов)?',re.I),
 ('stablecoin',r'стейблкоин(?:а|у|е|ом|ы|ов)?',re.I),
 ('smart-contract',r'смарт-контракт(?:а|у|е|ом|ы|ов)?',re.I),
 ('private-key',r'приватн(?:ый|ого|ому|ым|ом) ключ(?:а|у|ом|е)?',re.I),
 ('seed',r'секретн(?:ая|ую|ой) фраз(?:а|у|ы|е|ой)',re.I),
 ('network-fee',r'комисси(?:я|ю|и|ей|ям) сети',re.I),
 ('kyc',r'KYC',0),('2fa',r'2FA',0),('p2p',r'P2P',0),('iban',r'IBAN',0),('sepa',r'SEPA',0),
 ('txid',r'TxID|TXID',0),('trc20',r'TRC-20',0),('erc20',r'ERC-20',0),('mica',r'MiCAR?',0),('afsa',r'AFSA',0),('casp',r'CASP',0),
]
AUTO_TERM_RES=[(i,re.compile(r'(?<![\w-])(?:'+pat+r')(?![\w-])',flags)) for i,pat,flags in AUTO_TERMS]
# Страницы с текстом из JSON маршрутов (проверяется дословно валидаторами) не обрабатываются.
AUTO_TERM_PAGES={'','start','wallet','usdt','bitcoin','buy','transfer','about','articles','legal','privacy','articles/kak-poyavilas-kriptovalyuta','articles/seti-usdt-trc20-erc20','articles/zamorozka-usdt'}
RAW_TAGS={'script','style'}
SKIP_TAGS={'a','h1','h2','h3','h4','h5','h6','button','summary','label','option','select','textarea','code','pre','nav','title','dt'}
ALLOW_TAGS={'p','li','dd','td'}
VOID_TAGS={'br','img','input','meta','link','hr','source','wbr'}
def link_terms(body):
 done={i for i,_ in AUTO_TERM_RES if f'href="/english-terms/#term-{i}"' in body}
 out=[];raw=None;skip={};allow={}
 for token in re.split(r'(<[^>]+>)',body):
  if token.startswith('<') and token.endswith('>'):
   m=re.match(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)',token)
   if m:
    closing,name=m.group(1)=='/',m.group(2).lower()
    if raw:
     if closing and name==raw: raw=None
    elif not closing and name in RAW_TAGS and not token.endswith('/>'):
     raw=name
    elif name in VOID_TAGS or token.endswith('/>'):
     pass
    else:
     for table,names in ((skip,SKIP_TAGS),(allow,ALLOW_TAGS)):
      if name in names:
       table[name]=max(0,table.get(name,0)+(-1 if closing else 1))
   out.append(token);continue
  if raw or any(skip.values()) or not any(allow.values()) or not token.strip():
   out.append(token);continue
  for term_id,regex in AUTO_TERM_RES:
   if term_id in done: continue
   m=regex.search(token)
   if m:
    token=token[:m.start()]+f'<a class="en-term" href="/english-terms/#term-{term_id}">{m.group(0)}</a>'+token[m.end():]
    done.add(term_id)
  out.append(token)
 return ''.join(out)
def structured_data(title,desc,slug):
 url=page_url(slug)
 page_type='Article' if slug.startswith('articles/') else (['WebPage','AboutPage'] if slug=='about' else 'WebPage')
 published=ARTICLES[slug]['published'] if slug in ARTICLES else PUBLISHED
 graph=[
  {'@type':'Organization','@id':f'{BASE_URL}/#publisher','name':'Crypto Step Guide','url':f'{BASE_URL}/','logo':f'{BASE_URL}/assets/csg-logo.svg','email':'hello@crypto-step-guide.com','description':'Информационно-образовательный проект: понятные инструкции по покупке, хранению и переводу криптовалюты для начинающих. Сайт бесплатный, не принимает платежи и не оказывает финансовых услуг.'},
  {'@type':'WebSite','@id':f'{BASE_URL}/#website','url':f'{BASE_URL}/','name':'Crypto Step Guide','description':'Понятные инструкции по покупке, хранению и переводу криптовалюты для начинающих.','inLanguage':'ru','isAccessibleForFree':True,'publisher':{'@id':f'{BASE_URL}/#publisher'}},
  {'@type':page_type,'@id':f'{url}#webpage','url':url,'name':title,'headline':title if slug.startswith('articles/') else None,'description':desc,'inLanguage':'ru','isPartOf':{'@id':f'{BASE_URL}/#website'},'publisher':{'@id':f'{BASE_URL}/#publisher'},'isAccessibleForFree':True,'datePublished':published,'dateModified':MODIFIED.get(slug,UPDATED)}
 ]
 if slug in ARTICLES:
  graph[2]['image']=[f'{BASE_URL}{og_image_path(slug)}',f'{BASE_URL}/assets/{ARTICLES[slug]["cover"]}']
 graph[2]={k:v for k,v in graph[2].items() if v is not None}
 if slug=='english-terms':
  graph.append(glossary_graph(url))
 if slug:
  crumbs=[{'@type':'ListItem','position':1,'name':'Crypto Step Guide','item':f'{BASE_URL}/'}]
  if slug.startswith('articles/'):
   crumbs.append({'@type':'ListItem','position':2,'name':'Статьи','item':f'{BASE_URL}/articles/'})
   crumbs.append({'@type':'ListItem','position':3,'name':title,'item':url})
  else:
   crumbs.append({'@type':'ListItem','position':2,'name':title,'item':url})
  graph.append({'@type':'BreadcrumbList','@id':f'{url}#breadcrumb','itemListElement':crumbs})
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'))
def journey(slug):
 items=[('start','Шаг 1','Разобраться с основами'),('wallet','Шаг 2','Выбрать кошелёк'),('buy','Шаг 3','Подготовить покупку'),('transfer','Шаг 4','Подготовить перевод')]
 current={'usdt':'start','bitcoin':'start','articles':'start','articles/kak-poyavilas-kriptovalyuta':'start','articles/seti-usdt-trc20-erc20':'start','articles/zamorozka-usdt':'transfer','where-to-buy':'buy','buy-bank-transfer':'buy','buy-local-p2p':'buy','buy-usdt':'buy','service-status':'buy','sell-usdt':'transfer'}.get(slug,slug)
 links=''.join(f'<a class="journey-step" href="/{item_slug}/"'+(' aria-current="step"' if item_slug==current else '')+f'><small>{number}</small><strong>{label}</strong></a>' for item_slug,number,label in items)
 return f'<nav class="journey-nav" aria-label="Путь по разделам"><div class="journey-head"><span class="eyebrow">Путь по шагам</span><h2>Выберите следующий раздел</h2></div><div class="journey-steps">{links}</div></nav>'
def shell(title,desc,body,slug='',not_found=False):
 url=page_url(slug)
 if not_found:
  # Served by Cloudflare Pages with HTTP 404 for unknown paths: no canonical, not indexable, not in sitemap.
  full_title=f'{title} · Crypto Step Guide'
  head_meta=f'<meta name="robots" content="noindex,follow">'
 else:
  seo=SEO_CONTENT['pages'][slug]
  if slug in AUTO_TERM_PAGES:
   body=link_terms(body)
  title=seo['content_title']
  desc=seo['description']
  seo_title=seo['title']
  full_title=seo_title if 'Crypto Step Guide' in seo_title else f'{seo_title} · Crypto Step Guide'
  schema=structured_data(title,desc,slug)
  og_type='article' if slug.startswith('articles/') else 'website'
  og_height=675 if slug in ARTICLES else 630
  og_image=f'<meta property="og:image" content="{BASE_URL}{og_image_path(slug)}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="{og_height}"><meta property="og:image:alt" content="{html.escape(title)}">'
  head_meta=f'''<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="ru" href="{url}"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Crypto Step Guide"><meta property="og:title" content="{html.escape(full_title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}">{og_image}<meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">{schema}</script>'''
 return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(full_title)}</title><meta name="description" content="{html.escape(desc)}"><meta name="theme-color" content="#f7f5ef">{head_meta}<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="preload" href="/fonts/commissioner-cyrillic-wght-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/literata-cyrillic-wght-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/style.css?v={STYLE_VERSION}"><link rel="stylesheet" href="/theme.css?v={THEME_VERSION}"></head><body><a class="skip" href="#main">Перейти к содержанию</a><header><nav aria-label="Основная навигация"><a class="brand" href="/"><b>CSG</b><span>Crypto Step Guide</span></a><div class="links"><a href="/start/">Начать с основ</a><a href="/buy/">Как купить</a><a href="/sell-usdt/">Как продать</a><a href="/english-terms/">Криптословарь</a><a href="/articles/">Статьи</a><a href="/about/">О проекте</a></div></nav></header><main id="main">{body}{journey(slug) if slug and not not_found else ''}</main><footer class="footer"><span>Crypto Step Guide · Справочник для начинающих</span><span class="footer-links"><a href="/articles/">Статьи</a><a href="/english-terms/">Криптословарь</a><a href="/about/">О проекте</a><a href="/service-status/">Проверка сервисов</a><a href="/legal/">Правовая информация</a><a href="/privacy/">Конфиденциальность</a><a href="/es/" lang="es" hreflang="es">Español</a><a href="/pt/" lang="pt" hreflang="pt">Português</a><a href="/en/" lang="en" hreflang="en">English</a></span></footer><link rel="stylesheet" href="/theme.css?v={THEME_VERSION}"></body></html>'''
def put(slug,title,desc,body):
 p=D/slug;p.mkdir(parents=True,exist_ok=True);(p/'index.html').write_text(shell(title,desc,body,slug).replace('>Источники и принципы<','>О проекте<'))
home='''<div class="eyebrow">Информационно-образовательный проект</div><h1>Криптовалюта простыми словами</h1><p class="intro">Crypto Step Guide помогает начинающим разобраться в криптовалюте и предоставляет информационные и образовательные материалы.</p><p>Объясняем, как работают криптовалюты, кошельки и переводы, чем отличаются сети и какие риски важно учитывать. Помогаем разобраться в доступных способах покупки и продажи криптовалюты с учётом страны и условий сервисов.</p><h2>Что вы хотите сделать?</h2><p>Для подбора вариантов покупки USDT выберите страну и способ оплаты в форме ниже. Если сначала хотите разобраться в теме, откройте раздел «Разобраться с нуля». Для Украины и Беларуси маршруты имеют условный статус и требуют дополнительных проверок.</p>__HOME_ROUTE_FORM__<section class="grid" id="guides" aria-label="Выбор задачи"><a class="card start" href="/start/"><h2>Разобраться с нуля</h2><p>Понять, что такое криптовалюта, зачем она нужна и какие бывают виды.</p></a><a class="card" href="/wallet/"><h2>Выбрать кошелёк</h2><p>Выбрать способ хранения и защитить доступ.</p></a><a class="card" href="/buy/"><h2>Купить криптовалюту</h2><p>Разобраться в порядке покупки и расходах.</p></a><a class="card" href="/transfer/"><h2>Перевести криптовалюту</h2><p>Проверить реквизиты перед отправкой.</p></a></section><aside class="note warning"><strong>Перед первым переводом</strong><br>Никому не передавайте секретную фразу кошелька. Проверяйте адрес и сеть до отправки: перевод часто нельзя отменить.</aside><section style="margin-top:48px"><div class="eyebrow">Отдельные задачи</div><div class="secondary"><a href="/usdt/">Что такое USDT<span>Зачем нужен и чем отличается от доллара</span></a><a href="/service-status/">Проверка сервисов<span>Операторы, источники и дата проверки</span></a></div></section>'''
wizard_source=(Path(__file__).parent/'buy-usdt-page.html').read_text(encoding='utf-8')
route_markup=json.dumps({k:v for k,v in ROUTE_CONTENT.items() if k!='language_variants'},ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
wizard_markup=json.dumps(WIZARD_CONTENT,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
flow=wizard_source[wizard_source.index('  <section class="flow"'):wizard_source.index('<details class="route-reference"')]
extras=wizard_source[wizard_source.index('<section class="calculator"'):wizard_source.index('  <p class="meta">Сайт не принимает оплату')]
script=wizard_source[wizard_source.index('<script type="application/json" id="route-data">'):]
component=wizard_source[:wizard_source.index('</style>')+8]+flow+extras+script
component=component.replace('__ROUTE_DATA_JSON__',route_markup).replace('__WIZARD_DATA_JSON__',wizard_markup)
home=home.replace('__HOME_ROUTE_FORM__',component)
(D/'index.html').write_text(shell('Криптовалюта простыми словами: покупка, кошельки и переводы','Понятные инструкции для начинающих: что такое криптовалюта, где её купить, как выбрать кошелёк и проверить перевод перед подтверждением.',home).replace('>Источники и принципы<','>О проекте<'))
next_labels={p[0]:p[1] for p in pages}
next_labels['buy-usdt']='Купить USDT: полный маршрут'
for slug,label,title,desc,category,steps,nxt in pages:
 toc=''.join(f'<a href="#step-{i}">{i:02d} {s[0]}</a>' for i,s in enumerate(steps,1))
 body=f'<a class="back" href="/">← Все инструкции</a><div class="layout"><aside class="toc"><strong>В этой инструкции</strong>{toc}</aside><article><div class="eyebrow">{category} · {len(steps)} шага</div><h1>{title}</h1><p class="intro">{desc}</p><p class="meta">Общая инструкция · условия конкретного сервиса проверяйте перед операцией</p>'
 for i,(head,txt,check) in enumerate(steps,1):
  body+=f'<section class="step" id="step-{i}"><h2><span>{i:02d}</span>{head}</h2><p>{txt}</p><div class="check"><strong>Что проверить</strong>{check}</div></section>'
 source={'usdt':('https://tether.to/en/faqs/','Tether: описание USDT и условия эмитента'),'wallet':('https://ethereum.org/ru/wallets/','Ethereum.org: принципы работы кошельков')}.get(slug,('https://bitcoin.org/ru/getting-started','Bitcoin.org: начало работы с Bitcoin'))
 body+=f'<details><summary>Что такое секретная фраза?</summary><p>Это набор слов для восстановления доступа в некоторых самостоятельных кошельках. Любой человек, получивший эту фразу, может получить контроль над средствами. Для проверки перевода достаточно публичного адреса или TxID; запрос секретной фразы означает попытку получить доступ к кошельку.</p></details><div class="sources"><strong>Для проверки и дальнейшего чтения</strong><a href="{source[0]}" target="_blank" rel="noopener noreferrer">{source[1]} ↗</a><span>Источник относится к теме «{"USDT" if slug=="usdt" else "кошельки Ethereum" if slug=="wallet" else "Bitcoin"}». Условия конкретной площадки проверяются отдельно.</span></div><a class="next" href="/{nxt}/">Следующий материал<br><strong>{next_labels[nxt]} →</strong></a></article></div>'
 put(slug,title,desc,body)
put('about','О проекте Crypto Step Guide: методика и источники','Как мы проверяем сервисы, обновляем инструкции и отделяем редакционный выбор от партнёрской монетизации.','''<a class="back" href="/">← На главную</a><article style="max-width:740px"><div class="eyebrow">О справочнике</div><h1>Как мы готовим инструкции</h1><p>Crypto Step Guide – русскоязычный справочник для людей, которые только знакомятся с криптовалютой.</p></article>''')
# Dedicated first-purchase guide; preserved when regenerating the site.
put('buy','Как купить криптовалюту: первые шаги','Понятные шаги перед первой покупкой: цель, правила страны, сервис, кошелёк, сеть и полная стоимость.',(Path(__file__).parent/'buy-page.html').read_text())
def route_summary_html(countries=None,heading='h3',page_link=True):
  esc=lambda v:html.escape(str(v),quote=True)
  out=[]
  for country in (countries or ['ukraine','belarus','kazakhstan','kyrgyzstan','uzbekistan','serbia','russia']):
    cfg=WIZARD_CONTENT['countries'][country];routes=[r for r in ROUTE_CONTENT['routes_by_country'][country] if r['status']!='blocked']
    cards=[]
    if cfg.get('no_route'):
      no=cfg['no_route']
      sources=''.join(f'<a class="source-link" href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">{esc(x["label"])} ↗</a>' for x in no['sources'])
      checks=''.join(f'<li>{esc(x)}</li>' for x in no['next_steps'])
      cards.append(f'<article class="service-card"><div class="service-top"><h4>{esc(no["title"])}</h4><span class="status status-conditional">Проверка</span></div><p class="service-summary">{esc(no["message"])}</p><ul class="checks">{checks}</ul><details><summary>Проверенные официальные источники</summary>{sources}</details><a class="next-link" href="/buy-usdt/#country={country}">Открыть статус проверки →</a></article>')
    for r in routes:
      exchange_only=r.get('wallet_withdrawal_blocked') or r.get('allowed_destinations')==['exchange']
      end='Баланс сервиса – вывод в личный кошелёк не предлагается' if exchange_only else 'Личный кошелёк'+(f' ({r["network"]})' if r.get('network') else '')
      status='conditional' if r['status']=='conditional' else 'documented'
      sources=''.join(f'<a class="source-link" href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">{esc(x["label"])} ↗</a>' for x in r['sources'])
      cards.append(f'<article class="service-card"><div class="service-top"><h4>{esc(r["service"])}</h4><span class="status status-{status}">{esc(r["label"])}</span></div><p class="service-summary">{esc(r["payment"])}</p><div class="facts"><div class="fact"><strong>Валюта</strong> {esc(r["currency"])}</div><div class="fact"><strong>Где закончится</strong> {esc(end)}</div><div class="fact"><strong>Проверено</strong> {esc(r["last_source_reviewed"])}</div></div><details><summary>Официальные источники по этапам</summary>{sources}</details><a class="next-link" href="/buy-usdt/#country={country}&amp;route={esc(r["id"])}">Открыть пошаговый план →</a></article>')
    notes=''.join(f'<p class="finder-note"><strong>{esc(pay["title"])}:</strong> {esc(pay["message"])}</p>' for pay in cfg['payments'] if pay.get('route') is None and not pay.get('choices') and pay.get('message'))
    country_link=f'<p><a class="next-link" href="/buy-usdt-{country}/">Страница страны: правовая основа и реестры →</a></p>' if page_link else ''
    out.append(f'<div class="country-block" id="{country}"><{heading}>{esc(cfg["label"])}</{heading}>{country_link}<div class="service-list">{"".join(cards)}</div>{notes}</div>')
  return ''.join(out)
where_to_buy_body=(Path(__file__).parent/'where-to-buy-page.html').read_text(encoding='utf-8').replace('__ROUTE_SUMMARY_HTML__',route_summary_html())
put('where-to-buy','Где купить USDT: маршруты и статус проверки по странам','18 условных и документированных сценариев в семи странах. Для Украины и Беларуси показаны официальные маршруты с проверками аккаунта, оплаты и правовой применимости.',where_to_buy_body)
SELL_COUNTRIES=['kazakhstan','kyrgyzstan','uzbekistan','russia','ukraine','belarus','serbia']
def sell_routes_html():
  esc=lambda v:html.escape(str(v),quote=True)
  out=[]
  for country in SELL_COUNTRIES:
    cfg=SELL_CONTENT['countries'][country];cards=[]
    for r in cfg['routes']:
      status='documented' if r['status']=='ready' else 'conditional'
      steps=''.join(f'<li>{esc(x)}</li>' for x in r['steps'])
      checks=''.join(f'<li>{esc(x)}</li>' for x in r['checks_before_sale'])
      sources=''.join(f'<a class="source-link" href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">{esc(x["label"])} ↗</a>' for x in r['sources'])
      cards.append(f'<article class="service-card" id="{esc(r["id"])}"><div class="service-top"><h4>{esc(r["service"])}</h4><span class="status status-{status}">{esc(r["label"])}</span></div><p class="service-summary">{esc(r["payout"])}</p><div class="facts"><div class="fact"><strong>Валюта</strong> {esc(r["currency"])}</div><div class="fact"><strong>Тип</strong> {esc({"exchange":"Биржа","exchanger":"Обменник","p2p":"P2P-сделка"}[r["method"]])}</div><div class="fact"><strong>Проверено</strong> {esc(r["last_source_reviewed"])}</div></div><strong>Проверьте до продажи</strong><ul class="checks">{checks}</ul><details><summary>Пошагово</summary><ol class="sell-steps">{steps}</ol><p class="scope">{esc(r["evidence_scope"])}</p></details><details><summary>Официальные источники</summary>{sources}</details></article>')
    notice=f'<div class="caution" role="note"><strong>Важно</strong><p>{esc(cfg["legal_notice"])}</p></div>' if cfg.get('legal_notice') else ''
    empty=f'<p class="finder-note">{esc(cfg["no_route"])}</p>' if cfg.get('no_route') else ''
    out.append(f'<div class="country-block" id="sell-{country}"><h3>{esc(cfg["label"])}</h3>{notice}<div class="service-list">{"".join(cards)}</div>{empty}</div>')
  return ''.join(out)
def sell_country_nav():
  return ''.join(f'<a href="#sell-{c}">{html.escape(SELL_CONTENT["countries"][c]["label"])}</a>' for c in SELL_COUNTRIES)
sell_body=(Path(__file__).parent/'sell-usdt-page.html').read_text(encoding='utf-8').replace('__SELL_ROUTES_HTML__',sell_routes_html()).replace('__SELL_COUNTRY_NAV__',sell_country_nav())
put('sell-usdt','Как продать USDT и вывести деньги на карту','Как продать USDT и вывести деньги на свою карту или счёт: биржа, лицензированный обменник и P2P по странам, комиссии, лимиты и риски.',sell_body)
put('buy-usdt-kazakhstan-card','Как купить USDT в Казахстане с банковской карты','Сравнение покупки USDT с Mastercard через Binance Kazakhstan и собственной карты через AUSU: требования, стоимость, сеть и маршрут до личного кошелька.',(Path(__file__).parent/'buy-kazakhstan-card-page.html').read_text(encoding='utf-8'))
put('buy-usdt-shymkent-cash','Как купить USDT за наличные в Шымкенте','Маршрут AUSU с наличной оплатой в кассе Шымкента: адрес, часы, онлайн-проверка личности, минимум 25 000 тенге и перевод USDT TRON на личный кошелёк.',(Path(__file__).parent/'buy-shymkent-cash-page.html').read_text(encoding='utf-8'))
put('buy-usdt-uzbekistan-card','Как купить USDT в Узбекистане через Paynet, Uzcard или HUMO','Пошаговая инструкция CityPay: покупка USDT в сумах через Paynet, Uzcard или HUMO, комиссия, KYC, лимиты и внешний перевод на личный кошелёк.',(Path(__file__).parent/'buy-uzbekistan-card-page.html').read_text(encoding='utf-8'))
put('buy-usdt-tashkent-cash','Как купить USDT за наличные в Ташкенте','Маршрут Voluto: наличные сумы или доллары США в офисе на Labzak 2A, минимальная сумма 200 USDT, требования к документам и перевод USDT TRC-20 в кошелёк.',(Path(__file__).parent/'buy-tashkent-cash-page.html').read_text(encoding='utf-8'))
put('buy-usdt-serbia-bank','Как купить USDT в Сербии банковским переводом','Маршрут ECD Wallet: перевод RSD, покупка USDT, комиссии и требования к иностранцам с проживанием в Сербии.',(Path(__file__).parent/'buy-usdt-serbia-bank-page.html').read_text(encoding='utf-8'))
put('buy-usdt-serbia-crypto-atm','Как купить USDT в Сербии за наличные в криптомате','Локации ECD в Белграде и Нови-Саде, минимум 1 000 RSD, комиссия 6,2% + 500 RSD и покупка USDT ERC-20.',(Path(__file__).parent/'buy-usdt-serbia-crypto-atm-page.html').read_text(encoding='utf-8'))
put('buy-bank-transfer','Как купить криптовалюту банковским переводом','Проверенные и исследуемые маршруты покупки без карты с указанием юридического лица, условий и причин исключения.',(Path(__file__).parent/'bank-transfer-page.html').read_text())
put('buy-local-p2p','Местная оплата и P2P для покупки USDT','Сравнение местных способов покупки USDT в России, Казахстане и Узбекистане и правила проверки P2P.',(Path(__file__).parent/'local-p2p-page.html').read_text())
put('start','Что такое криптовалюта простыми словами','Что такое криптовалюта, зачем она нужна, какие бывают виды и что проверить перед первой операцией.',(Path(__file__).parent/'start-page.html').read_text())
put('wallet','Какой криптокошелёк выбрать','Сравнение кошельков для Bitcoin и USDT: сети, восстановление, комиссии и безопасность.',(Path(__file__).parent/'wallet-page.html').read_text())
put('transfer','Как вывести USDT с биржи в личный кошелёк','Пошаговая инструкция вывода USDT: как получить адрес, выбрать одинаковую сеть, проверить комиссию, TxID и поступление в кошелёк.',(Path(__file__).parent/'transfer-page.html').read_text())
route_data={k:v for k,v in ROUTE_CONTENT.items() if k!='language_variants'}  # языковые варианты в мастер не попадают
route_markup=json.dumps(route_data,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
wizard_markup=json.dumps(WIZARD_CONTENT,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
buy_usdt_body=(Path(__file__).parent/'buy-usdt-page.html').read_text(encoding='utf-8').replace('__ROUTE_DATA_JSON__',route_markup).replace('__WIZARD_DATA_JSON__',wizard_markup)
put('buy-usdt','Как купить USDT: маршрут и калькулятор полной стоимости','Выберите страну и способ оплаты, рассчитайте полную стоимость покупки и узнайте, сколько USDT поступит в личный кошелёк после комиссии вывода.',buy_usdt_body)
put('about','О проекте Crypto Step Guide','Для кого создан сервис, откуда берётся информация и как проверяются маршруты покупки, хранения и перевода криптовалюты.',(Path(__file__).parent/'about-page.html').read_text())
put('legal','Правовая информация','Роль сайта, границы информационных материалов, правила сравнения сервисов и раскрытие партнёрских отношений.',(Path(__file__).parent/'legal-page.html').read_text())
put('privacy','Конфиденциальность','Какие данные не запрашивает сайт, как работают внешние ссылки и что изменится при подключении аналитики или партнёрского отслеживания.',(Path(__file__).parent/'privacy-page.html').read_text())
put('service-status','Проверка сервисов для покупки USDT','18 сценариев в семи странах, включая условные маршруты Украины и Беларуси; официальные источники, ограничения и недостающие проверки.',(Path(__file__).parent/'service-status-page.html').read_text())
put('english-terms','Криптословарь: понятия, сокращения и кнопки','Простые объяснения криптовалютных понятий, сокращений и английских надписей, которые встречаются на биржах и в кошельках.',(Path(__file__).parent/'english-terms-page.html').read_text())
put('articles','Статьи о криптовалюте простыми словами','Разбираем устройство криптовалюты, Bitcoin, USDT, кошельки, сети и покупку без лишних технических подробностей.',(Path(__file__).parent/'articles-page.html').read_text())
put('articles/kak-poyavilas-kriptovalyuta','Как появилась криптовалюта и почему Bitcoin оказался только началом','Как появилась криптовалюта простыми словами: зачем создали Bitcoin, почему появились Ethereum, токены, USDT и другие стейблкоины.',(Path(__file__).parent/'article-crypto-origin-page.html').read_text())
put('articles/seti-usdt-trc20-erc20','Почему у USDT несколько сетей и как выбрать нужную','Чем TRC-20 отличается от ERC-20 и BEP-20, кто берёт комиссию за перевод USDT и что будет, если выбрать не ту сеть.',(Path(__file__).parent/'article-usdt-networks-page.html').read_text())
put('articles/zamorozka-usdt','Может ли Tether заморозить ваши USDT','Почему у USDT есть блокировка, за что Tether замораживает адреса, что такое «грязные» USDT и как снизить риск задержки перевода.',(Path(__file__).parent/'article-usdt-freeze-page.html').read_text(encoding='utf-8'))

# Cloudflare Pages serves a top-level 404.html with HTTP 404 for unknown paths (without it every path returns the home page with 200).
not_found_body='''<div class="eyebrow">Ошибка 404</div><h1>Такой страницы нет</h1><p class="intro">Возможно, ссылка устарела или в адресе опечатка. Выберите нужный раздел или начните с главной.</p><section class="grid" aria-label="Основные разделы"><a class="card start" href="/"><h2>Главная</h2><p>Подобрать маршрут покупки USDT по стране и способу оплаты.</p></a><a class="card" href="/start/"><h2>Разобраться с нуля</h2><p>Что такое криптовалюта и что проверить перед первой операцией.</p></a><a class="card" href="/buy/"><h2>Купить криптовалюту</h2><p>Порядок первой покупки и полная стоимость.</p></a><a class="card" href="/transfer/"><h2>Перевести криптовалюту</h2><p>Адрес, сеть и комиссия перед отправкой.</p></a></section>'''
(D/'404.html').write_text(shell('Страница не найдена','Такой страницы нет на Crypto Step Guide. Перейдите на главную или в основные разделы справочника.',not_found_body,not_found=True))

# Страницы стран: данные маршрутов и уведомления берутся из content/*.json; правовая основа — из SERVICE-LEGAL-REGISTRY.md.
COUNTRY_PAGES={
 'kazakhstan':{'slug':'buy-usdt-kazakhstan','in':'Казахстане','intro':'Покупка и обмен цифровых активов в Казахстане регулируются Законом № 193-VII «О цифровых активах». Услуги вправе оказывать провайдеры с лицензией Национального Банка РК или участники МФЦА с лицензией AFSA, поэтому перед оплатой проверьте юридическое лицо в реестре.','basis':[('Закон РК № 193-VII «О цифровых активах в Республике Казахстан» (adilet.zan.kz)','https://adilet.zan.kz/rus/docs/Z2300000193'),('Реестр лицензий AFSA (МФЦА)','https://publicreg.myafsa.com/dasp/?sort=license_number'),('Национальный Банк РК: операторы обмена необеспеченных цифровых активов','https://nationalbank.kz/ru/page/unsecured-asset-exchange-operators')],'related':[('buy-usdt-kazakhstan-card','Карта: Binance Kazakhstan или AUSU'),('buy-usdt-shymkent-cash','Наличные в Шымкенте (AUSU)')]},
 'belarus':{'slug':'buy-usdt-belarus','in':'Беларуси','intro':'В Беларуси покупка и продажа токенов за деньги разрешены только через резидентов Парка высоких технологий. Операции за деньги на зарубежных площадках и напрямую между физлицами Министерство по налогам и сборам считает запрещёнными.','basis':[('Указ Президента № 367 «Об обращении цифровых знаков (токенов)» от 17.09.2024 (pravo.by)','https://pravo.by/document/?guid=12551&p0=P32400367'),('Разъяснение МНС о порядке совершения и налогообложения операций с токенами (pravo.by, 20.01.2025)','https://pravo.by/novosti/analitika/2025/january/80298/'),('Реестр резидентов Парка высоких технологий','https://www.park.by/en/residents/')],'related':[]},
 'ukraine':{'slug':'buy-usdt-ukraine','in':'Украине','intro':'Для Украины в проекте описан один условный маршрут: P2P-сделка на Bybit. Применимость банковских правил НБУ, доступность объявления и выбранного банка проверяются до оплаты.','basis':[('НБУ, постановление № 18 о банковской деятельности в период военного положения','https://bank.gov.ua/admin_uploads/law/Resolution_24022022_18_kp.pdf')],'related':[]},
 'russia':{'slug':'buy-usdt-russia','in':'России','intro':'Банк России допускает прямые P2P-сделки между физлицами только до 01.07.2027, но считает недопустимым перевод со счёта физлица в собственный некастодиальный кошелёк. Поэтому для России показан ограниченный сценарий до баланса сервиса.','basis':[('Банк России: ответы о P2P, реестре и некастодиальном кошельке','https://www.cbr.ru/explan/cryptocurrency/'),('Банк России: реестр организаций обмена цифровых валют','https://www.cbr.ru/admissionfinmarket/register/'),('Федеральный закон № 282-ФЗ, статья 55 (КонсультантПлюс)','https://www.consultant.ru/document/cons_doc_LAW_540983/1ebbbb98154f5a1f6a5c766571fa997516489e90/')],'related':[('buy-local-p2p','Местная оплата и P2P: правила проверки')]},
 'kyrgyzstan':{'slug':'buy-usdt-kyrgyzstan','in':'Кыргызстане','intro':'В Кыргызстане в проекте описан условный маршрут через DantePay: лицензия оператора обмена виртуальных активов подтверждена в реестре Службы регулирования и надзора за финансовым рынком.','basis':[('Реестры Службы регулирования и надзора за финансовым рынком Кыргызстана','https://fsa.gov.kg/%d1%80%d0%b5%d0%b5%d1%81%d1%82%d1%80%d1%8b/?category_id=99&title_search=%D0%A1%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82')],'related':[]},
 'uzbekistan':{'slug':'buy-usdt-uzbekistan','in':'Узбекистане','intro':'В Узбекистане провайдеры проверяются по реестру лицензий NAPP. В проекте описаны три маршрута: Asterium, CityPay и наличные Voluto в Ташкенте; доступность зависит от профиля, документов и способа оплаты.','basis':[('NAPP: реестр лицензий провайдеров','https://napp.uz/ru/pages/erlsp')],'related':[('buy-usdt-uzbekistan-card','CityPay: Paynet, Uzcard или HUMO'),('buy-usdt-tashkent-cash','Наличные в Ташкенте (Voluto)')]},
 'serbia':{'slug':'buy-usdt-serbia','in':'Сербии','intro':'В Сербии оператор ECD (MCM 965 d.o.o.) внесён в реестр поставщиков услуг с виртуальными валютами Национального банка Сербии. Иностранцам для регистрации нужны паспорт, подтверждение проживания и личная верификация.','basis':[('Национальный банк Сербии: реестр MCM 965','https://www.nbs.rs/en/ciljevi-i-funkcije/nadzor-nad-finansijskim-institucijama/digital-imo/reg_di/reg_di_mcm/')],'related':[('buy-usdt-serbia-bank','Банковский перевод RSD'),('buy-usdt-serbia-crypto-atm','Наличные в криптомате')]},
}
COUNTRY_CSS="""<style>
.cpage .lead-box{margin:28px 0;padding:20px 24px;border-left:3px solid var(--primary);background:var(--surface);border-radius:8px}.cpage .lead-box p{margin:6px 0}
.cpage .route-list{list-style:none;margin:20px 0 0;padding:0;display:grid;gap:14px}.cpage .route-row{border:1px solid var(--line);border-radius:12px;padding:20px 22px;background:var(--surface)}
.cpage .route-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;flex-wrap:wrap}.cpage .route-row h3{margin:0;font-size:19px;line-height:1.4;max-width:34em}
.cpage .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:13px;font-weight:600;white-space:nowrap}.cpage .badge-ready{color:var(--safe);background:var(--safe-soft)}.cpage .badge-cond{color:var(--warning);background:var(--warning-soft)}
.cpage .route-meta{margin:10px 0 0;font-size:15px;color:var(--muted)}.cpage .route-meta b{color:var(--ink);font-weight:600}
.cpage .route-row details{border:0;padding:10px 0 0}.cpage .route-row summary{font-weight:600;font-size:15px}.cpage .route-row ul{margin:10px 0;padding-left:20px;font-size:15px}.cpage .route-row li{margin:6px 0}
.cpage .route-go{display:inline-block;margin-top:14px;padding:10px 16px;border-radius:8px;background:var(--button);color:var(--ink);text-decoration:none;font-weight:600;font-size:15px}.cpage .route-go:hover{background:var(--button-hover)}
.cpage .src a{display:block;margin:6px 0;font-size:15px}.cpage .legal-list{padding-left:20px}.cpage .legal-list li{margin:10px 0}
@media(max-width:760px){.cpage .route-row{padding:18px}.cpage .route-row h3{font-size:18px}}
</style>"""
def country_page_body(country):
  esc=lambda v:html.escape(str(v),quote=True)
  cfg=COUNTRY_PAGES[country];label=WIZARD_CONTENT['countries'][country]['label'];wz=WIZARD_CONTENT['countries'][country]
  routes=[r for r in ROUTE_CONTENT['routes_by_country'][country] if r['status']!='blocked']
  n=len(routes);reviewed=ROUTE_CONTENT['last_reviewed_on']
  ready=sum(1 for r in routes if r['status']!='conditional')
  def row(r):
    exch=r.get('wallet_withdrawal_blocked') or r.get('allowed_destinations')==['exchange']
    end='на баланс сервиса, вывод в личный кошелёк не предлагается' if exch else ('сразу на ваш личный кошелёк' if r.get('fixed_destination')=='personal_wallet' else 'на баланс сервиса, затем вывод на личный кошелёк')
    cond=r['status']=='conditional'
    checks=''.join(f'<li>{esc(c)}</li>' for c in r.get('checks_before_payment',[]))
    srcs=''.join(f'<a href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">{esc(x["label"])} ↗</a>' for x in r['sources'])
    return (f'<li class="route-row" id="{esc(r["id"])}"><div class="route-head"><h3>{esc(r["payment"])}</h3><span class="badge {"badge-cond" if cond else "badge-ready"}">{"Условно: проверить до оплаты" if cond else "Описан по официальным источникам"}</span></div>'
      f'<p class="route-meta"><b>Сервис:</b> {esc(r["service"])} · <b>Валюта:</b> {esc(r["currency"])} · <b>USDT приходят:</b> {end}</p>'
      f'<details><summary>Что проверить до оплаты</summary><ul>{checks}</ul><div class="src">{srcs}</div></details>'
      f'<a class="route-go" href="/buy-usdt/#country={country}&amp;route={esc(r["id"])}">Открыть пошаговый план →</a></li>')
  notes=''.join(f'<div class="note warning"><strong>{esc(pay["title"])}:</strong> {esc(pay["message"])}</div>' for pay in wz['payments'] if pay.get('route') is None and not pay.get('choices') and pay.get('message'))
  sell=SELL_CONTENT['countries'].get(country,{})
  notice=f'<div class="note warning" role="note"><strong>Важно при продаже USDT</strong><p>{esc(sell["legal_notice"])}</p></div>' if sell.get('legal_notice') else ''
  basis=''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{esc(t)} ↗</a></li>' for t,u in cfg['basis'])
  wallet_start=('Если кошелька ещё нет, мастер подскажет, как выбрать и подготовить его, а полный разбор есть на странице «Кошелёк». Маршруты с отправкой сразу на личный кошелёк потребуют его до оплаты.' if any(r.get('fixed_destination')=='personal_wallet' for r in routes) else 'Кошелёк можно подготовить позже: мастер покажет этот шаг в плане покупки.') if any(r.get('allowed_destinations')!=['exchange'] for r in routes) else 'В этой стране вывод в личный кошелёк пока не подтверждён: USDT остаются на балансе сервиса.'
  more=f'<li><a href="/sell-usdt/#sell-{country}">Как продать USDT в {esc(cfg["in"])}</a></li><li><a href="/where-to-buy/#{country}">Все страны на одной странице</a></li><li><a href="/english-terms/">Словарь: непонятные слова</a></li>'+''.join(f'<li><a href="/{r_slug}/">{esc(r_title)}</a></li>' for r_slug,r_title in cfg['related'])
  other=' · '.join(f'<a href="/{c["slug"]}/">{esc(WIZARD_CONTENT["countries"][k]["label"])}</a>' for k,c in COUNTRY_PAGES.items() if k!=country)
  toc='<a href="#short">01 Коротко</a><a href="#ways">02 Способы купить</a><a href="#law">03 Правовая основа</a><a href="#next">04 Что дальше</a>'
  short=f'<div class="lead-box"><p>{esc(cfg["intro"])}</p><p>Способов в проекте: {n}. '+('Все они условные: перед оплатой нужно проверить ограничения.' if ready==0 else f'По официальным источникам описано {ready}, остальные {n-ready} нужно проверить до оплаты.' if ready<n else 'Все они описаны по официальным источникам.')+' Реальные покупки мы не тестировали.</p></div>'
  return (COUNTRY_CSS+f'<a class="back" href="/where-to-buy/">← Все страны</a><div class="layout cpage"><aside class="toc"><strong>На этой странице</strong>{toc}</aside><article>'
    f'<div class="eyebrow">Покупка USDT · {esc(label)} · проверено {esc(reviewed)}</div><h1>Как купить USDT в {esc(cfg["in"])}</h1>'
    f'<section class="step" id="short"><h2><span>01</span>Коротко</h2>{short}<p><a class="route-go" href="/buy-usdt/#country={country}">Подобрать способ за 3 вопроса →</a></p></section>'
    f'<section class="step" id="ways"><h2><span>02</span>Способы купить</h2><p class="meta">{"Выберите вариант, который совпадает с вашим способом оплаты. Сервис может повторяться: различается способ пополнения." if len({r["service"] for r in routes})<n else "Откройте пошаговый план, чтобы увидеть шаги и проверки до оплаты."}</p><ul class="route-list">{"".join(row(r) for r in routes)}</ul>{notes}{notice}</section>'
    f'<section class="step" id="law"><h2><span>03</span>Правовая основа</h2><ul class="legal-list">{basis}</ul><p class="meta">Это справочные ссылки на законы и реестры, не юридическая консультация.</p></section>'
    f'<section class="step" id="next"><h2><span>04</span>Что дальше</h2><p>{esc(wallet_start)}</p><ul>{more}<li><a href="/wallet/">Кошелёк: как выбрать и создать</a></li></ul><p class="meta">Другие страны: {other}</p></section></article></div>')
for _country,_cfg in COUNTRY_PAGES.items():
  put(_cfg['slug'],f'Как купить USDT в {_cfg["in"]}',f'Маршруты покупки USDT в {_cfg["in"]}: правовая основа, реестры, способы оплаты и статус проверки.',country_page_body(_country))
# Языковые варианты (es/pt/en): страницы стран на языке страны, данные — content/language-variants.json и routes.json → language_variants.
# Это справочные страницы без мастера: маршруты не попадают во встроенные данные мастера на /buy-usdt/.
LANG_ROUTES=ROUTE_CONTENT['language_variants']['countries']
def lang_shell(lang,slug,body,crumbs):
  seo=SEO_CONTENT['pages'][slug];lc=LANG_CONTENT['languages'][lang];ui=lc['ui']
  url=page_url(slug);title=seo['content_title'];desc=seo['description'];seo_title=seo['title']
  full_title=seo_title if 'Crypto Step Guide' in seo_title else f'{seo_title} · Crypto Step Guide'
  e=lambda v:html.escape(str(v),quote=True)
  graph=[
   {'@type':'Organization','@id':f'{BASE_URL}/#publisher','name':'Crypto Step Guide','url':f'{BASE_URL}/','logo':f'{BASE_URL}/assets/csg-logo.svg','email':'hello@crypto-step-guide.com','description':ui['org_description']},
   {'@type':'WebSite','@id':f'{BASE_URL}/#website','url':f'{BASE_URL}/','name':'Crypto Step Guide','inLanguage':'ru','isAccessibleForFree':True,'publisher':{'@id':f'{BASE_URL}/#publisher'}},
   {'@type':'WebPage','@id':f'{url}#webpage','url':url,'name':title,'description':desc,'inLanguage':lang,'isAccessibleForFree':True,'isPartOf':{'@id':f'{BASE_URL}/#website'},'publisher':{'@id':f'{BASE_URL}/#publisher'},'datePublished':LANG_CONTENT['last_reviewed_on'],'dateModified':MODIFIED.get(slug,UPDATED)},
   {'@type':'BreadcrumbList','@id':f'{url}#breadcrumb','itemListElement':[{'@type':'ListItem','position':i,'name':n,'item':u} for i,(n,u) in enumerate(crumbs,1)]},
  ]
  schema=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'))
  og=f'{BASE_URL}/assets/og/home.png'
  head=(f'<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="{lang}" href="{url}">'
   f'<meta property="og:locale" content="{lc["locale"]}"><meta property="og:type" content="website"><meta property="og:site_name" content="Crypto Step Guide"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">'
   f'<meta property="og:image" content="{og}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Crypto Step Guide"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">{schema}</script>')
  links=''.join(f'<a href="/{LANG_ROUTES[k]["slug"]}/">{e(LANG_CONTENT["countries"][k]["name"])}</a>' for k in lc['countries'])
  return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(full_title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#f7f5ef">{head}<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="stylesheet" href="/style.css?v={STYLE_VERSION}"><link rel="stylesheet" href="/theme.css?v={THEME_VERSION}"></head>'
   f'<body><a class="skip" href="#main">{e(ui["skip"])}</a><header><nav aria-label="{e(ui["nav_label"])}"><a class="brand" href="/{lang}/"><b>CSG</b><span>Crypto Step Guide</span></a><div class="links">{links}<a href="/" lang="ru" hreflang="ru">Русская версия</a></div></nav></header><main id="main">{body}</main>'
   f'<footer class="footer"><span>{e(ui["footer"])}</span><span class="footer-links"><a href="/{lang}/">{e(ui["home"])}</a><a href="/" lang="ru" hreflang="ru">{e(ui["footer_ru"])}</a></span></footer></body></html>')
def lang_country_body(country):
  v=LANG_CONTENT['countries'][country];lang=v['language'];ui=LANG_CONTENT['languages'][lang]['ui'];routes=LANG_ROUTES[country]['routes']
  e=lambda x:html.escape(str(x),quote=True);ext=lambda u,t:f'<a href="{e(u)}" target="_blank" rel="noopener noreferrer">{e(t)} ↗</a>'
  reviewed=LANG_CONTENT['last_reviewed_on'];n=len(routes)
  def row(r):
    steps=''.join(f'<li>{e(x)}</li>' for x in r['steps']);checks=''.join(f'<li>{e(x)}</li>' for x in r['checks_before_payment'])
    srcs=''.join(ext(x['url'],x['label']) for x in r['sources'])
    return (f'<li class="route-row" id="{e(r["id"])}"><div class="route-head"><h3>{e(r["payment"])}</h3><span class="badge badge-cond">{e(ui["badge"])}</span></div>'
      f'<p class="route-meta"><b>{e(ui["service"])}:</b> {e(r["service"])} · <b>{e(ui["currency"])}:</b> {e(r["currency"])}</p><p class="route-meta">{e(r["label"])}</p>'
      f'<details open><summary>{e(ui["steps"])}</summary><ol>{steps}</ol></details>'
      f'<details><summary>{e(ui["checks"])}</summary><ul>{checks}</ul></details>'
      f'<details><summary>{e(ui["scope"])}</summary><p class="meta">{e(r["evidence_scope"])}</p></details>'
      f'<details><summary>{e(ui["sources"])}</summary><div class="src">{srcs}</div></details></li>')
  alerts=''.join(f'<div class="note warning">{e(a)}</div>' for a in v['alerts'])
  law=''.join(f'<p>{e(t)}</p>' for t in v['law_text'])+'<ul class="legal-list">'+''.join(f'<li>{ext(x["url"],x["text"])}</li>' for x in v['law'])+f'</ul><p class="meta">{e(ui["law_note"])}</p>'
  tax=''
  if v['tax']:
    tax=f'<section class="step" id="tax"><h2><span>04</span>{e(ui["h_tax"])}</h2>'+''.join(f'<p>{e(t)}</p>' for t in v['tax'])+('<ul class="legal-list">'+''.join(f'<li>{ext(x["url"],x["text"])}</li>' for x in v['tax_links'])+'</ul>' if v['tax_links'] else '')+'</section>'
  nxt_no='05' if tax else '04'
  siblings=[k for k in LANG_CONTENT['languages'][lang]['countries'] if k!=country]
  other=(' · '.join(f'<a href="/{LANG_ROUTES[k]["slug"]}/">{e(LANG_CONTENT["countries"][k]["name"])}</a>' for k in siblings)) if siblings else ''
  toc=f'<a href="#short">01 {e(ui["h_short"])}</a><a href="#ways">02 {e(ui["h_ways"])}</a><a href="#law">03 {e(ui["h_law"])}</a>'+(f'<a href="#tax">04 {e(ui["h_tax"])}</a>' if tax else '')+f'<a href="#next">{nxt_no} {e(ui["h_next"])}</a>'
  count=(ui['ways_count_one'] if n==1 else ui['ways_count'].format(n=n))+' '+ui['not_tested']
  eyebrow=ui['eyebrow'].format(country=v['name'],date=reviewed)
  return (COUNTRY_CSS+f'<a class="back" href="/{lang}/">{e(ui["back"])}</a><div class="layout cpage"><aside class="toc"><strong>{e(ui["h_short"])}</strong>{toc}</aside><article>'
    f'<div class="eyebrow">{e(eyebrow)}</div><h1>{e(SEO_CONTENT["pages"][LANG_ROUTES[country]["slug"]]["content_title"])}</h1>'
    f'<section class="step" id="short"><h2><span>01</span>{e(ui["h_short"])}</h2><div class="lead-box"><p>{e(v["intro"])}</p><p>{e(count)}</p><p>{e(ui["stablecoin"])}</p></div>{alerts}</section>'
    f'<section class="step" id="ways"><h2><span>02</span>{e(ui["h_ways"])}</h2><ul class="route-list">{"".join(row(r) for r in routes)}</ul></section>'
    f'<section class="step" id="law"><h2><span>03</span>{e(ui["h_law"])}</h2>{law}</section>{tax}'
    f'<section class="step" id="next"><h2><span>{nxt_no}</span>{e(ui["h_next"])}</h2><p>{e(v["next"])}</p>'+(f'<p class="meta">{e(ui["other"])}: {other}</p>' if other else '')+f'<p class="meta">{e(ui["about"])}</p></section></article></div>')
def lang_hub_body(lang):
  lc=LANG_CONTENT['languages'][lang];ui=lc['ui'];hub=lc['hub'];e=lambda x:html.escape(str(x),quote=True)
  cards=''.join(f'<a class="card" href="/{LANG_ROUTES[k]["slug"]}/"><h2>{e(LANG_CONTENT["countries"][k]["name"])}</h2><p>{e(LANG_CONTENT["countries"][k]["short"])}</p><span class="arrow" aria-hidden="true">→</span></a>' for k in lc['countries'])
  return (f'<div class="eyebrow">{e(ui["hub_countries"])}</div><h1>{e(hub["h1"])}</h1><p class="intro">{e(hub["intro"])}</p><section class="grid" aria-label="{e(ui["hub_countries"])}">{cards}</section>'
    f'<div class="note warning">{e(hub["note"])}</div><div class="note">{e(ui["stablecoin"])}</div><p class="meta">{e(ui["about"])}</p>')
for _lang,_lc in LANG_CONTENT['languages'].items():
  _hub=D/_lang;_hub.mkdir(parents=True,exist_ok=True)
  (_hub/'index.html').write_text(lang_shell(_lang,_lang,lang_hub_body(_lang),[('Crypto Step Guide',f'{BASE_URL}/'),(SEO_CONTENT['pages'][_lang]['content_title'],page_url(_lang))]),encoding='utf-8')
  for _country in _lc['countries']:
    _slug=LANG_ROUTES[_country]['slug'];_dir=D/_slug;_dir.mkdir(parents=True,exist_ok=True)
    (_dir/'index.html').write_text(lang_shell(_lang,_slug,lang_country_body(_country),[('Crypto Step Guide',f'{BASE_URL}/'),(SEO_CONTENT['pages'][_lang]['content_title'],page_url(_lang)),(SEO_CONTENT['pages'][_slug]['content_title'],page_url(_slug))]),encoding='utf-8')
slugs=['','start','buy','wallet','transfer','usdt','buy-usdt','bitcoin','where-to-buy','buy-usdt-kazakhstan-card','buy-usdt-shymkent-cash','buy-usdt-uzbekistan-card','buy-usdt-tashkent-cash','buy-usdt-serbia-bank','buy-usdt-serbia-crypto-atm','buy-usdt-kazakhstan','buy-usdt-belarus','buy-usdt-ukraine','buy-usdt-russia','buy-usdt-kyrgyzstan','buy-usdt-uzbekistan','buy-usdt-serbia','buy-bank-transfer','buy-local-p2p','sell-usdt','service-status','english-terms','articles','articles/kak-poyavilas-kriptovalyuta','articles/seti-usdt-trc20-erc20','articles/zamorozka-usdt','about','legal','privacy','es','pt','en','es/argentina','es/venezuela','es/espana','pt/brasil','en/india','en/nigeria']
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{page_url(slug)}</loc><lastmod>{MODIFIED.get(slug,UPDATED)}</lastmod></url>\n' for slug in slugs)+'</urlset>\n'
(D/'sitemap.xml').write_text(sitemap)
(D/'robots.txt').write_text(f'''User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Disallow: /

Sitemap: {BASE_URL}/sitemap.xml
''')
indexnow_key=(Path(__file__).parent/'.indexnow-key').read_text().strip()
(D/f'{indexnow_key}.txt').write_text(indexnow_key+'\n')
print('Created',len(slugs),'pages')

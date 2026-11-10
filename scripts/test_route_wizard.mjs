import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const model = JSON.parse(fs.readFileSync(path.join(root, 'content/routes.json'), 'utf8'));
const wizardModel = JSON.parse(fs.readFileSync(path.join(root, 'content/wizard.json'), 'utf8'));
const buyHtml = fs.readFileSync(path.join(root, 'dist/buy-usdt/index.html'), 'utf8');
const homeHtml = fs.readFileSync(path.join(root, 'dist/index.html'), 'utf8');
const finderHtml = fs.readFileSync(path.join(root, 'dist/where-to-buy/index.html'), 'utf8');

function readEmbedded(html, id) {
  const match = html.match(new RegExp('<script type="application/json" id="' + id + '">([\\s\\S]*?)<\\/script>'));
  assert.ok(match, id + ' must be embedded in built HTML');
  return JSON.parse(match[1]);
}
assert.deepEqual(readEmbedded(buyHtml, 'route-data').routes_by_country, model.routes_by_country);
assert.deepEqual(readEmbedded(buyHtml, 'wizard-data'), wizardModel);

const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));

class MockElement {
  constructor(id) {
    this.id = id; this.value = ''; this.textContent = ''; this.innerHTML = '';
    this.disabled = false; this.hidden = false; this.listeners = {};
  }
  addEventListener(name, callback) { (this.listeners[name] ??= []).push(callback); }
  fire(name) { for (const callback of this.listeners[name] ?? []) callback({ target: this }); }
}

function boot(search = '', pageHtml = buyHtml, hash = '') {
  const elements = new Map();
  const get = id => { if (!elements.has(id)) elements.set(id, new MockElement(id)); return elements.get(id); };
  get('route-data').textContent = JSON.stringify(readEmbedded(buyHtml, 'route-data'));
  get('wizard-data').textContent = JSON.stringify(wizardModel);
  for (const id of ['payment-fee', 'withdraw-fee']) get(id).value = '0';
  const scripts = [...pageHtml.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  const context = { document: { getElementById: get, querySelector: selector => get(selector === '.calculator' ? 'cost' : selector) }, window: { location: { search, hash }, history: { replaceState: (_, __, url) => { get('url').textContent = url; } } }, URLSearchParams, Intl, Number, Array, String, Object, Boolean, Math, JSON };
  vm.runInNewContext(scripts.at(-1)[1], context, { timeout: 1000 });
  const ui = {
    act: (step, value) => context.act(step, value),
    html: () => get('wizard-body').innerHTML,
    step: () => context.currentStep(),
    el: get,
    submit: (step, value) => { get('select-' + step).value = value; for (const callback of get('wizard-body').listeners.submit ?? []) callback({ preventDefault() {}, target: { getAttribute: name => name === 'data-select-form' ? step : null } }); },
    changeCountry: value => { for (const callback of get('wizard-body').listeners.change ?? []) callback({ target: { value, getAttribute: name => name === 'data-select-step' ? 'country' : null } }); },
    input: (id, value) => { get(id).value = value; get(id).fire('input'); }
  };
  return ui;
}

function pathTo(country, routeId) {
  for (const pay of wizardModel.countries[country].payments) {
    if (pay.route === routeId) return [['payment', pay.id]];
    for (const ch of pay.choices ?? []) if (ch.route === routeId) return [['payment', pay.id], ['choice', ch.id]];
  }
  throw new Error('No wizard path to ' + routeId);
}

// 1. Ukraine and Belarus expose payment choices, calculator, wallet guidance and conditional route plans.
for (const country of ['ukraine', 'belarus']) {
  const ui = boot();
  ui.act('country', country);
  assert.equal(ui.step(), 'payment');
  assert.ok(!wizardModel.countries[country].no_route);
  assert.ok(ui.html().includes('Способ оплаты'));
  for (const payment of wizardModel.countries[country].payments) assert.ok(ui.html().includes(escapeHtml(payment.title)));
  assert.equal(ui.el('wallet-guidance').hidden, true);
  assert.equal(ui.el('cost').hidden, true);
  ui.act('payment', '__unknown');
  assert.ok(ui.html().includes(escapeHtml(wizardModel.countries[country].payment_unknown)));
  ui.act('edit', 'country');
  assert.equal(ui.step(), 'country');
  const deepLink = boot('?country=' + country);
  assert.equal(deepLink.step(), 'payment', country + ': country deep link opens its payment choices');
  assert.equal(deepLink.el('cost').hidden, true);
}

// 2. Every published route is reachable from the first question and renders a complete plan.
let plans = 0;
for (const [country, routes] of Object.entries(model.routes_by_country)) {
  for (const route of routes.filter(r => r.status !== 'blocked')) {
    const ui = boot();
    assert.equal(ui.step(), 'country');
    assert.ok(ui.html().includes('Где вы живёте и как хотите оплатить?'));
    ui.act('country', country);
    for (const [step, value] of pathTo(country, route.id)) {
      ui.act(step, value);
    }
    const exchangeOnly = route.wallet_withdrawal_blocked === true;
    if (!exchangeOnly) {
      assert.equal(ui.step(), 'storage', route.id + ': asks where to keep USDT');
      ui.act('storage', 'own');
      assert.equal(ui.step(), 'wallet');
      ui.act('wallet', 'none');
      assert.equal(ui.step(), 'plan', route.id + ': "нет кошелька" сразу открывает план с выбором и созданием кошелька');
      const noWallet = ui.html();
      assert.ok(noWallet.includes(escapeHtml(wizardModel.wallet_criterion)), 'wallet suggestions explain the criterion');
      for (const w of wizardModel.wallets.filter(x => route.allowed_destinations.includes(x.id))) assert.ok(noWallet.includes(escapeHtml(w.name)), route.id + ': доступный кошелёк ' + w.name + ' показан');
      for (const stepText of wizardModel.wallet_setup_steps) assert.ok(noWallet.includes(escapeHtml(stepText)), route.id + ': шаги создания кошелька показаны сразу');
      assert.ok(noWallet.includes('App Store: приложение есть для вашей страны'), route.id + ': доступность в App Store показана для страны');
      ui.act('pick-wallet', 'trust');
    }
    assert.equal(ui.step(), 'plan', route.id + ': reaches the plan');
    const html = ui.html();
    assert.ok(html.includes('Ваш план: ' + escapeHtml(route.service)), route.id + ': plan heading');
    assert.ok(html.includes(escapeHtml(route.payment)), route.id + ': payment shown');
    assert.ok(html.includes(escapeHtml(route.evidence_scope)), route.id + ': evidence scope shown');
    for (const s of route.steps) assert.ok(html.includes(escapeHtml(s)), route.id + ': every route step shown');
    for (const c of route.checks_before_payment) assert.ok(html.includes(escapeHtml(c)), route.id + ': pre-payment checks shown');
    for (const source of route.sources) assert.ok(html.includes(escapeHtml(source.url)), route.id + ': official source shown');
    assert.ok(html.includes('Почему этот вариант'), route.id + ': explains the choice');
    if (route.purchase_url) {
      const cta = 'href="' + escapeHtml(route.purchase_url) + '"';
      assert.ok(html.includes(cta), route.id + ': official purchase CTA is present');
      assert.ok(html.includes(escapeHtml(route.purchase_label)), route.id + ': CTA label is clear');
      const checkListEnd = html.indexOf('</ul>', html.indexOf('Проверьте до оплаты'));
      assert.ok(checkListEnd >= 0 && html.indexOf(cta) > checkListEnd, route.id + ': all checks appear before the external CTA');
    }
    if (exchangeOnly) {
      assert.ok(html.includes(escapeHtml(route.destination_notice)), 'Russia states where the route ends');
      assert.ok(!html.includes('href="/transfer/"'), 'Russia must not expose a wallet-transfer CTA');
      assert.ok(!html.includes('href="/wallet/"'), 'Russia must not expose a personal-wallet CTA');
      assert.equal(ui.el('wallet-guidance').hidden, true);
    } else {
      for (const s of wizardModel.wallet_setup_steps) assert.ok(html.includes(escapeHtml(s)), route.id + ': new-wallet setup shown');
      assert.ok(html.includes('href="/transfer/"'), route.id + ': transfer guidance link');
      assert.ok(html.includes(route.network ? escapeHtml(route.network) : escapeHtml(wizardModel.network_rule_default)), route.id + ': network rule shown');
      assert.equal(ui.el('wallet-guidance').hidden, false);
    }
    if (['ukraine', 'belarus'].includes(country)) {
      ui.input('paid', '100'); ui.input('bought', '2');
      assert.ok(ui.el('total').textContent.endsWith(' ' + route.currency), route.id + ': calculator uses the local currency');
      assert.ok(ui.el('received').textContent.endsWith(' USDT'), route.id + ': calculator reports net USDT');
      assert.equal(ui.el('cost').hidden, false);
      assert.equal(ui.el('wallet-guidance').hidden, false);
    }
    plans++;
  }
}

// 2. Branches that do not lead to a route explain why and offer a way forward.
let ui = boot();
ui.act('country', 'russia');
ui.act('payment', 'bank');
assert.equal(ui.step(), 'none');
assert.ok(ui.html().includes('Подтверждённого способа нет'));
assert.ok(ui.html().includes('data-step="edit" data-value="payment"'));

ui = boot();
ui.act('country', 'kazakhstan');
ui.act('payment', 'card');
ui.act('choice', 'other-card');
assert.equal(ui.step(), 'storage', 'AUSU card route confirms the fixed wallet destination');
assert.ok(ui.html().includes('Этот маршрут отправляет USDT сразу на личный кошелёк'));
assert.ok(ui.html().includes('Подготовить личный кошелёк')); // Route details appear in the completed plan, after the storage choice.

// 3. "Не знаю" explains without moving forward.
ui = boot();
ui.act('country', 'kazakhstan');
ui.act('payment', '__unknown');
assert.equal(ui.step(), 'payment');
assert.ok(ui.html().includes(escapeHtml(wizardModel.countries.kazakhstan.payment_unknown)));
ui.act('payment', 'bank');
ui.act('choice', '__unknown');
assert.ok(ui.html().includes(escapeHtml(wizardModel.countries.kazakhstan.payments[0].unknown)));
ui.act('choice', 'freedom-qazpost');
ui.act('storage', '__unknown');
assert.ok(ui.html().includes(escapeHtml(wizardModel.storage.unknown)));

ui = boot();
ui.act('country', 'belarus');
ui.act('payment', 'bank');
ui.act('choice', '__unknown');
assert.ok(ui.html().includes(escapeHtml(wizardModel.countries.belarus.payments[0].unknown)));

// 4. Alternative route, back and edit keep answers consistent.
ui = boot();
ui.act('country', 'kazakhstan');
ui.act('payment', 'bank');
ui.act('choice', 'freedom-qazpost');
ui.act('storage', 'exchange');
assert.equal(ui.step(), 'plan');
assert.ok(ui.html().includes('Ваш план: Binance Kazakhstan'));
assert.ok(!ui.html().includes('href="/transfer/"'), 'no transfer CTA when USDT stay on the exchange');
ui.act('alt', 'kz-bybit-bank');
assert.ok(ui.html().includes('Ваш план: Bybit Kazakhstan'), 'alternative route switches the plan');
ui.act('edit', 'storage');
assert.equal(ui.step(), 'storage');
ui.act('back');
assert.equal(ui.step(), 'choice');
ui.act('back');
assert.equal(ui.step(), 'payment');
ui.act('back');
assert.equal(ui.step(), 'country');

ui = boot();
ui.act('country', 'uzbekistan');
assert.equal(ui.step(), 'payment', 'the wizard asks which payment category fits');
ui.act('back');
assert.equal(ui.step(), 'country', 'back returns to the country question');
ui.act('country', 'uzbekistan');
ui.act('payment', 'local');
ui.act('choice', 'asterium');
assert.equal(ui.step(), 'storage');
ui.act('storage', 'own');
ui.act('wallet', 'tronlink');
assert.ok(ui.html().includes('TRON (TRC-20)'));

// 5. Deep links from other pages.
ui = boot('?country=russia&route=ru-bybit-p2p');
assert.equal(ui.step(), 'plan');
assert.ok(ui.html().includes(escapeHtml(model.routes_by_country.russia[0].destination_notice)));
ui = boot('?country=kazakhstan&route=kz-binance-p2p-maker');
assert.equal(ui.step(), 'storage');
ui = boot('?country=unknown');
assert.equal(ui.step(), 'country');
// Ссылки сайта используют #country=…&route=… (без параметров в URL): мастер открывается так же, как по ?country=.
ui = boot('', buyHtml, '#country=russia&route=ru-bybit-p2p');
assert.equal(ui.step(), 'plan');
ui = boot('', buyHtml, '#country=kazakhstan&route=kz-binance-p2p-maker');
assert.equal(ui.step(), 'storage');
ui = boot('', buyHtml, '#wizard');
assert.equal(ui.step(), 'country');

// 6. Cost calculator follows the chosen destination.
ui = boot();
ui.act('country', 'kazakhstan');
ui.act('payment', 'card');
ui.act('choice', 'mastercard');
ui.act('storage', 'own');
ui.act('wallet', 'trust');
ui.input('paid', '100000'); ui.input('payment-fee', '0'); ui.input('bought', '195,5'); ui.input('withdraw-fee', '1');
assert.equal(ui.el('received').textContent, '194,5 USDT', 'withdrawal fee is subtracted for a personal wallet');
assert.ok(ui.el('total').textContent.endsWith(' KZT'));
assert.ok(ui.el('effective').textContent.endsWith(' KZT'));
ui.act('edit', 'storage');
ui.act('storage', 'exchange');
assert.equal(ui.el('withdraw-fee').disabled, true, 'no withdrawal fee when USDT stay on the exchange');
assert.equal(ui.el('received').textContent, '195,5 USDT');
ui.act('edit', 'storage');
ui.act('storage', 'own');
ui.act('wallet', 'trust');
assert.equal(ui.el('withdraw-fee').value, '1', 'entered withdrawal fee is restored');
assert.equal(ui.el('received').textContent, '194,5 USDT');
ui.input('paid', '-5');
assert.equal(ui.el('calc-message').textContent, 'Суммы и комиссии не могут быть отрицательными.');
ui.input('paid', '1.000,50');
assert.ok(ui.el('calc-message').textContent.startsWith('Не удалось прочитать число'));
ui.input('paid', '100000'); ui.input('bought', '0'); ui.input('withdraw-fee', '0');
assert.equal(ui.el('calc-message').textContent, 'Укажите количество купленных USDT больше нуля.');
ui = boot('?country=russia&route=ru-bybit-p2p');
ui.input('paid', '10000'); ui.input('bought', '120');
assert.equal(ui.el('withdraw-fee').disabled, true, 'Russia never includes a withdrawal');
assert.equal(ui.el('received').textContent, '120 USDT');
assert.ok(ui.el('total').textContent.endsWith(' RUB'));

// 8. Where-to-buy is static, lists every published route and leads into the wizard.
assert.ok(!finderHtml.includes('<script>'), 'where-to-buy has no client-side finder');
for (const [country, routes] of Object.entries(model.routes_by_country)) {
  for (const route of routes.filter(r => r.status !== 'blocked')) {
    assert.ok(finderHtml.includes('/buy-usdt/#country=' + country + '&amp;route=' + route.id), route.id + ': plan link');
    for (const source of route.sources) assert.ok(finderHtml.includes(escapeHtml(source.url)), route.id + ': source listed');
  }
}
assert.ok(finderHtml.includes('href="/buy-usdt/#wizard"'));
for (const country of ['ukraine', 'belarus']) {
  const routes = model.routes_by_country[country];
  assert.ok(routes.length > 0 && !wizardModel.countries[country].no_route);
  for (const route of routes) {
    assert.ok(finderHtml.includes('/buy-usdt/#country=' + country + '&amp;route=' + route.id));
    assert.ok(finderHtml.includes(escapeHtml(route.purchase_url)));
  }
}
assert.ok(finderHtml.includes(escapeHtml(wizardModel.countries.russia.payments.find(p => p.id === 'bank').message)));

console.log('Wizard behavior valid: ' + plans + ' routes reachable from the first question, dead ends, "Не знаю", back/edit, deep links, calculator and static where-to-buy.');


// Regression: the actual select/change/submit handlers work on both entry pages.
for (const pageHtml of [homeHtml, buyHtml]) {
  const form = boot('', pageHtml);
  assert.ok(form.html().includes('<select id="select-country"'));
  assert.ok(form.html().includes('<select id="select-payment"'));
  assert.ok(form.html().includes('disabled'));
  assert.equal(form.el('cost').hidden, true);
  form.changeCountry('ukraine');
  assert.equal(form.step(), 'payment');
  assert.ok(form.html().includes('<option value="p2p"'));
  assert.ok(!form.html().includes('<option value="card"'));
  form.submit('payment', 'p2p');
  form.submit('storage', 'exchange');
  assert.equal(form.step(), 'plan');
  assert.equal(form.el('cost').hidden, false);
  assert.equal(form.el('wallet-guidance').hidden, true);
  assert.ok(form.el('url').textContent.includes('route=ua-bybit-p2p'));
  form.act('edit', 'country');
  assert.equal(form.step(), 'country');
  assert.equal(form.el('cost').hidden, true);
  assert.ok(!form.el('url').textContent.includes('route='));
  form.changeCountry('kazakhstan');
  form.submit('payment', 'card');
  assert.equal(form.step(), 'choice');
  assert.ok(form.html().includes('<select id="select-choice"'));
  assert.ok(!form.html().includes('Ваш план'));
}
assert.ok(buyHtml.includes('<details class="route-reference" id="reference"><summary>'));
assert.ok(!homeHtml.includes('class="primary-route"'));
assert.deepEqual(readEmbedded(homeHtml, 'wizard-data'), readEmbedded(buyHtml, 'wizard-data'));
console.log('Compact form regression valid on homepage and /buy-usdt/: select, submit, dependent reset and URL.');

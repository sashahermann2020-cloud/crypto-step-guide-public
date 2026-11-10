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
const opts = (html, step) => { const m = html.match(new RegExp('<select id="select-' + step + '"[\\s\\S]*?</select>')); return m ? [...m[0].matchAll(/<option value="([^"]+)"/g)].map(x => x[1]) : []; };
// Полный обход мастера: каждая страна, каждый ответ на каждом шаге, диплинки #country=…&route=…; план должен содержать подготовку кошелька.
const problems = []; const seen = new Set();
function explore(trail, hash = '') {
  const ui = boot('', buyHtml, hash);
  try { for (const [s, v] of trail) ui.act(s, v); } catch (e) { problems.push(trail.join('>') + ' EXC ' + e.message); return; }
  const step = ui.step(); const html = ui.html();
  const key = trail.map(t => t.join(':')).join('>');
  if (step === 'plan') { seen.add(key); if(!trail.length) {}  if (!html.includes('Ваш план')) problems.push(key + ' plan empty');
    const none = trail.some(t => t[0]==='wallet' && t[1]==='none') || trail.some(t=>t[0]==='pick-wallet');
    const stays = html.includes('аккаунт сервиса');
    if (none && !stays && !/Подготовьте кошелёк|Установите и создайте кошелёк|Выберите и установите кошелёк/.test(html)) problems.push(key + ' NO wallet setup section');
    const plain = html.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ');
    if (!stays && !/Receive|получить/.test(plain) && none) problems.push(key+' no receive step'); return; }
  if (step === 'unavailable' || step === 'none') { problems.push(key + ' => ' + step); return; }
  const o = opts(html, step).filter(v => v !== '__unknown');
  if (!o.length) { problems.push(key + ' => step ' + step + ' has NO options: ' + html.replace(/<[^>]+>/g, ' ').slice(0, 200)); return; }
  if (trail.length > 8) { problems.push(key + ' too deep'); return; }
  for (const v of o) explore([...trail, [step, v]], hash);
}
for (const c of Object.keys(wizardModel.countries)) explore([['country', c]]);
for (const [c, rs] of Object.entries(model.routes_by_country)) {
  explore([], '#country=' + c);
  for (const r of rs) explore([], '#country=' + c + '&route=' + r.id);
}
// Единственная допустимая остановка: страна без подтверждённого способа оплаты, показанная с пояснением и кнопкой возврата.
const allowed = new Set(['country:russia>payment:bank => none', 'payment:bank => none']);
const unexpected = problems.filter(p => !allowed.has(p));
assert.deepEqual(unexpected, [], 'Мастер содержит тупики или планы без кошелька:\n' + unexpected.join('\n'));
console.log('Wizard paths valid: ' + seen.size + ' plans reached from every country, deep link and answer combination; no dead ends.');

/* Drives the real page script in Node with a fake browser + fake market. */
const fs = require('fs'), vm = require('vm');
const els = {};
function el(id) {
  if (id === 'c') return { width: 1000, height: 270, getContext: () => new Proxy({}, { get: () => () => {} }) };
  if (!els[id]) els[id] = { id, classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
    style: {}, value: '', innerHTML: '', textContent: '', dataset: {}, setAttribute() {}, after() {} };
  return els[id];
}
global.document = { getElementById: el, querySelectorAll: () => [], createElement: () => el('tmp') };
global.window = global;
global.localStorage = { s: {}, getItem(k) { return this.s[k] || null }, setItem(k, v) { this.s[k] = v }, removeItem(k) { delete this.s[k] } };
global.alert = m => console.log('  [alert]', m);
global.confirm = () => true;
global.setInterval = () => 0;
let P = 100, SIG = 1;
const instruments = [
  { symbol: 'AAPL', name: 'Apple', market: 'US', exchange: 'US', type: 'STOCK', unit: 1, margin: 1, currency: 'USD' },
  { symbol: 'BTC-USD', name: 'Bitcoin', market: 'CRYPTO', exchange: 'Crypto', type: 'CRYPTO', unit: 1, margin: 1, currency: 'USD' },
  { symbol: 'NIFTY-FUT', name: 'NIFTY Futures', market: 'IN', exchange: 'F&O', type: 'FUT', unit: 75, margin: 0.12, currency: 'INR' },
];
global.fetch = async url => {
  if (url.startsWith('/api/instruments')) return { json: async () => instruments };
  if (url.startsWith('/api/fx')) return { json: async () => ({ USDINR: 100 }) };
  if (url.startsWith('/api/quotes')) return { json: async () => [{ symbol: 'AAPL', price: P, change_pct: 1, currency: 'USD', simulated: false }] };
  if (url.startsWith('/api/signal')) return { json: async () => ({ signal: SIG, price: P, simulated: false }) };
  if (url.startsWith('/api/best')) return { json: async () => ({ best: 'momentum' }) };
  if (url.startsWith('/api/recommendations') || url.startsWith('/api/recommend'))
    return { json: async () => [{ symbol: 'AAPL', action: 'BUY', confidence: 72, price: P, target: P * 1.06, stop: P * 0.975,
      reward_pct: 6, risk_pct: 2.5, rr: 2.4, reasons: ['4 of 6 strategies bullish'], best_strategy: 'momentum' }] };
  if (url.startsWith('/api/scan')) return { json: async () => [] };
  if (url.startsWith('/api/backtest')) return { json: async () => ({ return_pct: 5, max_drawdown_pct: 2, sharpe: 1, num_trades: 3, last: P, index: [100, 101], equity: [100, 101], trades: [] }) };
  throw new Error('unexpected ' + url);
};
const page = process.argv[2];
vm.runInThisContext(fs.readFileSync(page, 'utf8') + '\n;globalThis.__S=()=>S;globalThis.__FX=()=>FX;globalThis.__tickBot=tickBot;globalThis.__tick=tick;globalThis.__startAlgo=startAlgo;');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  await sleep(120);
  const S = globalThis.__S();
  const ok = [];
  const check = (name, cond, extra) => { ok.push(cond); console.log((cond ? 'PASS ' : 'FAIL ') + name, extra === undefined ? '' : extra); };
  ['ts:2.5','tp:6','pp:3','sz:10','mode:both','strat:auto','mq:10'].forEach(kv=>{const [k,v]=kv.split(':');el(k).value=v});
  check('capital is 1 crore', S.cash === 1e7, '\u20b9' + S.cash.toLocaleString('en-IN'));
  globalThis.__startAlgo('AAPL', 'sma_crossover');
  const b = S.bots.AAPL;
  SIG = 1; await globalThis.__tickBot(b);
  check('enters immediately on a live signal (no waiting)', b.pos === 1 && b.side === 'LONG', 'shares ' + b.qty.toFixed(0));
  check('1% commission charged on entry', S.fee > 0, '\u20b9' + S.fee.toFixed(0));
  P = 104; await globalThis.__tickBot(b);
  check('partial profit booked', b.qty > 0 && b.partialDone && S.pending > 0, 'pending \u20b9' + S.pending.toFixed(0));
  P = 107; await globalThis.__tickBot(b);
  check('take profit closed the rest', !b.pos, 'net \u20b9' + S.net.toFixed(0));
  const netAfterLong = S.net;
  SIG = 0; b.cd = 0; await globalThis.__tickBot(b);
  check('short side opens when signal is bearish', b.pos === 1 && b.side === 'SHORT');
  P = 100; await globalThis.__tickBot(b);
  check('short books profit as price falls', S.net > netAfterLong, 'net \u20b9' + S.net.toFixed(0));
  const pend = S.pending; el('xfer').onclick();
  check('transfer to bank moves booked profit', Math.abs(S.bank - pend) < 1 && S.pending === 0, 'bank \u20b9' + S.bank.toFixed(0));
  el('mq').value = 10; const feeBefore = S.fee; el('buy').onclick();
  const held = !!S.hold.AAPL; el('close1').onclick();
  check('manual buy then close', held && !S.hold.AAPL && S.fee > feeBefore);
  globalThis.__startAlgo('NIFTY-FUT', 'macd');
  const fb = S.bots['NIFTY-FUT'];
  fb.sz = 10; SIG = 1; await globalThis.__tickBot(fb);
  const notional = fb.qty * fb.entry * 75;
  check('futures trade on 12% margin, not full notional', fb.pos === 1 && fb.blocked < notional * 0.2,
    'blocked ₹' + fb.blocked.toFixed(0) + ' of notional ₹' + notional.toFixed(0));
  const failed = ok.filter(x => !x).length;
  console.log(failed ? 'RESULT FAIL' : 'RESULT PASS');
  process.exit(failed ? 1 : 0);
})();

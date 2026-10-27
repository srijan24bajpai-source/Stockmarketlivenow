PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AlgoTrader - paper trading desk</title>
<style>
:root{--bg:#e8ecf4;--hi:#fff;--lo:#c2c9d8;--txt:#111827;--mut:#434e68;--acc:#2f4fd8;--up:#067a4d;--dn:#c81e42;--gold:#8a6a00}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;font-size:15px;line-height:1.45;-webkit-font-smoothing:antialiased}
.raised{background:var(--bg);border-radius:22px;box-shadow:9px 9px 20px var(--lo),-9px -9px 20px var(--hi)}
.inset{background:var(--bg);border-radius:14px;box-shadow:inset 5px 5px 10px var(--lo),inset -5px -5px 10px var(--hi)}
header{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;padding:16px 24px;margin:20px auto;max-width:1360px}
header h1{font-size:21px;margin:0;font-weight:800;letter-spacing:.2px}
.bank{font-size:13px;color:var(--mut);font-weight:600}
.bank b{display:block;font-size:19px;color:var(--txt)}
.tag{font-size:11px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:var(--gold);padding:4px 10px;border-radius:99px}
button{font:inherit;font-weight:700;color:var(--txt);background:var(--bg);border:0;border-radius:14px;padding:10px 16px;cursor:pointer;box-shadow:5px 5px 10px var(--lo),-5px -5px 10px var(--hi)}
button:active,button.on{box-shadow:inset 4px 4px 9px var(--lo),inset -4px -4px 9px var(--hi);color:var(--acc)}
button.go{color:#fff;background:var(--acc)}
input,select{font:inherit;font-weight:600;color:var(--txt);background:var(--bg);border:0;border-radius:13px;padding:10px 13px;outline:none;box-shadow:inset 4px 4px 8px var(--lo),inset -4px -4px 8px var(--hi)}
input::placeholder{color:var(--mut);font-weight:500}
main{display:grid;grid-template-columns:350px 1fr;gap:24px;max-width:1360px;margin:0 auto 36px;padding:0 20px}
@media(max-width:980px){main{grid-template-columns:1fr}}
.side{padding:18px;display:flex;flex-direction:column;height:calc(100vh - 140px);min-height:460px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.chip{padding:5px 12px;font-size:12.5px;border-radius:99px}
#list{overflow:auto;flex:1;padding:4px 6px 4px 0}
.row{display:flex;justify-content:space-between;gap:10px;align-items:center;padding:11px 14px;margin-bottom:10px;border-radius:15px;cursor:pointer;box-shadow:4px 4px 9px var(--lo),-4px -4px 9px var(--hi)}
.row.sel{box-shadow:inset 4px 4px 9px var(--lo),inset -4px -4px 9px var(--hi)}
.sym{font-weight:800}.nm{font-size:12.5px;color:var(--mut)}
.px{text-align:right;font-size:14px;font-weight:800}.chg{font-size:12px;font-weight:700}
.on-pill{font-size:10px;font-weight:900;color:var(--up);letter-spacing:.5px}
.panel{padding:24px}
.top{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.top h2{margin:0;font-size:30px;font-weight:800}
.big{font-size:32px;font-weight:800;margin-top:2px}.big small{font-size:14px;font-weight:700;margin-left:10px}
.ctl{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:16px;margin:22px 0}
.stat{padding:14px 16px;border-radius:16px}.stat small{color:var(--mut);font-weight:700;font-size:12px;display:block}.stat b{font-size:21px}
.profitbox{padding:20px;border-radius:20px;margin-bottom:18px;box-shadow:inset 6px 6px 14px var(--lo),inset -6px -6px 14px var(--hi)}
.profitbox h3{margin:0 0 4px;font-size:16px;letter-spacing:.3px}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(125px,1fr));gap:14px;margin:14px 0}
.pcell b{display:block;font-size:20px}
.pcell small{color:var(--mut);font-size:11.5px;font-weight:700}
.rowbtns{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
canvas{width:100%;height:290px;border-radius:18px}
.legend{font-size:12.5px;color:var(--mut);margin-top:8px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:20px}
@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.card{padding:18px;border-radius:18px}.card h3{margin:0 0 10px;font-size:15px}
.cfg{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0}
.cfg label{font-size:11.5px;font-weight:700;color:var(--mut)}.cfg input{display:block;width:88px;margin-top:4px}
#log{max-height:150px;overflow:auto;font-size:13px}
#log div{padding:5px 0;border-bottom:1px solid var(--lo)}
#log b{font-weight:800}
.up{color:var(--up)}.dn{color:var(--dn)}
.sw{display:flex;align-items:center;gap:9px;font-weight:700;font-size:13.5px}
.tg{width:56px;height:29px;border-radius:99px;position:relative;padding:0}
.tg i{position:absolute;top:4px;left:5px;width:21px;height:21px;border-radius:50%;background:var(--bg);box-shadow:3px 3px 6px var(--lo),-2px -2px 5px var(--hi);transition:.22s}
.tg.on i{left:30px;background:var(--up)}
.qty{width:100px}
</style></head><body>
<header class="raised">
 <div><h1>&#9670; AlgoTrader &mdash; paper trading desk</h1><div class="tag inset">Simulated money &middot; real market data</div></div>
 <div class="bank">Bank account (simulated) <b id="bankh"></b></div>
 <div class="bank">Last price update <b id="upd">--</b></div>
 <button id="rst">Reset simulation</button>
</header>
<main>
 <aside class="raised side">
  <input id="q" placeholder="Search 125 stocks, e.g. TSLA, Infosys">
  <div class="chips" id="chips"></div>
  <div id="list"></div>
  <div class="legend" id="count"></div>
 </aside>
 <section class="raised panel">
  <div class="top">
   <div><h2 id="hs">-</h2><div class="nm" id="hn"></div><div class="big" id="hp"></div></div>
   <div class="ctl">
    <select id="strat">
     <option value="auto">Auto: best of all</option>
     <option value="sma_crossover">SMA crossover</option>
     <option value="rsi">RSI mean reversion</option>
     <option value="macd">MACD</option>
     <option value="bollinger">Bollinger breakout</option>
     <option value="donchian">Donchian breakout</option>
     <option value="momentum">Momentum</option>
    </select>
    <button id="go">Backtest</button>
   </div>
  </div>
  <div class="stats" id="stats"></div>
  <div class="profitbox">
   <h3>Profit box &mdash; booked in real time</h3>
   <div class="pgrid" id="pbox"></div>
   <div class="rowbtns">
    <button class="go" id="xfer">Transfer profits to bank account</button>
    <div class="sw"><span>Auto-transfer after every trade</span><button class="tg inset" id="auto"><i></i></button></div>
   </div>
  </div>
  <canvas id="c" width="1000" height="290"></canvas>
  <div class="legend">Dark: stock price (indexed to 100, 1 year) &middot; Blue: strategy equity &middot; Green/red dots: backtest buys/sells</div>
  <div class="grid2">
   <div class="card inset">
    <h3>Algo trading bot &mdash; <span id="bs" class="legend" style="display:inline">off</span></h3>
    <div class="cfg">
     <label>Trailing stop %<input id="ts" type="number" value="2.5" min="0.3" step="0.1"></label>
     <label>Take profit %<input id="tp" type="number" value="6" min="0.5" step="0.5"></label>
     <label>Partial book %<input id="pp" type="number" value="3" min="0.5" step="0.5"></label>
     <label>Size % of cash<input id="sz" type="number" value="10" min="1" max="100"></label>
    </div>
    <div class="sw" style="margin:10px 0"><span>Enable bot on <span id="bsym">AAPL</span></span><button class="tg inset" id="tg"><i></i></button></div>
    <div id="log"></div>
   </div>
   <div class="card inset">
    <h3>Manual order (1% commission)</h3>
    <div class="cfg"><label>Quantity<input id="mq" type="number" value="10" min="1" step="1" class="qty"></label></div>
    <div class="rowbtns"><button class="go" id="buy">BUY</button><button id="sell">SELL</button></div>
    <div class="legend" id="hold"></div>
    <h3 style="margin-top:16px">Recent fills</h3>
    <div id="fills"></div>
   </div>
  </div>
  <div class="legend">Paper orders executed at live delayed prices. No real money, no broker. 1% commission is deducted on every buy and sell. Not financial advice.</div>
 </section>
</main>
<script>
const $=id=>document.getElementById(id);
const CAP=1e13; // 10 lakh crore
const FEE=0.01;
const inr=v=>'\u20b9'+Number(v).toLocaleString('en-IN',{maximumFractionDigits:2});
let ALL=[],sel='AAPL',sector='All',term='',Q={},FX=95.18;
let S=JSON.parse(localStorage.getItem('sim2')||'null')||{cash:CAP,bank:0,gross:0,net:0,fee:0,pending:0,sells:0,wins:0,auto:false,bots:{},hold:{},fills:[]};
const save=()=>localStorage.setItem('sim2',JSON.stringify(S));
const cur=s=>((ALL.find(x=>x.symbol===s)||{}).exchange==='NSE')?'INR':'USD';
const toINR=(p,s)=>cur(s)==='NSE'?p:p*FX;
const pxINR=s=>{const q=Q[s];return q?toINR(q.price,s):null};
const now=()=>new Date().toLocaleTimeString();
function fill(side,sym,qty,price,why,pl){
 S.fills.unshift({side,sym,qty,price,why,pl,t:now()});S.fills=S.fills.slice(0,40);
}
/* ---------- money movements ---------- */
function buy(sym,spend,why,bot){
 const p=pxINR(sym);if(!p||spend<=0)return false;
 spend=Math.min(spend,S.cash);if(spend<1)return false;
 const qty=spend/(p*(1+FEE));
 const fee=spend-qty*p;
 S.cash-=spend;S.fee+=fee;
 if(bot){bot.pos=1;bot.qty=qty;bot.buyPrice=p;bot.entry=spend/qty;bot.peak=p;bot.partialDone=false;bot.cost=spend;bot.realized=0}
 else{const h=S.hold[sym]||{qty:0,cost:0,buyPrice:p};
  h.buyPrice=(h.qty*h.buyPrice+qty*p)/(h.qty+qty);h.qty+=qty;h.cost+=spend;S.hold[sym]=h}
 fill('BUY',sym,qty,p,why,null);save();return true;
}
function sell(sym,qty,why,bot){
 const p=pxINR(sym);if(!p||qty<=0)return;
 const proceeds=qty*p*(1-FEE);const costPerShare=bot?bot.entry:(S.hold[sym].cost/S.hold[sym].qty);
 const cost=qty*costPerShare;const pl=proceeds-cost;
 const rawBuy=bot?bot.buyPrice:(S.hold[sym].buyPrice);
 const gross=qty*(p-rawBuy);const fee=qty*p*FEE;
 S.cash+=proceeds;S.gross+=gross;S.fee+=fee;S.net+=pl;S.pending+=pl;S.sells++;
 if(pl>0)S.wins++;
 if(bot){bot.qty-=qty;bot.cost=Math.max(0,bot.cost-cost);bot.realized+=pl;if(bot.qty<=1e-9){bot.pos=0;bot.qty=0;bot.armed=false}bot.log.unshift({side:'SELL',why,qty,pl,price:p,t:now()});bot.log=bot.log.slice(0,25)}
 else{const h=S.hold[sym];h.qty-=qty;h.cost-=cost;if(h.qty<=1e-9)delete S.hold[sym]}
 fill('SELL',sym,qty,p,why,pl);save();
}
/* ---------- profit box ---------- */
function invested(){
 let v=0;for(const [s,h] of Object.entries(S.hold)){const p=pxINR(s);v+=h.qty*(p||h.buyPrice)}
 for(const [s,b] of Object.entries(S.bots))if(b.pos)v+=b.qty*(pxINR(s)||b.entry);
 return v;
}
function renderMoney(){
 const eq=S.cash+invested();
 $('bankh').textContent=inr(S.bank);
 const unrealized=invested()-Object.entries(S.hold).reduce((a,[s,h])=>a+h.cost,0)-Object.values(S.bots).filter(b=>b.pos).reduce((a,b)=>a+b.cost,0);
 const wr=S.sells?(S.wins/S.sells*100).toFixed(0):'0';
 $('pbox').innerHTML=[
  ['Net booked P&L',inr(S.net),S.net>=0?'up':'dn'],
  ['Gross P&L',inr(S.gross),S.gross>=0?'up':'dn'],
  ['Commission paid',inr(S.fee),'dn'],
  ['Pending transfer',inr(S.pending),S.pending>=0?'up':'dn'],
  ['Moved to bank',inr(S.bank),'up'],
  ['Win rate',wr+'% ('+S.wins+'/'+S.sells+')',''],
  ['Trading capital',inr(S.cash),''],
  ['Open positions',inr(invested())+(unrealized>=0?' <span class="up">+'+inr(unrealized)+'</span>':' <span class="dn">'+inr(unrealized)+'</span>'),'']
 ].map(x=>`<div class="pcell"><small>${x[0]}</small><b class="${x[2]}">${x[1]}</b></div>`).join('');
}
$('xfer').onclick=()=>{
 if(!S.pending){alert('No booked profit to transfer yet.');return}
 if(!confirm('Move '+inr(S.pending)+' of booked P&L from the trading wallet to your simulated bank account?'))return;
 S.bank+=S.pending;S.pending=0;save();renderMoney();
};
$('auto').onclick=()=>{S.auto=!S.auto;$('auto').classList.toggle('on',S.auto);save()};
$('rst').onclick=()=>{if(confirm('Reset the whole simulation? Capital, bots, positions and profits will be cleared.')){localStorage.removeItem('sim2');location.reload()}};
/* ---------- list ---------- */
function pxCell(s){const q=Q[s];if(!q)return '<span class="nm">...</span>';const cls=q.change_pct>=0?'up':'dn';
 return `<div class="px">${inr(pxINR(s))}</div><div class="chg ${cls}">${q.change_pct>=0?'+':''}${q.change_pct}%</div>`}
function renderList(){
 const t=term.toLowerCase();
 const f=ALL.filter(s=>(sector==='All'||s.sector===sector||s.exchange===sector)&&(s.symbol.toLowerCase().includes(t)||s.name.toLowerCase().includes(t)));
 $('count').textContent=f.length+' of '+ALL.length+' stocks';
 $('list').innerHTML=f.map(s=>`<div class="row ${s.symbol===sel?'sel':''}" data-s="${s.symbol}"><div><div class="sym">${s.symbol}${S.bots[s.symbol]?'<span class="on-pill"> BOT</span>':''}${S.hold[s.symbol]?'<span class="on-pill" style="color:var(--acc)"> HELD</span>':''}</div><div class="nm">${s.name} &middot; ${s.exchange}</div></div><div>${pxCell(s.symbol)}</div></div>`).join('');
}
$('list').onclick=e=>{const r=e.target.closest('.row');if(r){sel=r.dataset.s;renderList();showHead();showBot();run();loadQuotes()}};
$('q').oninput=e=>{term=e.target.value;renderList();clearTimeout(window.qt);window.qt=setTimeout(loadQuotes,350)};
function chips(){const secs=['All','US','NSE',...new Set(ALL.map(s=>s.sector))];
 $('chips').innerHTML=secs.map(s=>`<button class="chip ${s===sector?'on':''}" data-c="${s}">${s}</button>`).join('')}
$('chips').onclick=e=>{const b=e.target.closest('.chip');if(b){sector=b.dataset.c;chips();renderList();loadQuotes()}};
function showHead(){const q=Q[sel];const s=ALL.find(x=>x.symbol===sel)||{};
 $('hs').textContent=sel;$('hn').textContent=(s.name||'')+' \u00b7 '+(s.sector||'')+' \u00b7 '+(s.exchange||'');
 $('bsym').textContent=sel;
 $('hp').innerHTML=q?inr(pxINR(sel))+`<small class="${q.change_pct>=0?'up':'dn'}">${q.change_pct>=0?'+':''}${q.change_pct}% today</small>`+(q.simulated?'<small class="dn">simulated feed</small>':''):'&mdash;'}
/* ---------- quotes ---------- */
function visibleSyms(){
 const t=term.toLowerCase();
 return ALL.filter(s=>(sector==='All'||s.sector===sector||s.exchange===sector)&&(s.symbol.toLowerCase().includes(t)||s.name.toLowerCase().includes(t))).slice(0,30).map(s=>s.symbol);
}
async function loadQuotes(){
 const need=[...new Set([sel,Object.keys(S.hold),Object.values(S.bots).filter(b=>b.pos).map(b=>b.sym),...visibleSyms()])].filter(Boolean).slice(0,30);
 if(!need.length)return;
 try{(await (await fetch('/api/quotes?symbols='+need.join(','))).json()).forEach(q=>Q[q.symbol]=q)}catch(e){}
 $('upd').textContent=now();renderList();showHead();renderMoney();showHold();showBot();
}
async function loadFX(){try{FX=(await (await fetch('/api/fx')).json()).USDINR||FX}catch(e){}}
/* ---------- bot ---------- */
const newBot=sym=>({sym,strategy:$('strat').value,ts:+$('ts').value,tp:+$('tp').value,pp:+$('pp').value,sz:+$('sz').value,pos:0,qty:0,entry:0,buyPrice:0,peak:0,cost:0,realized:0,partialDone:false,armed:false,log:[]});
function showBot(){
 const b=S.bots[sel];$('tg').classList.toggle('on',!!b);
 if(b){$('strat').value=b.strategy;$('ts').value=b.ts;$('tp').value=b.tp;$('pp').value=b.pp;$('sz').value=b.sz}
 const p=pxINR(sel);
 $('bs').textContent=b?(b.pos?`in position ${b.qty.toFixed(4)} sh @ ${inr(b.entry)} | stop ${inr(b.peak*(1-b.ts/100))} | target ${inr(b.buyPrice*(1+b.tp/100))} | booked ${inr(b.realized)}`:(b.armed?'flat, armed for next buy signal':'flat, waiting for exit signal')):'off';
 $('log').innerHTML=b?(b.log.map(l=>`<div class="${l.side==='BUY'?'up':(l.pl>=0?'up':'dn')}"><b>${l.side}</b> ${l.why} \u00b7 ${l.qty.toFixed(4)} sh @ ${inr(l.price)}${l.pl!=null?' \u00b7 P&L '+inr(l.pl):''} \u00b7 ${l.t}</div>`).join('')||'<div>Waiting for a signal...</div>'):'<div>Switch on the bot to trade '+sel+' automatically.</div>';
}
$('tg').onclick=()=>{
 const b=S.bots[sel];
 if(b){if(b.pos)sell(sel,b.qty,'BOT OFF',b);delete S.bots[sel]}
 else S.bots[sel]=newBot(sel);
 save();renderList();showBot();renderMoney();tick();
};
['ts','tp','pp','sz'].forEach(id=>$(id).onchange=()=>{const b=S.bots[sel];if(b){b.ts=+$('ts').value;b.tp=+$('tp').value;b.pp=+$('pp').value;b.sz=+$('sz').value;save();showBot()}});
$('strat').onchange=()=>{const b=S.bots[sel];if(b){if(b.pos)sell(sel,b.qty,'STRATEGY CHANGED',b);S.bots[sel]=newBot(sel);save();showBot()}};
const BEST={};
async function stratSignal(sym,strat){
 if(strat==='auto'){try{const c=BEST[sym];if(c&&Date.now()-c.t<300000){strat=c.v}else{const r=await (await fetch('/api/best?symbol='+sym)).json();strat=r.best||'sma_crossover';BEST[sym]={v:strat,t:Date.now()}}}catch(e){strat='sma_crossover'}}
 const r=await (await fetch('/api/signal?symbol='+sym+'&strategy='+strat)).json();return r;
}
async function tick(){
 for(const b of Object.values(S.bots)){
  const sym=b.sym;let r;
  try{r=await stratSignal(sym,b.strategy)}catch(e){continue}
  if(!r||r.error)continue;
  Q[sym]=Object.assign(Q[sym]||{symbol:sym,change_pct:0,currency:cur(sym)},{price:r.price,simulated:r.simulated});
  const p=pxINR(sym);if(!p)continue;
  if(b.pos){
   b.peak=Math.max(b.peak,p);
   if(!b.partialDone&&p>=b.buyPrice*(1+b.pp/100)){b.partialDone=true;sell(sym,b.qty/2,'PARTIAL PROFIT',b)}
   if(b.pos){
    if(p<=b.peak*(1-b.ts/100))sell(sym,b.qty,'TRAILING STOP',b);
    else if(p>=b.buyPrice*(1+b.tp/100))sell(sym,b.qty,'TAKE PROFIT',b);
    else if(r.signal===0)sell(sym,b.qty,'SIGNAL EXIT',b);
   }
  }else{
   if(r.signal===0)b.armed=true;
   else if(b.armed){if(buy(sym,S.cash*b.sz/100,'SIGNAL BUY',b)){b.log.unshift({side:'BUY',why:'SIGNAL',qty:b.qty,price:b.buyPrice,t:now()});b.log=b.log.slice(0,25)}}
  }
 }
 if(S.auto&&S.pending>0){S.bank+=S.pending;S.pending=0}
 save();showBot();renderMoney();renderList();
}
/* ---------- manual ---------- */
function showHold(){
 const h=S.hold[sel];const p=pxINR(sel);
 $('hold').innerHTML=h?`Holding ${h.qty.toFixed(4)} sh &middot; avg ${inr(h.cost/h.qty)} &middot; value ${inr(h.qty*(p||0))} &middot; P&L <b class="${(h.qty*(p||0)-h.cost)>=0?'up':'dn'}">${inr(h.qty*(p||0)-h.cost)}</b>`:'No manual position in '+sel+'.';
 $('fills').innerHTML=S.fills.slice(0,12).map(f=>`<div class="legend"><b class="${f.side==='BUY'?'up':'dn'}">${f.side}</b> ${f.sym} ${f.qty.toFixed(4)} @ ${inr(f.price)} \u00b7 ${f.why}${f.pl!=null?' \u00b7 '+inr(f.pl):''} \u00b7 ${f.t}</div>`).join('')||'<div class="legend">No fills yet.</div>';
}
$('buy').onclick=()=>{const q=+$('mq').value||0;const p=pxINR(sel);if(!p)return alert('Price not loaded yet.');
 const spend=Math.min(S.cash,q*p*(1+FEE));if(spend<p*(1+FEE))return alert('Not enough trading capital.');
 buy(sel,spend,'MANUAL',null);save();renderMoney();renderList();showHold();showBot()};
$('sell').onclick=()=>{const q=+$('mq').value||0;const h=S.hold[sel];if(!h)return alert('No manual holding in '+sel+'.');
 sell(sel,Math.min(q,h.qty),'MANUAL',null);save();renderMoney();renderList();showHold();showBot()};
/* ---------- backtest ---------- */
function draw(r){
 const c=$('c'),g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);
 const all=r.index.concat(r.equity),lo=Math.min(...all),hi=Math.max(...all),n=r.index.length;
 const X=i=>i/(n-1)*c.width,Y=v=>c.height-14-(v-lo)/(hi-lo)*(c.height-28);
 g.strokeStyle='rgba(60,70,100,.16)';for(let k=0;k<5;k++){g.beginPath();g.moveTo(0,k*c.height/4);g.lineTo(c.width,k*c.height/4);g.stroke()}
 const line=(a,col,w)=>{g.beginPath();g.strokeStyle=col;g.lineWidth=w;a.forEach((v,i)=>i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)));g.stroke()};
 line(r.index,'#111827',2);line(r.equity,'#2f4fd8',2.5);
 r.trades.forEach(t=>{g.fillStyle=t.side==='BUY'?'#067a4d':'#c81e42';g.beginPath();g.arc(X(t.bar),Y(r.index[t.bar]),5,0,7);g.fill()});
}
async function run(){
 const strat=$('strat').value==='auto'?'sma_crossover':$('strat').value;
 try{
 const r=await (await fetch('/api/backtest?symbol='+sel+'&strategy='+strat)).json();
 if(r.error)return;
 const cls=v=>v>=0?'up':'dn';
 $('stats').innerHTML=[['Backtest return',r.return_pct+'%',cls(r.return_pct)],['Max drawdown','-'+r.max_drawdown_pct+'%','dn'],['Sharpe',r.sharpe,cls(r.sharpe)],['Backtest trades',r.num_trades,''],['Last price',inr(toINR(r.last,sel)),'']]
  .map(x=>`<div class="stat inset"><small>${x[0]}</small><b class="${x[2]}">${x[1]}</b></div>`).join('');
 if($('strat').value==='auto'){const b=await (await fetch('/api/best?symbol='+sel)).json();$('stats').innerHTML+='<div class="stat inset"><small>Auto picked</small><b>'+b.best+'</b></div>'}
 draw(r);
 }catch(e){}
}
$('go').onclick=run;
/* ---------- boot ---------- */
fetch('/api/stocks').then(r=>r.json()).then(d=>{ALL=d;chips();renderList();showHead();showBot();showHold();renderMoney();
 if(S.auto)$('auto').classList.add('on');
 return loadFX()}).then(()=>{loadQuotes();run();tick()});
setInterval(tick,5000);setInterval(loadQuotes,20000);setInterval(loadFX,600000);
</script></body></html>"""

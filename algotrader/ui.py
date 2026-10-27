PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AlgoTrader India - paper trading</title>
<style>
:root{--bg:#e8ecf4;--hi:#fff;--lo:#c2c9d8;--txt:#0f172a;--mut:#48526b;--acc:#2f4fd8;--up:#067a4d;--dn:#c81e42;--gold:#8a6a00}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;font-size:15px;line-height:1.45;-webkit-font-smoothing:antialiased}
.raised{background:var(--bg);border-radius:20px;box-shadow:8px 8px 18px var(--lo),-8px -8px 18px var(--hi)}
.inset{background:var(--bg);border-radius:14px;box-shadow:inset 4px 4px 9px var(--lo),inset -4px -4px 9px var(--hi)}
header{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;padding:14px 22px;margin:18px auto 0;max-width:1440px}
header h1{font-size:20px;margin:0;font-weight:800}
header h1 .sub{font-size:12px;color:var(--mut);font-weight:600;margin-left:8px}
.bank{font-size:11.5px;color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.4px}
.bank b{display:block;font-size:17px;color:var(--txt);letter-spacing:0;text-transform:none}
.tag{font-size:10.5px;font-weight:900;letter-spacing:.8px;text-transform:uppercase;color:var(--gold);padding:4px 10px;border-radius:99px;display:inline-block;margin-top:6px}
nav.tabs{display:flex;gap:10px;padding:10px;margin:14px auto;max-width:1440px;flex-wrap:wrap}
.tab{padding:9px 18px;border-radius:99px;font-weight:800;font-size:13.5px}
button{font:inherit;font-weight:700;color:var(--txt);background:var(--bg);border:0;border-radius:13px;padding:9px 15px;cursor:pointer;box-shadow:4px 4px 9px var(--lo),-4px -4px 9px var(--hi)}
button:active{box-shadow:inset 3px 3px 7px var(--lo),inset -3px -3px 7px var(--hi)}
button.on{box-shadow:inset 3px 3px 7px var(--lo),inset -3px -3px 7px var(--hi);color:var(--acc)}
button.go{color:#fff;background:var(--acc)}button.dgr{color:#fff;background:var(--dn)}
input,select{font:inherit;font-weight:600;color:var(--txt);background:var(--bg);border:0;border-radius:12px;padding:9px 12px;outline:none;box-shadow:inset 4px 4px 8px var(--lo),inset -4px -4px 8px var(--hi)}
input::placeholder{color:var(--mut);font-weight:500}
main{display:grid;grid-template-columns:340px 1fr;gap:22px;max-width:1440px;margin:0 auto 40px;padding:0 18px}
@media(max-width:1000px){main{grid-template-columns:1fr}}
.side{padding:16px;display:flex;flex-direction:column;height:calc(100vh - 190px);min-height:480px}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0}
.chip{padding:4px 11px;font-size:12px;border-radius:99px}
#list{overflow:auto;flex:1;padding-right:4px}
.row{display:flex;justify-content:space-between;gap:8px;align-items:center;padding:10px 12px;margin-bottom:8px;border-radius:14px;cursor:pointer;box-shadow:3px 3px 8px var(--lo),-3px -3px 8px var(--hi)}
.row.sel{box-shadow:inset 3px 3px 8px var(--lo),inset -3px -3px 8px var(--hi)}
.sym{font-weight:800;font-size:14.5px}.nm{font-size:11.5px;color:var(--mut)}
.px{text-align:right;font-size:13.5px;font-weight:800}.chg{font-size:11.5px;font-weight:700}
.on-pill{font-size:9.5px;font-weight:900;color:var(--up);letter-spacing:.5px}
.panel{padding:22px}
.top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}
.badge{display:inline-block;font-size:10.5px;font-weight:900;letter-spacing:.6px;text-transform:uppercase;color:var(--acc);padding:3px 9px;border-radius:99px;margin-bottom:4px}
.top h2{margin:0;font-size:27px;font-weight:800;line-height:1.1}
.big{font-size:29px;font-weight:800}.big small{font-size:13px;font-weight:800;margin-left:9px}
.ctl{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
.profitbox{padding:18px;border-radius:18px;margin:16px 0;box-shadow:inset 5px 5px 12px var(--lo),inset -5px -5px 12px var(--hi)}
.profitbox h3{margin:0 0 6px;font-size:14.5px}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:12px;margin:12px 0}
.pcell small{display:block;color:var(--mut);font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.3px}
.pcell b{font-size:18px;font-weight:800;overflow-wrap:anywhere;display:block;line-height:1.25}
.rowbtns{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
canvas{width:100%;height:270px;border-radius:16px}
.legend{font-size:12px;color:var(--mut)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
@media(max-width:820px){.grid2{grid-template-columns:1fr}}
.card{padding:16px;border-radius:16px}.card h3{margin:0 0 10px;font-size:14px}
.cfg{display:flex;gap:9px;flex-wrap:wrap;margin:6px 0}
.cfg label{font-size:10.5px;font-weight:800;color:var(--mut);text-transform:uppercase;letter-spacing:.3px}
.cfg input,.cfg select{display:block;width:86px;margin-top:3px}
#log{max-height:132px;overflow:auto;font-size:12px;margin-top:8px}
#log div{padding:4px 0;border-bottom:1px solid var(--lo)}
#pos div,#sugg div{padding:6px 0;border-bottom:1px solid var(--lo);font-size:12.5px}
#fills div{padding:4px 0;font-size:12px;border-bottom:1px solid var(--lo)}
.up{color:var(--up)}.dn{color:var(--dn)}
.sw{display:flex;align-items:center;gap:8px;font-weight:700;font-size:13px}
.tg{width:54px;height:28px;border-radius:99px;position:relative;padding:0}
.tg i{position:absolute;top:4px;left:5px;width:20px;height:20px;border-radius:50%;background:var(--bg);box-shadow:3px 3px 6px var(--lo),-2px -2px 5px var(--hi);transition:.2s}
.tg.on i{left:29px;background:var(--up)}
.mk{font-size:9.5px;font-weight:900;letter-spacing:.5px;padding:2px 6px;border-radius:5px;background:rgba(47,79,216,.12);color:var(--acc)}
</style></head><body>
<header class="raised">
 <div><h1>&#9670; AlgoTrader India <span class="sub">paper trading desk</span></h1><div class="tag inset">Simulated money &middot; real market data</div></div>
 <div class="bank">Capital<b id="cap">&#8377;1,00,00,000</b></div>
 <div class="bank">Bank account<b id="bankh">&#8377;0</b></div>
 <div class="bank">Booked P&amp;L<b id="net">&#8377;0</b></div>
 <div class="bank">Updated<b id="upd">--</b></div>
 <button id="rst">Reset</button>
</header>
<nav class="tabs raised">
 <button class="tab on" data-m="IN">India &middot; NSE + BSE + F&amp;O</button>
 <button class="tab" data-m="US">US stocks</button>
 <button class="tab" data-m="CRYPTO">Bitcoin &amp; crypto</button>
 <button class="tab" data-m="BEST">Best trades now</button>
</nav>
<main>
 <aside class="raised side">
  <input id="q" placeholder="Search stocks, indices, futures, options">
  <div class="chips" id="chips"></div>
  <div id="list"></div>
  <div class="legend" id="count"></div>
 </aside>
 <section class="raised panel">
  <div class="top">
   <div><span class="badge" id="badge"></span><h2 id="hs">-</h2><div class="nm" id="hn"></div><div class="big" id="hp"></div></div>
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
    <button class="go" id="quick">Start algo</button>
   </div>
  </div>
  <div class="profitbox">
   <h3>Profit box &mdash; booked in real time</h3>
   <div class="pgrid" id="pbox"></div>
   <div class="rowbtns">
    <button class="go" id="xfer">Transfer profits to bank</button>
    <div class="sw"><span>Auto-transfer</span><button class="tg inset" id="auto"><i></i></button></div>
    <button class="dgr" id="closeall">Close all positions</button>
   </div>
  </div>
  <canvas id="c" width="1000" height="270"></canvas>
  <div class="legend" id="clegend"></div>
  <div class="grid2">
   <div class="card inset"><h3>Best trades now &mdash; <span id="bmkt" class="legend"></span></h3><div id="sugg"></div></div>
   <div class="card inset"><h3>Open positions</h3><div id="pos"></div></div>
  </div>
  <div class="grid2">
   <div class="card inset">
    <h3>Algo trading &mdash; <span id="bs" class="legend"></span></h3>
    <div class="cfg">
     <label>Trailing %<input id="ts" type="number" value="2.5" min="0.3" step="0.1"></label>
     <label>Target %<input id="tp" type="number" value="6" min="0.5" step="0.5"></label>
     <label>Partial %<input id="pp" type="number" value="3" min="0.5" step="0.5"></label>
     <label>Size %<input id="sz" type="number" value="10" min="1" max="100"></label>
     <label>Mode<select id="mode"><option value="both">Long + short</option><option value="long">Long only</option></select></label>
    </div>
    <div class="sw"><span>Start algo on <span id="bsym">-</span></span><button class="tg inset" id="tg"><i></i></button></div>
    <div class="legend" id="bhint" style="margin-top:6px"></div>
    <div id="log"></div>
   </div>
   <div class="card inset">
    <h3>Manual order &mdash; 1% commission</h3>
    <div class="cfg"><label>Qty / lots<input id="mq" type="number" value="10" min="1" step="1"></label></div>
    <div class="rowbtns"><button class="go" id="buy">BUY / LONG</button><button class="dgr" id="short">SHORT</button><button id="close1">CLOSE</button></div>
    <div class="legend" id="hold" style="margin-top:8px"></div>
    <h3 style="margin-top:14px">Recent fills</h3><div id="fills"></div>
   </div>
  </div>
  <div class="legend" style="margin-top:12px">Paper orders at live delayed prices. No real money, no broker. 1% commission on every fill. Futures use 12% margin, options trade at premium. Not financial advice.</div>
 </section>
</main>
<script>
const $=id=>document.getElementById(id);
const CAP=1e7, FEE=0.01, MAXBOTS=8;
const inr=v=>'\u20b9'+Number(v||0).toLocaleString('en-IN',{maximumFractionDigits:2});
const now=()=>new Date().toLocaleTimeString();
let ALL=[],INSTR={},sel='RELIANCE',market='IN',ftype='All',term='',Q={},FX=95.2,SUGG=[],BESTC=[];
let S=JSON.parse(localStorage.getItem('sim3')||'null')||{cash:CAP,bank:0,gross:0,net:0,fee:0,pending:0,sells:0,wins:0,auto:false,bots:{},hold:{},fills:[]};
const save=()=>localStorage.setItem('sim3',JSON.stringify(S));
const curOf=s=>(INSTR[s]||{}).currency||'INR';
const px=s=>{const q=Q[s];if(!q)return null;return curOf(s)==='INR'?q.price:q.price*FX};
const unitOf=s=>(INSTR[s]||{}).unit||1;
const margOf=s=>(INSTR[s]||{}).margin||1;
function fill(side,sym,qty,price,why,pl){S.fills.unshift({side,sym,qty,price,why,pl,t:now()});S.fills=S.fills.slice(0,40)}
/* ---------------- trading core ---------------- */
function openTrade(sym,side,qty,why,bot){
 const p=px(sym); if(!p||qty<=0) return false;
 const per=p*unitOf(sym)*margOf(sym), blocked=qty*per, fee=blocked*FEE;
 if(blocked+fee>S.cash+1e-6) return false;
 S.cash-=blocked+fee; S.fee+=fee;
 if(bot){Object.assign(bot,{pos:1,side,qty,entry:p,blocked,best:p,partialDone:false,cd:0});
  bot.log.unshift({side:side==='LONG'?'BUY':'SHORT',why,qty,price:p,t:now()}); bot.log=bot.log.slice(0,20)}
 else S.hold[sym]={sym,side,qty,entry:p,blocked};
 fill(side==='LONG'?'BUY':'SHORT',sym,qty,p,why,null);
 return true;
}
function closeTrade(r,why,price,frac){
 if(!r||r.qty<=0) return;
 const p=price||px(r.sym); if(!p) return;
 const q=r.qty*(frac||1);
 const pnl=(r.side==='LONG'?p-r.entry:r.entry-p)*q*unitOf(r.sym);
 const blocked=r.blocked*(q/r.qty), fee=blocked*FEE;
 S.cash+=blocked+pnl-fee; S.fee+=fee; S.gross+=pnl; S.net+=pnl-fee; S.pending+=pnl-fee; S.sells++;
 if(pnl-fee>0)S.wins++;
 r.qty-=q; r.blocked-=blocked;
 if(r.log){ r.realized=(r.realized||0)+pnl-fee;
  r.log.unshift({side:r.side==='LONG'?'SELL':'COVER',why,qty:q,price:p,pl:pnl-fee,t:now()}); r.log=r.log.slice(0,20);
  if(r.qty<=1e-9){r.pos=0;r.qty=0;r.blocked=0;r.side='';r.cd=3} }
 else if(r.qty<=1e-9) delete S.hold[r.sym];
 fill(r.side==='LONG'?'SELL':'COVER',r.sym,q, p,why,pnl-fee);
}
function invested(){let v=0;for(const s in S.hold)v+=S.hold[s].blocked;for(const s in S.bots)v+=S.bots[s].blocked||0;return v}
function unrealized(){let v=0;const add=r=>{const p=px(r.sym);if(!p)return;v+=(r.side==='LONG'?p-r.entry:r.entry-p)*r.qty*unitOf(r.sym)};
 Object.values(S.hold).forEach(add);Object.values(S.bots).filter(b=>b.pos).forEach(add);return v}
/* ---------------- money render ---------------- */
function renderMoney(){
 $('cap').textContent=inr(CAP); $('bankh').textContent=inr(S.bank); $('net').textContent=inr(S.net);
 $('net').className=S.net>=0?'up':'dn';
 const w=S.sells?(S.wins/S.sells*100).toFixed(0):'0';
 $('pbox').innerHTML=[['Net booked P&L',inr(S.net),S.net>=0?'up':'dn'],['Gross P&L',inr(S.gross),S.gross>=0?'up':'dn'],
  ['Commission',inr(S.fee),'dn'],['Pending transfer',inr(S.pending),S.pending>=0?'up':'dn'],['Moved to bank',inr(S.bank),'up'],
  ['Win rate',w+'% ('+S.wins+'/'+S.sells+')',''],['Free capital',inr(S.cash),''],
  ['Open positions',inr(invested())+' <span class="'+(unrealized()>=0?'up':'dn')+'">'+(unrealized()>=0?'+':'')+inr(unrealized())+'</span>','']]
  .map(x=>`<div class="pcell"><small>${x[0]}</small><b class="${x[2]}">${x[1]}</b></div>`).join('');
 $('auto').classList.toggle('on',S.auto);
}
$('xfer').onclick=()=>{if(!S.pending)return alert('No booked profit to transfer yet.');
 if(!confirm('Move '+inr(S.pending)+' of booked P&L to the simulated bank account?'))return;
 S.bank+=S.pending;S.pending=0;save();renderMoney()};
$('auto').onclick=()=>{S.auto=!S.auto;save();renderMoney()};
$('rst').onclick=()=>{if(confirm('Reset capital, bots, positions and profits?')){localStorage.removeItem('sim3');location.reload()}};
$('closeall').onclick=()=>{Object.keys(S.hold).forEach(k=>closeTrade(S.hold[k],'CLOSE ALL'));
 Object.values(S.bots).forEach(b=>{if(b.pos)closeTrade(b,'CLOSE ALL')});save();renderAll()};
/* ---------------- list ---------------- */
function items(){
 const t=term.toLowerCase();
 let rows=ALL.filter(i=>i.market===market);
 if(ftype!=='All')rows=rows.filter(i=>i.type===ftype);
 return rows.filter(i=>i.symbol.toLowerCase().includes(t)||i.name.toLowerCase().includes(t));
}
function pxCell(s){const q=Q[s];if(!q)return '<span class="nm">...</span>';const c=q.change_pct>=0?'up':'dn';
 return `<div class="px">${inr(px(s))}</div><div class="chg ${c}">${q.change_pct>=0?'+':''}${q.change_pct}%</div>`}
function renderList(){
 if(market==='BEST'){
  $('count').textContent=BESTC.length+' ranked trades across India, US and crypto';
  $('list').innerHTML=BESTC.map((s,i)=>`<div class="row ${s.symbol===sel?'sel':''}" data-s="${s.symbol}"><div><div class="sym">${i+1}. ${s.symbol} <span class="mk">${s.action}</span></div><div class="nm">${s.name}</div></div><div>${pxCell(s.symbol)}</div></div>`).join('')||'<div class="legend">Scanning…</div>';
  return;
 }
 const f=items();
 $('count').textContent=f.length+' of '+ALL.filter(i=>i.market===market).length+' instruments';
 $('list').innerHTML=f.slice(0,150).map(i=>`<div class="row ${i.symbol===sel?'sel':''}" data-s="${i.symbol}"><div><div class="sym">${i.symbol}${S.bots[i.symbol]?'<span class="on-pill"> BOT</span>':''}${S.hold[i.symbol]?'<span class="on-pill" style="color:var(--acc)"> HELD</span>':''}</div><div class="nm">${i.name} &middot; ${i.exchange}</div></div><div>${pxCell(i.symbol)}</div></div>`).join('');
}
$('list').onclick=e=>{const r=e.target.closest('.row');if(r){sel=r.dataset.s;renderList();showAll();run();loadQuotes()}};
$('q').oninput=e=>{term=e.target.value;renderList();clearTimeout(window.qt);window.qt=setTimeout(loadQuotes,350)};
const TYPES={IN:['All','STOCK','INDEX','FUT','OPT'],US:['All'],CRYPTO:['All'],BEST:[]};
function chips(){
 const t=TYPES[market]||['All'];
 const names={All:'All',STOCK:'Stocks',INDEX:'Indices',FUT:'Futures',OPT:'Options'};
 $('chips').innerHTML=t.map(x=>`<button class="chip ${x===ftype?'on':''}" data-c="${x}">${names[x]||x}</button>`).join('');
}
$('chips').onclick=e=>{const b=e.target.closest('.chip');if(b){ftype=b.dataset.c;chips();renderList();loadQuotes()}};
function showHead(){const q=Q[sel],i=INSTR[sel]||{};
 $('hs').textContent=sel;$('hn').textContent=(i.name||'')+' \u00b7 '+(i.exchange||'')+(i.type&&i.type!=='STOCK'?' \u00b7 '+i.type:'');
 $('badge').textContent=i.market==='IN'?'India '+(i.exchange||''):(i.market||'');
 $('bsym').textContent=sel;
 $('hp').innerHTML=q?inr(px(sel))+`<small class="${q.change_pct>=0?'up':'dn'}">${q.change_pct>=0?'+':''}${q.change_pct}% today</small>`+(q.simulated?'<small class="dn">simulated</small>':''):'&mdash;';
 $('clegend').textContent=(i.type==='OPT'?'Underlying '+(i.underlying||''):'Price')+' indexed to 100, 1 year \u00b7 Blue: strategy equity \u00b7 dots: backtest fills';
}
/* ---------------- quotes ---------------- */
async function loadQuotes(){
 const need=[...new Set([sel,Object.keys(S.hold),...Object.values(S.bots).filter(b=>b.pos).map(b=>b.sym),...items().slice(0,30).map(i=>i.symbol),...BESTC.slice(0,10).map(s=>s.symbol)])].filter(Boolean).slice(0,30);
 if(!need.length)return;
 try{(await (await fetch('/api/quotes?symbols='+need.join(','))).json()).forEach(q=>Q[q.symbol]=q)}catch(e){}
 $('upd').textContent=now();renderList();showHead();renderMoney();showAll();
}
async function loadFX(){try{FX=(await (await fetch('/api/fx')).json()).USDINR||FX}catch(e){}}
/* ---------------- positions / suggestions ---------------- */
function posRow(r,key){const p=px(r.sym);const pl=p?((r.side==='LONG'?p-r.entry:r.entry-p)*r.qty*unitOf(r.sym)):0;
 return `<div><b>${r.sym}</b> <span class="mk">${r.side}</span> ${r.qty.toFixed(2)} @ ${inr(r.entry)} \u00b7 LTP ${p?inr(p):'-'} \u00b7 <b class="${pl>=0?'up':'dn'}">${inr(pl)}</b> <button data-x="${key}" style="padding:2px 8px;font-size:11px">Close</button></div>`}
function renderPos(){
 const rows=[];
 for(const s in S.hold)rows.push(posRow(S.hold[s],'h:'+s));
 for(const s in S.bots)if(S.bots[s].pos)rows.push(posRow(S.bots[s],'b:'+s));
 $('pos').innerHTML=rows.join('')||'<div class="legend">No open positions. Start an algo or place a manual order.</div>';
}
$('pos').onclick=e=>{const b=e.target.closest('button[data-x]');if(!b)return;const [k,s]=b.dataset.x.split(':');
 closeTrade(k==='h'?S.hold[s]:S.bots[s],'MANUAL CLOSE');save();renderAll()};
function renderSugg(){
 $('bmkt').textContent=market==='BEST'?'India + US + crypto':(market==='IN'?'India':market==='US'?'US':'Crypto');
 const rows=(market==='BEST'?BESTC:SUGG);
 $('sugg').innerHTML=rows.slice(0,7).map(s=>{
  const tgt=s.price*(1+6/100), stp=s.price*(1-2.5/100), mk=s.market==='IN'?'NSE':s.market;
  return `<div><b>${s.symbol}</b> <span class="mk">${mk}</span> <span class="${s.action==='BUY'?'up':'dn'}"><b>${s.action}</b></span> \u00b7 ${s.strategy} \u00b7 3m ${s.ret_3m>0?'+':''}${s.ret_3m}%<br>
  <span class="legend">${inr(s.price)} \u00b7 target ${inr(tgt)} \u00b7 stop ${inr(stp)}</span> <button data-start="${s.symbol}" data-strat="${s.strategy}" style="padding:2px 9px;font-size:11px">Start algo</button></div>`}).join('')||'<div class="legend">Scanning the market…</div>';
 $('sugg').innerHTML+=`<div style="padding-top:8px"><button class="go" id="top5">Start algo on top 5 trades</button></div>`;
}
$('sugg').onclick=e=>{const b=e.target.closest('button[data-start]');
 if(b){startAlgo(b.dataset.start,b.dataset.strat);return}
 if(e.target.id==='top5'){
  const pick=(market==='BEST'?BESTC:SUGG).filter(s=>s.action==='BUY').slice(0,5);
  if(!pick.length)return alert('No buy signals right now.');
  pick.forEach(s=>startAlgo(s.symbol,s.strategy,true));
  save();renderAll();alert('Algo started on: '+pick.map(s=>s.symbol).join(', '));
 }
};
/* ---------------- bots ---------------- */
function newBot(sym,strat){return {sym,strategy:strat||$('strat').value||'auto',ts:+$('ts').value||2.5,tp:+$('tp').value||6,pp:+$('pp').value||3,sz:+$('sz').value||10,mode:$('mode').value||'both',pos:0,side:'',qty:0,entry:0,blocked:0,best:0,partialDone:false,cd:0,realized:0,log:[]}}
function startAlgo(sym,strat,quiet){
 if(Object.keys(S.bots).length>=MAXBOTS&&!S.bots[sym]){if(!quiet)alert('Max '+MAXBOTS+' bots at once. Stop one first.');return}
 if(S.bots[sym])return;
 S.bots[sym]=newBot(sym,strat);
 save(); if(!quiet){sel=sym;renderList();showAll()} tickBot(S.bots[sym]);
}
$('quick').onclick=()=>{if(S.bots[sel])return alert('Algo already running on '+sel+'.');startAlgo(sel,$('strat').value)};
$('tg').onclick=()=>{const b=S.bots[sel];if(b){if(b.pos)closeTrade(b,'BOT OFF');delete S.bots[sel];save();renderAll()}
 else startAlgo(sel,$('strat').value)};
['ts','tp','pp','sz','mode'].forEach(id=>$(id).onchange=()=>{const b=S.bots[sel];if(!b)return;
 b.ts=+$('ts').value||b.ts;b.tp=+$('tp').value||b.tp;b.pp=+$('pp').value||b.pp;b.sz=+$('sz').value||b.sz;b.mode=$('mode').value||b.mode;save();showBot()});
$('strat').onchange=()=>{const b=S.bots[sel];if(b){if(b.pos)closeTrade(b,'STRATEGY CHANGE');S.bots[sel]=newBot(sel,$('strat').value);save();renderAll()}};
function showBot(){
 const b=S.bots[sel];$('tg').classList.toggle('on',!!b);
 if(b){$('strat').value=b.strategy;$('ts').value=b.ts;$('tp').value=b.tp;$('pp').value=b.pp;$('sz').value=b.sz;$('mode').value=b.mode}
 $('bs').textContent=b?(b.pos?`in ${b.side} ${b.qty.toFixed(2)} @ ${inr(b.entry)} | trail ${inr(b.best*(1-b.ts/100))} | target ${inr(b.entry*(1+b.tp/100))} | booked ${inr(b.realized||0)}`:(b.cd>0?'cooling down after exit':'flat and ready')):'off';
 $('bhint').textContent=b?(b.pos?'':'Watching for the next signal; long+short mode enters on either side.'):'Turn this on (or press Start algo) to trade '+sel+' automatically.';
 $('log').innerHTML=b?(b.log.map(l=>`<div class="${l.pl==null?'':(l.pl>=0?'up':'dn')}"><b>${l.side}</b> ${l.why} \u00b7 ${l.qty.toFixed(2)} @ ${inr(l.price)}${l.pl!=null?' \u00b7 '+inr(l.pl):''} \u00b7 ${l.t}</div>`).join('')||'<div>No fills yet.</div>'):'<div>Algo off.</div>';
}
const BESTCACHE={};
async function bestFor(sym){const c=BESTCACHE[sym];if(c&&Date.now()-c.t<300000)return c.v;
 try{const r=await (await fetch('/api/best?symbol='+sym)).json();BESTCACHE[sym]={v:r.best||'sma_crossover',t:Date.now()};return BESTCACHE[sym].v}catch(e){return 'sma_crossover'}}
async function tickBot(b){
 try{
  const strat=b.strategy==='auto'?await bestFor(b.sym):b.strategy;
  const r=await (await fetch('/api/signal?symbol='+encodeURIComponent(b.sym)+'&strategy='+strat)).json();
  if(!r||r.error)return;
  Q[b.sym]=Object.assign(Q[b.sym]||{symbol:b.sym,change_pct:0,currency:curOf(b.sym)},{price:r.price,simulated:r.simulated});
  const p=px(b.sym);if(!p)return;
  if(!b.pos){
   if(b.cd>0){b.cd--;return}
   const dir=r.signal===1?'LONG':(b.mode==='both'?'SHORT':null);
   if(!dir)return;
   const budget=S.cash*b.sz/100, per=p*unitOf(b.sym)*margOf(b.sym);
   openTrade(b.sym,dir,budget/(per*(1+FEE)),dir==='LONG'?'SIGNAL BUY':'SIGNAL SHORT',b);
  }else{
   const long=b.side==='LONG';
   b.best=long?Math.max(b.best,p):Math.min(b.best,p);
   if(!b.partialDone&&(long?p>=b.entry*(1+b.pp/100):p<=b.entry*(1-b.pp/100))){b.partialDone=true;closeTrade(b,'PARTIAL PROFIT',p,0.5)}
   if(b.pos){
    if(long?p<=b.best*(1-b.ts/100):p>=b.best*(1+b.ts/100))closeTrade(b,long?'TRAILING STOP':'TRAILING STOP',p);
    else if(long?p>=b.entry*(1+b.tp/100):p<=b.entry*(1-b.tp/100))closeTrade(b,'TAKE PROFIT',p);
    else if((long&&r.signal===0)||(!long&&r.signal===1))closeTrade(b,'SIGNAL FLIP',p);
   }
  }
 }catch(e){}
}
async function tick(){for(const b of Object.values(S.bots))await tickBot(b);
 if(S.auto&&S.pending>0){S.bank+=S.pending;S.pending=0}
 save();renderMoney();showBot();renderPos();renderList()}
/* ---------------- manual ---------------- */
function showHold(){const h=S.hold[sel],p=px(sel);
 $('hold').innerHTML=h?`<b>${h.side}</b> ${h.qty.toFixed(2)} @ ${inr(h.entry)} \u00b7 value ${inr(h.qty*unitOf(sel)*(p||0)*margOf(sel))} \u00b7 P&L <b class="${(h.side==='LONG'?p-h.entry:h.entry-p)>=0?'up':'dn'}">${inr((h.side==='LONG'?p-h.entry:h.entry-p)*h.qty*unitOf(sel))}</b>`:'No manual position in '+sel+'.';
 $('fills').innerHTML=S.fills.slice(0,10).map(f=>`<div><b class="${f.side==='BUY'?'up':'dn'}">${f.side}</b> ${f.sym} ${f.qty.toFixed(2)} @ ${inr(f.price)} \u00b7 ${f.why}${f.pl!=null?' \u00b7 '+inr(f.pl):''}</div>`).join('')||'<div class="legend">No fills yet.</div>';
}
$('buy').onclick=()=>manual('LONG');$('short').onclick=()=>manual('SHORT');
$('close1').onclick=()=>{const h=S.hold[sel];if(!h)return alert('No manual position in '+sel+'.');closeTrade(h,'MANUAL CLOSE');save();renderAll()};
function manual(side){
 const q=+$('mq').value||0; if(q<=0)return alert('Enter a quantity.');
 if(!px(sel))return alert('Price not loaded yet.');
 if(S.hold[sel])return alert('Close the existing manual position in '+sel+' first.');
 if(!openTrade(sel,side,q,'MANUAL',null))return alert('Not enough free capital.');
 save();renderAll();
}
function renderAll(){renderMoney();renderList();showHead();showBot();showHold();renderPos();renderSugg()}
const showAll=renderAll;
/* ---------------- chart / backtest ---------------- */
function draw(r){
 const c=$('c'),g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);
 const all=r.index.concat(r.equity),lo=Math.min(...all),hi=Math.max(...all),n=r.index.length;
 const X=i=>i/(n-1)*c.width,Y=v=>c.height-12-(v-lo)/(hi-lo)*(c.height-24);
 g.strokeStyle='rgba(60,70,100,.16)';for(let k=0;k<5;k++){g.beginPath();g.moveTo(0,k*c.height/4);g.lineTo(c.width,k*c.height/4);g.stroke()}
 const line=(a,col,w)=>{g.beginPath();g.strokeStyle=col;g.lineWidth=w;a.forEach((v,i)=>i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)));g.stroke()};
 line(r.index,'#0f172a',2);line(r.equity,'#2f4fd8',2.5);
 r.trades.forEach(t=>{g.fillStyle=t.side==='BUY'?'#067a4d':'#c81e42';g.beginPath();g.arc(X(t.bar),Y(r.index[t.bar]),4.5,0,7);g.fill()});
}
async function run(){
 if(market==='BEST')return;
 try{
  const strat=$('strat').value==='auto'?(S.bots[sel]&&S.bots[sel].strategy!=='auto'?S.bots[sel].strategy:await bestFor(sel)):$('strat').value;
  const r=await (await fetch('/api/backtest?symbol='+encodeURIComponent(sel)+'&strategy='+strat)).json();
  if(r.error)return;
  const cls=v=>v>=0?'up':'dn';
  $('pbox').setAttribute('data-bt',r.return_pct);
  draw(r);
  const extra=document.getElementById('btstats');
  if(!extra){const d=document.createElement('div');d.id='btstats';d.className='legend';d.style.marginTop='6px';$('clegend').after(d)}
  document.getElementById('btstats').innerHTML=`Backtest (${strat}, 1 year): <b class="${cls(r.return_pct)}">${r.return_pct}%</b> return \u00b7 max drawdown ${r.max_drawdown_pct}% \u00b7 Sharpe ${r.sharpe} \u00b7 ${r.num_trades} trades`;
 }catch(e){}
}
$('go').onclick=run;
/* ---------------- scan ---------------- */
async function loadScan(){
 try{
  if(market==='BEST'){
   const parts=await Promise.all(['IN','US','CRYPTO'].map(m=>fetch('/api/scan?market='+m+'&limit=8').then(r=>r.json()).catch(()=>[])));
   BESTC=parts.flat().sort((a,b)=>b.score-a.score).slice(0,14);
  }else{SUGG=await (await fetch('/api/scan?market='+market+'&limit=8')).json()}
 }catch(e){}
 renderSugg();renderList();
}
/* ---------------- boot ---------------- */
function setTab(m){market=m;ftype='All';chips();renderList();renderSugg();loadQuotes();
 document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.m===m));
 if(m==='BEST')loadScan();
 if(m==='BEST'){const f=ALL.filter(i=>i.market==='IN')[0];if(f&&!INSTR[sel])sel=f.symbol}}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>setTab(t.dataset.m));
async function boot(){
 ALL=await (await fetch('/api/instruments')).json();
 ALL.forEach(i=>INSTR[i.symbol]=i);
 sel=ALL.find(i=>i.symbol==='RELIANCE')?  'RELIANCE' : (ALL[0]&&ALL[0].symbol);
 chips();renderList();showHead();showAll();renderMoney();
 await loadFX();loadQuotes();run();loadScan();
 Object.values(S.bots).forEach(b=>tickBot(b));
}
boot();
setInterval(tick,4000);setInterval(loadQuotes,15000);setInterval(loadScan,90000);setInterval(loadFX,600000);
</script></body></html>
'''

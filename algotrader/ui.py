PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AlgoTrader</title>
<style>
:root{--glass:rgba(255,255,255,.14);--edge:rgba(255,255,255,.38);--txt:#fff;--mut:rgba(255,255,255,.72);--up:#6ef3b0;--dn:#ff8aa0}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;color:var(--txt);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;
 background:radial-gradient(circle at 15% 20%,#5ee7ff 0,transparent 40%),radial-gradient(circle at 85% 15%,#b69cff 0,transparent 42%),
 radial-gradient(circle at 70% 90%,#7dffd6 0,transparent 45%),radial-gradient(circle at 10% 90%,#ffb5e8 0,transparent 40%),linear-gradient(135deg,#1e6fd9,#6a4bd8);background-attachment:fixed}
.glass{background:var(--glass);backdrop-filter:blur(22px) saturate(180%);-webkit-backdrop-filter:blur(22px) saturate(180%);
 border:1px solid var(--edge);border-radius:22px;box-shadow:0 8px 32px rgba(20,30,90,.28),inset 0 1px 0 rgba(255,255,255,.5)}
header{display:flex;justify-content:space-between;align-items:center;padding:14px 22px;margin:18px auto;max-width:1300px}
header h1{font-size:20px;margin:0;letter-spacing:.5px}
.pill{font-size:12px;padding:5px 12px;border-radius:99px;background:rgba(255,255,255,.2);border:1px solid var(--edge)}
main{display:grid;grid-template-columns:360px 1fr;gap:18px;max-width:1300px;margin:0 auto 30px;padding:0 18px}
@media(max-width:860px){main{grid-template-columns:1fr}}
.side{padding:16px;display:flex;flex-direction:column;height:calc(100vh - 120px);min-height:420px}
input,select,button{font:inherit;color:var(--txt);background:rgba(255,255,255,.16);border:1px solid var(--edge);border-radius:12px;padding:9px 12px;outline:none}
input::placeholder{color:var(--mut)}select option{color:#123}
button{cursor:pointer;font-weight:600;transition:.2s}button:hover{background:rgba(255,255,255,.32)}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}
.chip{padding:4px 10px;font-size:12px;border-radius:99px}.chip.on{background:rgba(255,255,255,.4)}
#list{overflow:auto;flex:1;margin-top:4px}
.row{display:flex;justify-content:space-between;align-items:center;padding:10px 12px;border-radius:14px;cursor:pointer;border:1px solid transparent}
.row:hover{background:rgba(255,255,255,.14)}.row.sel{background:rgba(255,255,255,.26);border-color:var(--edge)}
.sym{font-weight:700}.nm{font-size:12px;color:var(--mut)}.px{font-size:11px;color:var(--mut);font-style:italic}
.panel{padding:22px}
.top{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px}
.top h2{margin:0;font-size:28px}.top .nm{font-size:14px}
.ctl{display:flex;gap:8px;flex-wrap:wrap}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:18px 0}
.stat{padding:14px;border-radius:16px;background:rgba(255,255,255,.14);border:1px solid var(--edge)}
.stat small{color:var(--mut);display:block;margin-bottom:4px}.stat b{font-size:22px}
.up{color:var(--up)}.dn{color:var(--dn)}
canvas{width:100%;height:340px;border-radius:16px;background:rgba(255,255,255,.08);border:1px solid var(--edge)}
.legend{font-size:12px;color:var(--mut);margin-top:8px}
.note{margin-top:14px;font-size:12px;color:var(--mut)}
</style></head><body>
<header class="glass"><h1>&#9670; AlgoTrader</h1><span class="pill">Prices: coming soon (premium feed)</span></header>
<main>
 <aside class="glass side">
  <input id="q" placeholder="Search stocks, e.g. TSLA, Infosys…">
  <div class="chips" id="chips"></div>
  <div id="list"></div>
  <div class="legend" id="count"></div>
 </aside>
 <section class="glass panel">
  <div class="top">
   <div><h2 id="hs">—</h2><div class="nm" id="hn"></div><div class="px" id="hp">Live price: unlock with premium plan</div></div>
   <div class="ctl"><select id="strat"><option value="sma_crossover">SMA crossover</option><option value="rsi">RSI mean reversion</option></select><button id="go">Run backtest</button></div>
  </div>
  <div class="stats" id="stats"></div>
  <canvas id="c" width="1000" height="340"></canvas>
  <div class="legend">White: stock performance (indexed to 100) &middot; Cyan: strategy equity &middot; Green/Red dots: buy/sell</div>
  <div class="note">Simulated data for demonstration. Not financial advice.</div>
 </section>
</main>
<script>
const $=id=>document.getElementById(id);
let ALL=[],sel='AAPL',sector='All',term='';
function renderList(){
 const t=term.toLowerCase();
 const f=ALL.filter(s=>(sector==='All'||s.sector===sector||s.exchange===sector)&&(s.symbol.toLowerCase().includes(t)||s.name.toLowerCase().includes(t)));
 $('count').textContent=f.length+' of '+ALL.length+' stocks';
 $('list').innerHTML=f.map(s=>`<div class="row ${s.symbol===sel?'sel':''}" data-s="${s.symbol}"><div><div class="sym">${s.symbol}</div><div class="nm">${s.name} · ${s.exchange}</div></div><div class="px">— soon</div></div>`).join('');
}
$('list').onclick=e=>{const r=e.target.closest('.row');if(r){sel=r.dataset.s;renderList();run()}};
$('q').oninput=e=>{term=e.target.value;renderList()};
$('go').onclick=run;$('strat').onchange=run;
function chips(){
 const secs=['All','US','NSE',...new Set(ALL.map(s=>s.sector))];
 $('chips').innerHTML=secs.map(s=>`<button class="chip ${s===sector?'on':''}" data-c="${s}">${s}</button>`).join('');
}
$('chips').onclick=e=>{const b=e.target.closest('.chip');if(b){sector=b.dataset.c;chips();renderList()}};
function draw(r){
 const c=$('c'),g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);
 const all=r.index.concat(r.equity),lo=Math.min(...all),hi=Math.max(...all),n=r.index.length;
 const X=i=>i/(n-1)*c.width,Y=v=>c.height-12-(v-lo)/(hi-lo)*(c.height-24);
 g.strokeStyle='rgba(255,255,255,.15)';for(let k=0;k<5;k++){g.beginPath();g.moveTo(0,k*c.height/4);g.lineTo(c.width,k*c.height/4);g.stroke()}
 const line=(a,col,w)=>{g.beginPath();g.strokeStyle=col;g.lineWidth=w;a.forEach((v,i)=>i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)));g.stroke()};
 line(r.index,'rgba(255,255,255,.85)',2);line(r.equity,'#5ef0ff',2.5);
 r.trades.forEach(t=>{g.fillStyle=t.side==='BUY'?'#6ef3b0':'#ff8aa0';g.beginPath();g.arc(X(t.bar),Y(r.index[t.bar]),5,0,7);g.fill()});
}
async function run(){
 const s=ALL.find(x=>x.symbol===sel)||{symbol:sel,name:''};
 $('hs').textContent=s.symbol;$('hn').textContent=s.name+' · '+s.sector+' · '+s.exchange;
 const r=await (await fetch('/api/backtest?symbol='+encodeURIComponent(sel)+'&strategy='+$('strat').value)).json();
 const cls=v=>v>=0?'up':'dn';
 $('stats').innerHTML=[['Return',r.return_pct+'%',cls(r.return_pct)],['Max drawdown','-'+r.max_drawdown_pct+'%','dn'],['Sharpe',r.sharpe,cls(r.sharpe)],['Trades',r.num_trades,'']]
  .map(x=>`<div class="stat"><small>${x[0]}</small><b class="${x[2]}">${x[1]}</b></div>`).join('');
 draw(r);
}
fetch('/api/stocks').then(r=>r.json()).then(d=>{ALL=d;chips();renderList();run()});
</script></body></html>"""

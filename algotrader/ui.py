PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AlgoTrader</title>
<style>
:root{--bg:#e6eaf2;--hi:#fff;--lo:#c3c9d6;--txt:#1b2236;--mut:#4a5470;--acc:#3b5bdb;--up:#0a8f5b;--dn:#d6284a}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:var(--bg);color:var(--txt);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;font-size:15px;line-height:1.45;-webkit-font-smoothing:antialiased}
.raised{background:var(--bg);border-radius:22px;box-shadow:9px 9px 18px var(--lo),-9px -9px 18px var(--hi)}
.inset{background:var(--bg);border-radius:16px;box-shadow:inset 5px 5px 10px var(--lo),inset -5px -5px 10px var(--hi)}
header{display:flex;justify-content:space-between;align-items:center;padding:16px 24px;margin:22px auto;max-width:1300px}
header h1{font-size:22px;margin:0;font-weight:800}
.pill{font-size:13px;font-weight:600;color:var(--mut);padding:7px 14px;border-radius:99px}
main{display:grid;grid-template-columns:360px 1fr;gap:26px;max-width:1300px;margin:0 auto 34px;padding:0 22px}
@media(max-width:860px){main{grid-template-columns:1fr}}
.side{padding:18px;display:flex;flex-direction:column;height:calc(100vh - 130px);min-height:440px}
input,select,button{font:inherit;color:var(--txt);background:var(--bg);border:0;border-radius:14px;padding:10px 14px;outline:none}
input{width:100%;box-shadow:inset 4px 4px 8px var(--lo),inset -4px -4px 8px var(--hi)}
input::placeholder{color:var(--mut)}
select,button{box-shadow:5px 5px 10px var(--lo),-5px -5px 10px var(--hi);cursor:pointer;font-weight:600}
button:active,button.on{box-shadow:inset 4px 4px 8px var(--lo),inset -4px -4px 8px var(--hi);color:var(--acc)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.chip{padding:5px 12px;font-size:12.5px;border-radius:99px}
#list{overflow:auto;flex:1;padding:6px}
.row{display:flex;justify-content:space-between;align-items:center;padding:11px 14px;margin-bottom:10px;border-radius:14px;cursor:pointer;box-shadow:4px 4px 8px var(--lo),-4px -4px 8px var(--hi)}
.row.sel{box-shadow:inset 4px 4px 8px var(--lo),inset -4px -4px 8px var(--hi)}
.sym{font-weight:800}.nm{font-size:12.5px;color:var(--mut)}.px{font-size:12px;color:var(--mut);font-style:italic}
.bot{font-size:11px;font-weight:700;color:var(--up);margin-left:6px}
.panel{padding:26px}
.top{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:14px}
.top h2{margin:0;font-size:30px;font-weight:800}
.ctl{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.sw{display:flex;align-items:center;gap:10px;font-weight:700}
.tg{width:58px;height:30px;border-radius:99px;position:relative;padding:0;cursor:pointer}
.tg i{position:absolute;top:4px;left:5px;width:22px;height:22px;border-radius:50%;background:var(--bg);box-shadow:3px 3px 6px var(--lo),-2px -2px 5px var(--hi);transition:.25s}
.tg.on i{left:31px;background:var(--up)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:18px;margin:24px 0}
.stat{padding:16px;border-radius:18px}.stat small{color:var(--mut);display:block;font-weight:600}.stat b{font-size:24px}
.up{color:var(--up)}.dn{color:var(--dn)}
canvas{width:100%;height:320px;border-radius:18px}
.legend{font-size:13px;color:var(--mut);margin-top:10px}
.bt{margin-top:22px;padding:18px;border-radius:18px}.bt h3{margin:0 0 8px;font-size:16px}
#log{max-height:170px;overflow:auto;font-size:13.5px}
#log div{padding:4px 0;border-bottom:1px solid var(--lo)}
</style></head><body>
<header class="raised"><h1>&#9670; AlgoTrader</h1><span class="pill inset">Prices: coming soon (premium feed)</span></header>
<main>
 <aside class="raised side">
  <input id="q" placeholder="Search stocks, e.g. TSLA, Infosys">
  <div class="chips" id="chips"></div>
  <div id="list"></div>
  <div class="legend" id="count"></div>
 </aside>
 <section class="raised panel">
  <div class="top">
   <div><h2 id="hs">-</h2><div class="nm" id="hn"></div><div class="px">Live price: unlock with premium plan</div></div>
   <div class="ctl">
    <select id="strat"><option value="sma_crossover">SMA crossover</option><option value="rsi">RSI mean reversion</option></select>
    <button id="go">Run backtest</button>
    <div class="sw"><span>Algo trading</span><button class="tg inset" id="tg" aria-label="Enable algo trading"><i></i></button></div>
   </div>
  </div>
  <div class="stats" id="stats"></div>
  <canvas id="c" class="inset" width="1000" height="320"></canvas>
  <div class="legend">Dark: stock performance (indexed to 100) &middot; Blue: strategy equity &middot; Green/Red dots: buy/sell</div>
  <div class="bt inset"><h3>Algo trading bot <span id="bs" class="px">off</span></h3><div id="log"></div></div>
  <div class="legend">Paper trading on simulated data. Not financial advice.</div>
 </section>
</main>
<script>
const $=id=>document.getElementById(id);
let ALL=[],sel='AAPL',sector='All',term='';
let bots=JSON.parse(localStorage.getItem('bots')||'{}');
const save=()=>localStorage.setItem('bots',JSON.stringify(bots));
function renderList(){
 const t=term.toLowerCase();
 const f=ALL.filter(s=>(sector==='All'||s.sector===sector||s.exchange===sector)&&(s.symbol.toLowerCase().includes(t)||s.name.toLowerCase().includes(t)));
 $('count').textContent=f.length+' of '+ALL.length+' stocks';
 $('list').innerHTML=f.map(s=>`<div class="row ${s.symbol===sel?'sel':''}" data-s="${s.symbol}"><div><div class="sym">${s.symbol}${bots[s.symbol]?'<span class="bot">BOT ON</span>':''}</div><div class="nm">${s.name} · ${s.exchange}</div></div><div class="px">soon</div></div>`).join('');
}
$('list').onclick=e=>{const r=e.target.closest('.row');if(r){sel=r.dataset.s;renderList();run();showBot()}};
$('q').oninput=e=>{term=e.target.value;renderList()};
$('go').onclick=run;$('strat').onchange=()=>{run();if(bots[sel]){bots[sel]={strategy:$('strat').value,bar:60,pos:0,entry:0,pnl:0,log:[]};save();showBot()}};
function chips(){
 const secs=['All','US','NSE',...new Set(ALL.map(s=>s.sector))];
 $('chips').innerHTML=secs.map(s=>`<button class="chip ${s===sector?'on':''}" data-c="${s}">${s}</button>`).join('');
}
$('chips').onclick=e=>{const b=e.target.closest('.chip');if(b){sector=b.dataset.c;chips();renderList()}};
function draw(r){
 const c=$('c'),g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);
 const all=r.index.concat(r.equity),lo=Math.min(...all),hi=Math.max(...all),n=r.index.length;
 const X=i=>i/(n-1)*c.width,Y=v=>c.height-14-(v-lo)/(hi-lo)*(c.height-28);
 g.strokeStyle='rgba(60,70,100,.15)';for(let k=0;k<5;k++){g.beginPath();g.moveTo(0,k*c.height/4);g.lineTo(c.width,k*c.height/4);g.stroke()}
 const line=(a,col,w)=>{g.beginPath();g.strokeStyle=col;g.lineWidth=w;a.forEach((v,i)=>i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)));g.stroke()};
 line(r.index,'#1b2236',2);line(r.equity,'#3b5bdb',2.5);
 r.trades.forEach(t=>{g.fillStyle=t.side==='BUY'?'#0a8f5b':'#d6284a';g.beginPath();g.arc(X(t.bar),Y(r.index[t.bar]),5,0,7);g.fill()});
}
async function run(){
 const s=ALL.find(x=>x.symbol===sel)||{symbol:sel,name:'',sector:'',exchange:''};
 $('hs').textContent=s.symbol;$('hn').textContent=s.name+' · '+s.sector+' · '+s.exchange;
 const r=await (await fetch('/api/backtest?symbol='+encodeURIComponent(sel)+'&strategy='+$('strat').value)).json();
 const cls=v=>v>=0?'up':'dn';
 $('stats').innerHTML=[['Return',r.return_pct+'%',cls(r.return_pct)],['Max drawdown','-'+r.max_drawdown_pct+'%','dn'],['Sharpe',r.sharpe,cls(r.sharpe)],['Trades',r.num_trades,'']]
  .map(x=>`<div class="stat raised"><small>${x[0]}</small><b class="${x[2]}">${x[1]}</b></div>`).join('');
 draw(r);
}
function showBot(){
 const b=bots[sel];
 $('tg').classList.toggle('on',!!b);
 if(b)$('strat').value=b.strategy;
 $('bs').textContent=b?(b.pos?'in position':'flat')+' · paper P&L '+b.pnl.toFixed(2)+'%':'off';
 $('log').innerHTML=b?(b.log.slice().reverse().map(l=>`<div class="${l.side==='BUY'?'up':'dn'}"><b>${l.side}</b> bar ${l.bar} · index ${l.index}${l.pl!=null?' · trade '+l.pl.toFixed(2)+'%':''}</div>`).join('')||'<div>Waiting for a signal…</div>'):'<div>Switch on Algo trading to start the paper bot for '+sel+'.</div>';
}
$('tg').onclick=()=>{
 if(bots[sel])delete bots[sel];else bots[sel]={strategy:$('strat').value,bar:60,pos:0,entry:0,pnl:0,log:[]};
 save();renderList();showBot();
};
async function tick(){
 for(const [sym,b] of Object.entries(bots)){
  try{
   const r=await (await fetch('/api/signal?symbol='+sym+'&strategy='+b.strategy+'&bar='+b.bar)).json();
   if(r.signal===1&&!b.pos){b.pos=1;b.entry=r.index;b.log.push({side:'BUY',bar:r.bar,index:r.index})}
   else if(r.signal===0&&b.pos){const pl=(r.index/b.entry-1)*100;b.pos=0;b.pnl+=pl;b.log.push({side:'SELL',bar:r.bar,index:r.index,pl})}
   b.bar=r.bar>=500?60:r.bar+1;
  }catch(e){}
 }
 save();showBot();
}
setInterval(tick,2500);
fetch('/api/stocks').then(r=>r.json()).then(d=>{ALL=d;chips();renderList();run();showBot()});
</script></body></html>"""

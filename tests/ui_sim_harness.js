const fs=require('fs'),vm=require('vm');
const els={};
function el(id){if(id==='c')return {width:1000,height:290,getContext:()=>new Proxy({},{get:()=>()=>{}})};
 if(!els[id])els[id]={id,classList:{add(){},remove(){},toggle(){},contains(){return false}},style:{},value:'',innerHTML:'',textContent:'',dataset:{}};return els[id]}
global.document={getElementById:el};
global.window=global;
global.localStorage={s:{},getItem(k){return this.s[k]||null},setItem(k,v){this.s[k]=v},removeItem(k){delete this.s[k]}};
global.alert=m=>console.log('  [alert]',m);global.confirm=()=>true;global.setInterval=()=>0;
global.HTMLCanvasElement=1;
let P=100,SIG=1; // USD price and signal controlled by the test
const stocks=[{symbol:'AAPL',name:'Apple',sector:'Technology',exchange:'US'}];
global.fetch=async url=>{
  if(url.startsWith('/api/stocks'))return {json:async()=>stocks};
  if(url.startsWith('/api/fx'))return {json:async()=>({USDINR:100})};
  if(url.startsWith('/api/quotes'))return {json:async()=>[{symbol:'AAPL',price:P,change_pct:1,currency:'USD',simulated:false}]};
  if(url.startsWith('/api/signal'))return {json:async()=>({signal:SIG,price:P,simulated:false})};
  if(url.startsWith('/api/best'))return {json:async()=>({best:'macd'})};
  if(url.startsWith('/api/backtest'))return {json:async()=>({return_pct:5,max_drawdown_pct:2,sharpe:1,num_trades:3,last:P,index:[100,101],equity:[100,101],trades:[]})};
  throw new Error('unexpected '+url);
};
const page=process.argv[2];vm.runInThisContext(fs.readFileSync(page,'utf8')+'\n;globalThis.__S=()=>S;globalThis.__Q=()=>Q;globalThis.__FX=()=>FX;globalThis.__tick=tick;');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  await sleep(60);
  const S=globalThis.__S();const FX=globalThis.__FX();
  console.log('capital', S.cash.toLocaleString('en-IN'), 'fx', FX);
  S.bots.AAPL={sym:'AAPL',strategy:'sma_crossover',ts:2.5,tp:6,pp:3,sz:10,pos:0,qty:0,entry:0,buyPrice:0,peak:0,cost:0,realized:0,partialDone:false,armed:false,log:[]};
  SIG=0; await globalThis.__tick();            // arm
  SIG=1; await globalThis.__tick();            // buy
  let b=S.bots.AAPL;
  console.log('after buy: pos',b.pos,'shares',b.qty.toFixed(0),'entry',b.entry.toFixed(2),'cashDelta',(1e13-S.cash).toExponential(3),'fee',S.fee.toFixed(0));
  P=104; await globalThis.__tick();            // +4% -> partial book
  console.log('partial: shares',b.qty.toFixed(0),'pending',S.pending.toFixed(0),'sells',S.sells);
  P=107; await globalThis.__tick();            // +7% -> take profit rest
  console.log('after TP: pos',b.pos,'qty',b.qty,'net',S.net.toFixed(0),'fee',S.fee.toFixed(0),'sells',S.sells,'winrate',(S.wins/S.sells*100).toFixed(0)+'%');
  const pending=S.pending; el('xfer').onclick(); const movedOk=Math.abs(S.bank-pending)<1;
  console.log('transfer: pending',S.pending,'bank',S.bank.toFixed(0),'movedOk',movedOk);
  // trailing stop test
  S.bots.MSFT={sym:'AAPL',strategy:'sma_crossover',ts:2.5,tp:50,pp:99,sz:5,pos:0,qty:0,entry:0,buyPrice:0,peak:0,cost:0,realized:0,partialDone:false,armed:true,log:[]};
  SIG=1; await globalThis.__tick();
  const b2=S.bots.MSFT; P=P*1.05; await globalThis.__tick(); const pk=b2.peak;
  P=pk*0.97/FX; await globalThis.__tick();
  console.log('trailing stop fired:', !b2.pos, 'reason', b2.log[0]&&b2.log[0].why, 'peak', pk.toFixed(0));
  console.log('commission check: fee>0 and net<gross:', S.fee>0, S.net<S.gross);
  el('mq').value=10; const feeBefore=S.fee; el('buy').onclick();
  const held=Object.keys(S.hold).length>0;
  el('sell').onclick();
  const manualOk=held && Object.keys(S.hold).length===0 && S.fee>feeBefore;
  console.log('manual buy/sell ok:', manualOk, 'feeDelta', (S.fee-feeBefore).toFixed(2));
  const ok=!b.pos && S.bank>0 && S.fee>0 && !b2.pos && S.net>0 && movedOk && manualOk;
  console.log(ok?'RESULT PASS':'RESULT FAIL');process.exit(ok?0:1);
})();

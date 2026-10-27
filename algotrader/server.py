"""Dashboard + JSON API. Run: python -m algotrader.server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from .backtest import backtest
from .data import generate_prices
from .strategies import STRATEGIES

PAGE = """<!doctype html><meta charset=utf-8><title>AlgoTrader</title>
<style>body{font-family:sans-serif;max-width:900px;margin:2em auto}canvas{width:100%;border:1px solid #ccc}</style>
<h1>AlgoTrader (simulated data)</h1>
Symbol <input id=sym value=AAPL size=6>
<select id=strat><option value=sma_crossover>SMA crossover</option><option value=rsi>RSI</option></select>
<button onclick=run()>Backtest</button>
<pre id=out></pre><canvas id=c width=900 height=350></canvas>
<script>
async function run(){
 const r=await (await fetch('/api/backtest?symbol='+sym.value+'&strategy='+strat.value)).json();
 const {equity,trades,...m}=r; out.textContent=JSON.stringify(m,null,2);
 const g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);
 const lo=Math.min(...r.prices),hi=Math.max(...r.prices);
 const line=(a,col)=>{g.beginPath();g.strokeStyle=col;a.forEach((v,i)=>{const x=i/(a.length-1)*c.width,y=c.height-(v-lo)/(hi-lo)*c.height;i?g.lineTo(x,y):g.moveTo(x,y)});g.stroke()};
 line(r.prices,'#888');
 trades.forEach(t=>{const x=t.bar/(r.prices.length-1)*c.width,y=c.height-(t.price-lo)/(hi-lo)*c.height;g.fillStyle=t.side=='BUY'?'green':'red';g.fillRect(x-3,y-3,6,6)});
}
run();
</script>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            return self._send(200, PAGE, "text/html")
        if u.path == "/api/backtest":
            q = parse_qs(u.query)
            symbol = q.get("symbol", ["AAPL"])[0].upper()[:10]
            name = q.get("strategy", ["sma_crossover"])[0]
            if name not in STRATEGIES:
                return self._send(400, json.dumps({"error": "unknown strategy"}))
            prices = generate_prices(symbol)
            res = backtest(prices, STRATEGIES[name](prices))
            res["prices"] = prices
            return self._send(200, json.dumps(res))
        self._send(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    print("http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

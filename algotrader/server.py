"""Dashboard + JSON API. Run: python -m algotrader.server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from .backtest import backtest
from . import market
from .strategies import STRATEGIES

from .ui import PAGE
from .stocks import STOCKS


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
        if u.path == "/api/stocks":
            return self._send(200, json.dumps(STOCKS))
        q = parse_qs(u.query)
        if u.path == "/api/fx":
            return self._send(200, json.dumps({"USDINR": market.usdinr()}))
        if u.path == "/api/best":
            symbol = q.get("symbol", ["AAPL"])[0].upper()
            if symbol not in market.BY_SYMBOL:
                return self._send(400, json.dumps({"error": "unknown symbol"}))
            key = ("best", symbol)
            hit = market._cache.get(key)
            if not (hit and __import__("time").time() - hit[0] < 300):
                prices = market.history(symbol)["closes"]
                best = max(STRATEGIES, key=lambda n: backtest(prices, STRATEGIES[n](prices))["return_pct"])
                hit = market._cache[key] = (__import__("time").time(), best)
            return self._send(200, json.dumps({"best": hit[1]}))
        if u.path == "/api/quotes":
            syms = [x.strip().upper() for x in q.get("symbols", [""])[0].split(",") if x.strip()]
            return self._send(200, json.dumps(market.quotes(syms)))
        if u.path in ("/api/signal", "/api/backtest"):
            symbol = q.get("symbol", ["AAPL"])[0].upper()
            name = q.get("strategy", ["sma_crossover"])[0]
            if symbol not in market.BY_SYMBOL:
                return self._send(400, json.dumps({"error": "unknown symbol"}))
            if name not in STRATEGIES:
                return self._send(400, json.dumps({"error": "unknown strategy"}))
            h = market.history(symbol)
            prices = h["closes"]
            sig = STRATEGIES[name](prices)
            if u.path == "/api/signal":
                return self._send(200, json.dumps({"signal": sig[-1], "price": h["price"],
                                                   "simulated": h["simulated"]}))
            res = backtest(prices, sig)
            base = prices[0]
            res["index"] = [round(p / base * 100, 2) for p in prices]
            res["trades"] = [{"bar": t["bar"], "side": t["side"], "price": t["price"]} for t in res["trades"]]
            res["equity"] = [round(e / res["equity"][0] * 100, 2) for e in res["equity"]]
            res.update(currency=h["currency"], simulated=h["simulated"], last=h["price"])
            return self._send(200, json.dumps(res))
        self._send(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    print("http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

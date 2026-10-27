"""Dashboard + JSON API. Run: python -m algotrader.server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from .backtest import backtest
from .data import generate_prices
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
        if u.path == "/api/signal":
            q = parse_qs(u.query)
            symbol = q.get("symbol", ["AAPL"])[0].upper()[:10]
            name = q.get("strategy", ["sma_crossover"])[0]
            try:
                bar = max(40, min(500, int(q.get("bar", [60])[0])))
            except ValueError:
                return self._send(400, json.dumps({"error": "bad bar"}))
            if name not in STRATEGIES:
                return self._send(400, json.dumps({"error": "unknown strategy"}))
            prices = generate_prices(symbol)[:bar]
            sig = STRATEGIES[name](prices)
            base = prices[0]
            return self._send(200, json.dumps({"bar": bar, "signal": sig[-1],
                                               "index": round(prices[-1] / base * 100, 2)}))
        if u.path == "/api/backtest":
            q = parse_qs(u.query)
            symbol = q.get("symbol", ["AAPL"])[0].upper()[:10]
            name = q.get("strategy", ["sma_crossover"])[0]
            if name not in STRATEGIES:
                return self._send(400, json.dumps({"error": "unknown strategy"}))
            prices = generate_prices(symbol)
            res = backtest(prices, STRATEGIES[name](prices))
            base = prices[0]
            res["index"] = [round(p / base * 100, 2) for p in prices]
            res["trades"] = [{"bar": t["bar"], "side": t["side"]} for t in res["trades"]]
            res["equity"] = [round(e / res["equity"][0] * 100, 2) for e in res["equity"]]
            return self._send(200, json.dumps(res))
        self._send(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    print("http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

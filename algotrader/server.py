"""Dashboard + JSON API. Run: python -m algotrader.server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from . import market, scanner
from .backtest import backtest
from .strategies import STRATEGIES
from .ui import PAGE


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            return self.route(u.path, q)
        except KeyError as e:
            return self._send(404, json.dumps({"error": "unknown symbol %s" % e}))
        except Exception as e:  # never 500 the dashboard
            return self._send(400, json.dumps({"error": str(e)}))

    def route(self, path, q):
        arg = lambda k, d="": q.get(k, [d])[0]
        if path in ("/", "/index.html"):
            return self._send(200, PAGE, "text/html")
        if path == "/api/instruments":
            rows = market.instruments(arg("market") or None)
            return self._send(200, json.dumps(rows))
        if path == "/api/quotes":
            ids = [s.strip() for s in arg("symbols").split(",") if s.strip()]
            return self._send(200, json.dumps(market.quotes(ids)))
        if path == "/api/scan":
            return self._send(200, json.dumps(scanner.scan(arg("market", "IN"), int(arg("limit", "8")))))
        if path == "/api/fx":
            return self._send(200, json.dumps({"USDINR": market.usdinr()}))
        if path == "/api/optionchain":
            name = arg("underlying", "NIFTY")
            rows = [o for o in market.instruments("IN")
                    if o["type"] == "OPT" and o.get("underlying") == name]
            return self._send(200, json.dumps(rows))
        if path == "/api/best":
            sid = arg("symbol").upper()
            prices = market.history(sid)["closes"][-180:]
            best = max(STRATEGIES, key=lambda n: backtest(prices, STRATEGIES[n](prices))["return_pct"])
            return self._send(200, json.dumps({"best": best}))
        if path in ("/api/signal", "/api/backtest"):
            sid = arg("symbol").upper()
            name = arg("strategy", "sma_crossover")
            if name not in STRATEGIES:
                return self._send(400, json.dumps({"error": "unknown strategy"}))
            h = market.history(sid)
            prices = h["closes"]
            sig = STRATEGIES[name](prices)
            if path == "/api/signal":
                return self._send(200, json.dumps({"signal": sig[-1], "price": h["price"],
                                                   "simulated": h["simulated"], "type": h["type"]}))
            res = backtest(prices, sig)
            base = prices[0]
            res["index"] = [round(p / base * 100, 2) for p in prices]
            res["equity"] = [round(e / res["equity"][0] * 100, 2) for e in res["equity"]]
            res.update(currency=h["currency"], simulated=h["simulated"], last=h["price"], type=h["type"])
            return self._send(200, json.dumps(res))
        return self._send(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    print("http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

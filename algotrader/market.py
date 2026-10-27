"""Real market data from Yahoo Finance's public chart endpoint (unofficial, free, delayed).
Falls back to simulated prices (flagged simulated=True) if the feed is unreachable."""
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from .data import generate_prices
from .stocks import STOCKS

BY_SYMBOL = {s["symbol"]: s for s in STOCKS}
CURRENCY = {"US": "USD", "NSE": "INR"}
_cache = {}


def yahoo_symbol(symbol):
    s = BY_SYMBOL[symbol]
    if s["exchange"] == "NSE":
        return symbol + ".NS"
    return symbol.replace(".", "-")


def _fetch(symbol, rng, interval, ttl):
    if symbol not in BY_SYMBOL:
        raise KeyError(symbol)
    key = (symbol, rng, interval)
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < ttl:
        return hit[1]
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/%s?range=%s&interval=%s"
           % (yahoo_symbol(symbol), rng, interval))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            res = json.load(r)["chart"]["result"][0]
        closes = res["indicators"]["quote"][0]["close"]
        ts = res["timestamp"]
        pairs = [(t, c) for t, c in zip(ts, closes) if c is not None]
        out = {"symbol": symbol, "simulated": False,
               "currency": res["meta"].get("currency", CURRENCY[BY_SYMBOL[symbol]["exchange"]]),
               "times": [p[0] for p in pairs], "closes": [round(p[1], 2) for p in pairs],
               "price": round(res["meta"].get("regularMarketPrice") or pairs[-1][1], 2)}
    except Exception:
        closes = generate_prices(symbol, 250)
        now = int(time.time())
        out = {"symbol": symbol, "simulated": True,
               "currency": CURRENCY[BY_SYMBOL[symbol]["exchange"]],
               "times": [now - 86400 * (len(closes) - i) for i in range(len(closes))],
               "closes": closes, "price": closes[-1]}
    _cache[key] = (time.time(), out)
    return out


def history(symbol):
    return _fetch(symbol, "1y", "1d", 120)


def quote(symbol):
    h = _fetch(symbol, "5d", "1d", 8)
    prev = h["closes"][-2] if len(h["closes"]) > 1 else h["price"]
    chg = (h["price"] / prev - 1) * 100 if prev else 0
    return {"symbol": symbol, "price": h["price"], "change_pct": round(chg, 2),
            "currency": h["currency"], "simulated": h["simulated"]}


def quotes(symbols):
    symbols = [s for s in symbols if s in BY_SYMBOL][:30]
    with ThreadPoolExecutor(max_workers=10) as ex:
        return list(ex.map(quote, symbols))


def usdinr():
    """Live USD->INR, cached 5 min, fallback 83.5."""
    key = ("FX", "1d", "1d")
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < 300:
        return hit[1]
    rate = 83.5
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/INR=X?range=1d&interval=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as r:
            rate = round(json.load(r)["chart"]["result"][0]["meta"]["regularMarketPrice"], 2)
    except Exception:
        pass
    _cache[key] = (time.time(), rate)
    return rate

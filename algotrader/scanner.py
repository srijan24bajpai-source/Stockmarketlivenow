"""Ranks instruments into actionable suggestions using every strategy."""
import time
from concurrent.futures import ThreadPoolExecutor

from . import market
from .backtest import backtest
from .strategies import STRATEGIES

_cache = {}
TRADEABLE = ("STOCK", "INDEX", "CRYPTO", "FUT")


def _evaluate(row):
    try:
        h = market.history(row["symbol"])
    except Exception:
        return None
    px = market.price_of(row["symbol"])
    closes = h["closes"]
    window = closes[-120:]
    scores = {}
    for name, fn in STRATEGIES.items():
        sig = fn(window)
        r = backtest(window, sig)
        scores[name] = (r["return_pct"], r["max_drawdown_pct"], sig[-1])
    best = max(scores, key=lambda n: scores[n][0])
    ret, dd, sig_now = scores[best]
    nwins = sum(1 for k, v in scores.items() if v[0] > 0)
    mom = (closes[-1] / closes[-21] - 1) * 100 if len(closes) > 21 else 0
    score = round(ret + mom / 2 + nwins * 0.5, 2)
    return {"symbol": row["symbol"], "name": row["name"], "market": row["market"],
            "type": row.get("type", "STOCK"), "exchange": row.get("exchange"),
            "price": px, "strategy": best, "signal": sig_now, "action": "BUY" if sig_now else "WAIT",
            "ret_3m": ret, "drawdown": dd, "momentum": round(mom, 2),
            "score": score, "simulated": h["simulated"]}


def scan(market_name="IN", limit=10):
    key = (market_name, limit)
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < 90:
        return hit[1]
    rows = [i for i in market.instruments(market_name) if i["type"] in TRADEABLE]
    rows = sorted(rows, key=lambda r: -("NIFTY" in r["symbol"]) * 1)[:30]
    with ThreadPoolExecutor(max_workers=8) as ex:
        out = [r for r in ex.map(_evaluate, rows) if r]
    out.sort(key=lambda r: (-r["signal"], -r["ret_3m"]))
    _cache[key] = (time.time(), out[:limit])
    return out[:limit]

"""Buy / sell / wait calls with confidence, target, stop and plain reasons."""
import time

from . import market
from .backtest import backtest
from .strategies import STRATEGIES, rsi, sma

_cache = {}
TTL = 60


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def indicators(closes):
    price = closes[-1]
    s20 = sma(closes[-60:], 20)[-1] or price
    s50 = sma(closes[-90:], 50)[-1] or price
    r = rsi(closes[-90:], 14)[-1]
    mom20 = (price / closes[-21] - 1) * 100 if len(closes) > 21 else 0.0
    diffs = [abs(closes[i] - closes[i - 1]) for i in range(max(1, len(closes) - 14), len(closes))]
    atr = (sum(diffs) / len(diffs)) * 2.2 if diffs else price * 0.01
    return {"price": price, "sma20": round(s20, 2), "sma50": round(s50, 2),
            "rsi": round(r if r is not None else 50, 1), "mom20": round(mom20, 2),
            "atr": round(atr, 2), "above20": price > s20, "above50": price > s50}


def votes(closes):
    window = closes[-160:]
    out = {}
    for name, fn in STRATEGIES.items():
        sig = fn(window)
        r = backtest(window, sig)
        out[name] = {"signal": int(sig[-1]), "ret_6m": round(r["return_pct"], 2), "sharpe": r["sharpe"]}
    return out


def recommend(sid):
    key = ("rec", sid)
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < TTL:
        return hit[1]
    h = market.history(sid)
    closes = h["closes"]
    price = market.price_of(sid)
    ind = indicators(closes)
    v = votes(closes)
    bulls = sum(x["signal"] for x in v.values())
    breadth = bulls / len(v) * 100
    best = max(v, key=lambda n: v[n]["ret_6m"])
    score = 0.60 * breadth
    score += 15 if ind["above20"] else -15
    score += _clamp(ind["mom20"] * 1.2, -15, 15)
    if ind["rsi"] > 75:
        score -= 6
    elif ind["rsi"] < 25:
        score += 6
    score = round(_clamp(score, 0, 100), 1)
    action = "BUY" if score >= 58 else ("SELL" if score <= 42 else "WAIT")
    conf = min(95, int(round(abs(score - 50) * 2)))
    atr = ind["atr"] or price * 0.01
    if action == "SELL":
        target, stop = price - 2 * atr, price + 1.2 * atr
    else:
        target, stop = price + 2 * atr, price - 1.2 * atr
    reasons = [
        "%d of %d strategies are bullish" % (bulls, len(v)),
        "Price is %s the 20-day average (%s) and %s the 50-day (%s)" % (
            "above" if ind["above20"] else "below", ind["sma20"],
            "above" if ind["above50"] else "below", ind["sma50"]),
        "RSI %s (%s)" % (ind["rsi"], "overbought" if ind["rsi"] > 70 else ("oversold" if ind["rsi"] < 30 else "neutral")),
        "20-day momentum %+.2f%%" % ind["mom20"],
        "Best recent strategy: %s (%+.2f%% over 6 months)" % (best, v[best]["ret_6m"]),
    ]
    out = {"symbol": sid, "name": getattr(market, "name_of", lambda s: s)(sid),
           "action": action, "score": score, "confidence": conf,
           "price": price, "target": round(target, 2), "stop": round(stop, 2),
           "reward_pct": round(abs(target - price) / price * 100, 2),
           "risk_pct": round(abs(price - stop) / price * 100, 2),
           "rr": round(abs(target - price) / max(abs(price - stop), 1e-9), 2),
           "best_strategy": best, "votes": v, "indicators": ind,
           "simulated": h["simulated"], "as_of": int(time.time()), "reasons": reasons}
    _cache[key] = (time.time(), out)
    return out


def batch(symbols, limit=25):
    out = []
    for s in [x for x in symbols if x][:limit]:
        try:
            out.append(recommend(s))
        except Exception:
            continue
    return out

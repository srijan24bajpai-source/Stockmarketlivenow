"""Black-Scholes pricing so the app can trade index options with live spot."""
import math

RATE = 0.065


def _n(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs(S, K, T, sigma, call=True, r=RATE):
    if T <= 0 or sigma <= 0:
        return max(0.0, (S - K) if call else (K - S))
    d1 = (math.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if call:
        return S * _n(d1) - K * math.exp(-r * T) * _n(d2)
    return K * math.exp(-r * T) * _n(-d2) - S * _n(-d1)


def realized_vol(closes, n=30):
    if len(closes) < 3:
        return 0.25
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(max(1, len(closes) - n), len(closes))]
    m = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - m) ** 2 for r in rets) / len(rets))
    return min(0.9, max(0.10, sd * math.sqrt(252)))


def chain(name, spot, expiry_days, sigma, strikes=5, step=None):
    """ATM +/- strikes, both sides. Prices are per unit (lot size applied by caller)."""
    step = step or (max(50, round(spot * 0.01 / 50) * 50) if spot > 1000 else max(5, round(spot * 0.02 / 5) * 5))
    atm = round(spot / step) * step
    T = max(expiry_days, 0.5) / 365
    out = []
    for k in range(-strikes, strikes + 1):
        K = atm + k * step
        for side, call in (("CE", True), ("PE", False)):
            px = round(bs(spot, K, T, sigma, call), 2)
            out.append({"symbol": "%s-%d-%s" % (name, int(K), side), "strike": int(K), "side": side,
                        "price": px, "days": expiry_days,
                        "delta": round((_n((math.log(spot / K) + (RATE + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T)))) if call else -_n(-((math.log(spot / K) + (RATE + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T)))), 2),
                        "atm": K == atm})
    return out

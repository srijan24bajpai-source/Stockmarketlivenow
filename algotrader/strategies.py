"""Strategies return a signal per bar: 1 = long, 0 = flat."""


def sma(prices, window):
    out = [None] * len(prices)
    s = 0.0
    for i, p in enumerate(prices):
        s += p
        if i >= window:
            s -= prices[i - window]
        if i >= window - 1:
            out[i] = s / window
    return out


def rsi(prices, period=14):
    out = [None] * len(prices)
    if len(prices) <= period:
        return out
    gains = losses = 0.0
    for i in range(1, period + 1):
        d = prices[i] - prices[i - 1]
        gains += max(d, 0)
        losses += max(-d, 0)
    ag, al = gains / period, losses / period
    for i in range(period, len(prices)):
        if i > period:
            d = prices[i] - prices[i - 1]
            ag = (ag * (period - 1) + max(d, 0)) / period
            al = (al * (period - 1) + max(-d, 0)) / period
        out[i] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    return out


def sma_crossover(prices, fast=10, slow=30):
    f, s = sma(prices, fast), sma(prices, slow)
    return [1 if (a is not None and b is not None and a > b) else 0 for a, b in zip(f, s)]


def rsi_mean_reversion(prices, period=14, buy_below=30, sell_above=70):
    r = rsi(prices, period)
    pos, sig = 0, []
    for v in r:
        if v is not None:
            if v < buy_below:
                pos = 1
            elif v > sell_above:
                pos = 0
        sig.append(pos)
    return sig


STRATEGIES = {"sma_crossover": sma_crossover, "rsi": rsi_mean_reversion}

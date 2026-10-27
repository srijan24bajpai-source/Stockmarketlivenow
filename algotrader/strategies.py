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





def ema(prices, n):
    out, k, prev = [], 2 / (n + 1), prices[0]
    for p in prices:
        prev = p * k + prev * (1 - k)
        out.append(prev)
    return out


def macd(prices, fast=12, slow=26, signal=9):
    f, s = ema(prices, fast), ema(prices, slow)
    line = [a - b for a, b in zip(f, s)]
    sig = ema(line, signal)
    return [1 if l > g else 0 for l, g in zip(line, sig)]


def bollinger_breakout(prices, n=20, k=2):
    out, pos = [], 0
    for i in range(len(prices)):
        if i >= n:
            w = prices[i - n:i]
            m = sum(w) / n
            sd = (sum((x - m) ** 2 for x in w) / n) ** 0.5
            if prices[i] > m + k * sd:
                pos = 1
            elif prices[i] < m:
                pos = 0
        out.append(pos)
    return out


def donchian(prices, entry=20, exit_=10):
    out, pos = [], 0
    for i in range(len(prices)):
        if i >= entry and prices[i] > max(prices[i - entry:i]):
            pos = 1
        elif i >= exit_ and prices[i] < min(prices[i - exit_:i]):
            pos = 0
        out.append(pos)
    return out


def momentum(prices, n=60):
    return [1 if i >= n and prices[i] > prices[i - n] else 0 for i in range(len(prices))]


STRATEGIES = {
    "sma_crossover": sma_crossover,
    "rsi": rsi_mean_reversion,
    "macd": macd,
    "bollinger": bollinger_breakout,
    "donchian": donchian,
    "momentum": momentum,
}

"""Simulated market data (geometric random walk). Swap for a real feed in production."""
import math
import random


def generate_prices(symbol: str, n: int = 500, start: float = 100.0,
                    drift: float = 0.0004, vol: float = 0.015, seed=None):
    rng = random.Random(seed if seed is not None else symbol)
    prices, p = [], start
    for _ in range(n):
        p *= math.exp(drift + vol * rng.gauss(0, 1))
        prices.append(round(p, 2))
    return prices

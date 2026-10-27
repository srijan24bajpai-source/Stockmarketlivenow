import math


def backtest(prices, signals, cash=10000.0, fee=0.001):
    """Long-only. Signal at bar i is executed at bar i+1 price (no lookahead)."""
    equity, shares, trades = [], 0.0, []
    for i, price in enumerate(prices):
        if i > 0:
            want = signals[i - 1]
            if want and shares == 0:
                shares = cash * (1 - fee) / price
                trades.append({"bar": i, "side": "BUY", "price": price})
                cash = 0.0
            elif not want and shares > 0:
                cash = shares * price * (1 - fee)
                trades.append({"bar": i, "side": "SELL", "price": price})
                shares = 0.0
        equity.append(cash + shares * price)
    peak, mdd = equity[0], 0.0
    for e in equity:
        peak = max(peak, e)
        mdd = max(mdd, (peak - e) / peak)
    rets = [equity[i] / equity[i - 1] - 1 for i in range(1, len(equity))]
    mean = sum(rets) / len(rets) if rets else 0
    sd = math.sqrt(sum((r - mean) ** 2 for r in rets) / len(rets)) if rets else 0
    return {
        "final_equity": round(equity[-1], 2),
        "return_pct": round((equity[-1] / equity[0] - 1) * 100, 2),
        "max_drawdown_pct": round(mdd * 100, 2),
        "sharpe": round(mean / sd * math.sqrt(252), 2) if sd else 0.0,
        "num_trades": len(trades),
        "trades": trades,
        "equity": [round(e, 2) for e in equity],
    }

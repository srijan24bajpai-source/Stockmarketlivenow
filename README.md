# AlgoTrader - India-first paper trading desk

A real-market, fake-money trading app: live prices, algo bots that book profit in real time,
1% commission per fill, and a profit box that moves booked P&L into a simulated bank account
only when you approve it. It is a rehearsal before risking real capital.

```
python3 -m algotrader.server      # http://localhost:8000
python3 -m unittest discover tests
```

Standard library only. The JavaScript tests need `node`.

## Markets (197 instruments, 79% India)

| Window | Contents |
|---|---|
| India - NSE + BSE + F&O | 63 NSE equities, 15 BSE scrips, NIFTY / BANK NIFTY / SENSEX / India VIX, 6 futures, 66 index options priced with Black-Scholes from live spot |
| US stocks | 37 large caps |
| Bitcoin & crypto | BTC, ETH, SOL, XRP, DOGE (live, 24/7) |
| Best trades now | ranked list across all three, with entry / target / stop |

## Trading engine

- **Capital:** Rs 1,00,00,000 (1 crore) of simulated money per session.
- **Entry never waits:** a bot acts on the current signal the moment you start it. `Long + short`
  mode (default) goes long on a bullish signal and short on a bearish one, so it is never idle;
  `Long only` sits flat when the signal is bearish. After an exit there is a 3-tick cooldown.
- **Profit booking:** partial booking (default 3%), take profit (6%), ratcheting trailing stop
  (2.5%), and exit on signal flip. Shorts mirror the same rules.
- **Commission:** 1% of the money committed, on every buy and every sell.
- **Futures:** lot sizes with 12% margin (NIFTY 75, BANK NIFTY 15, SENSEX 10, stock futures).
- **Options:** 11 strikes x CE/PE per index, priced from live spot with realised volatility,
  expiring next Thursday. Long calls/puts only (no writing).
- **Strategies:** SMA crossover, RSI mean reversion, MACD, Bollinger breakout, Donchian
  breakout, momentum, plus `Auto: best of all` (re-picks the best 1-year performer every 5 min).
- **Best trades:** the scanner backtests all six strategies on the last 120 bars for each
  instrument, ranks by return + momentum + breadth, and returns entry, target and stop.
  Start one, or `Start algo on top 5 trades` to batch-start five bots at once.
- **Profit box:** net and gross P&L, commission, pending transfer, moved to bank, win rate,
  free capital, open positions with live unrealised P&L. `Transfer profits to bank` asks for
  confirmation; `Auto-transfer` sweeps after every trade. Open positions each have a Close button.

State lives in your browser (localStorage), so it survives reloads with no server database.
`Reset` clears it.

## Limits - read this

- No real money, no broker, no order routing. Fills use the last quoted price: no slippage,
  no queue, no partial fills, no liquidity limit.
- Shorts and futures margins are simulated; real F&O needs a broker mandate and exchange margins.
- Option prices are model prices from live spot and realised volatility, not market quotes.
- Yahoo's endpoint is free and unofficial: delayed, rate-limited, and can change. Any symbol it
  refuses falls back to simulated data and is labelled `simulated` in the UI.
- No strategy guarantees profit. Tight targets lock gains early but cap upside and whipsaw in
  ranging markets. A 1-year backtest is a sanity check, not a forecast.

Not financial advice.

# AlgoTrader - paper trading desk

A stock market app with real market data and **simulated money**. It is a pre-test harness
before risking real capital: live prices, algo bots that book profit in real time, 1% broker
commission on every fill, and a profit box that moves booked P&L into a simulated bank
account only when you approve it.

## Run

```
python3 -m algotrader.server      # http://localhost:8000
python3 -m unittest discover tests
```

No dependencies beyond the Python standard library (tests need Node.js only for the JS checks).

## Trading

- **Capital:** Rs 10 lakh crore (1,00,00,00,00,000) of simulated money per session.
- **Prices:** live/delayed quotes and 1 year of daily history from Yahoo Finance's public
  chart endpoint, for 125 US and NSE stocks. If the feed fails, that symbol falls back to
  simulated data and is labelled as such.
- **Orders:** 1% commission on both buy and sell. Buys size from your cash, sells credit
  net proceeds, and `entry` stores the post-commission cost basis.
- **Strategies:** SMA crossover, RSI mean reversion, MACD, Bollinger breakout, Donchian
  breakout, momentum, plus `Auto` which backtests all six and picks the best for that stock.
- **Profit booking:** partial booking (default 3%), take profit (default 6%), ratcheting
  trailing stop (default 2.5%), signal exit. After any exit the bot re-arms only on a fresh
  entry signal, so it cannot rebuy instantly after a stop-out.
- **Profit box:** net and gross P&L, commission paid, pending transfer, moved-to-bank,
  win rate, open positions. `Transfer profits to bank account` needs your confirmation;
  `Auto-transfer` does it after every trade.
- **Manual trading:** buy/sell any stock by quantity at the live price, same 1% fee.

State (wallet, bots, fills) is stored in your browser, so it survives reloads and needs no
server database. `Reset simulation` clears it.

## Limits - read this

- No real money, no broker, no order routing. Fills are simulated at the last quoted price,
  so there is no slippage, no partial fills, no liquidity limit and no exchange fees.
- Yahoo's endpoint is free and unofficial: it can be delayed, rate-limited or change.
- No strategy can guarantee profit. The defaults are tuned to lock gains early, which also
  caps upside and can whipsaw in choppy markets.
- Backtests on 1 year of daily bars are a sanity check, not evidence of future returns.

Not financial advice. Use it as a rehearsal before connecting a real broker with real money.

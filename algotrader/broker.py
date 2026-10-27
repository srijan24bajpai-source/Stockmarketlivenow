"""Paper broker with a risk limit; replace with a real broker API for live trading."""


class PaperBroker:
    def __init__(self, cash=100000.0, max_position_pct=0.25):
        self.cash, self.positions, self.log = cash, {}, []
        self.max_position_pct = max_position_pct

    def equity(self, prices):
        return self.cash + sum(q * prices[s] for s, q in self.positions.items())

    def order(self, symbol, side, qty, price, prices=None):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if side == "BUY":
            cost = qty * price
            if cost > self.cash:
                raise ValueError("insufficient cash")
            eq = self.equity(prices or {symbol: price})
            held = self.positions.get(symbol, 0) * price
            if held + cost > eq * self.max_position_pct:
                raise ValueError("risk limit: position too large")
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
        elif side == "SELL":
            if self.positions.get(symbol, 0) < qty:
                raise ValueError("insufficient shares")
            self.cash += qty * price
            self.positions[symbol] -= qty
            if not self.positions[symbol]:
                del self.positions[symbol]
        else:
            raise ValueError("side must be BUY or SELL")
        self.log.append({"symbol": symbol, "side": side, "qty": qty, "price": price})

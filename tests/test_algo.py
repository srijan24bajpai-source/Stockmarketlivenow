import unittest
from algotrader.backtest import backtest
from algotrader.broker import PaperBroker
from algotrader.data import generate_prices
from algotrader.strategies import STRATEGIES, sma, rsi


class T(unittest.TestCase):
    def test_sma(self):
        self.assertEqual(sma([1, 2, 3, 4], 2), [None, 1.5, 2.5, 3.5])

    def test_rsi_bounds(self):
        r = [v for v in rsi(generate_prices("X")) if v is not None]
        self.assertTrue(all(0 <= v <= 100 for v in r))

    def test_backtest_all(self):
        p = generate_prices("AAPL")
        for f in STRATEGIES.values():
            res = backtest(p, f(p))
            self.assertEqual(len(res["equity"]), len(p))

    def test_no_lookahead_flat(self):
        res = backtest([1, 2, 3], [0, 0, 0])
        self.assertEqual(res["final_equity"], 10000.0)

    def test_broker(self):
        b = PaperBroker(1000, 0.5)
        b.order("A", "BUY", 4, 100)
        with self.assertRaises(ValueError):
            b.order("A", "BUY", 4, 100)
        b.order("A", "SELL", 4, 100)
        self.assertEqual(b.cash, 1000)


if __name__ == "__main__":
    unittest.main()

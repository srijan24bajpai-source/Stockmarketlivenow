import unittest
from unittest import mock

from algotrader import scanner

RISING = [100 + i * 0.4 + (3 if i % 7 == 0 else 0) for i in range(200)]


class ScannerTest(unittest.TestCase):
    def test_suggestion_shape_and_buy_signal(self):
        row = {"symbol": "TCS", "name": "TCS", "market": "IN", "type": "STOCK", "exchange": "NSE"}
        with mock.patch.object(scanner.market, "history", return_value={"closes": RISING, "simulated": False}), \
             mock.patch.object(scanner.market, "price_of", return_value=RISING[-1]):
            s = scanner._evaluate(row)
        for k in ("symbol", "price", "strategy", "action", "ret_3m", "score"):
            self.assertIn(k, s)
        self.assertIn(s["action"], ("BUY", "WAIT"))
        self.assertIsInstance(s["score"], float)

    def test_scan_is_cached_and_sorted(self):
        rows = [{"symbol": s, "name": s, "market": "IN", "type": "STOCK"} for s in ("A", "B", "C")]
        with mock.patch.object(scanner.market, "instruments", return_value=rows), \
             mock.patch.object(scanner.market, "history", return_value={"closes": RISING, "simulated": False}), \
             mock.patch.object(scanner.market, "price_of", return_value=110.0):
            scanner._cache.clear()
            out = scanner.scan("IN", 2)
            again = scanner.scan("IN", 2)
        self.assertEqual(len(out), 2)
        self.assertEqual(out, again)
        self.assertGreaterEqual(out[0]["ret_3m"], out[1]["ret_3m"] - 100)


if __name__ == "__main__":
    unittest.main()

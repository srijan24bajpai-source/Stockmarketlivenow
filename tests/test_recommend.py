import unittest
from unittest import mock

from algotrader import recommend as rec

RISING = [100 + i * 0.45 + (2.5 if i % 6 == 0 else 0) for i in range(220)]
FALLING = [400 - i * 0.5 - (3 if i % 5 == 0 else 0) for i in range(220)]


class RecommendTest(unittest.TestCase):
    def _rec(self, closes):
        rec._cache.clear()
        with mock.patch.object(rec.market, "history", return_value={"closes": closes, "simulated": False}), \
             mock.patch.object(rec.market, "price_of", return_value=closes[-1]):
            return rec.recommend("TCS")

    def test_shape_and_ranges(self):
        r = self._rec(RISING)
        self.assertIn(r["action"], ("BUY", "SELL", "WAIT"))
        self.assertGreaterEqual(r["score"], 0)
        self.assertLessEqual(r["score"], 100)
        self.assertGreaterEqual(r["confidence"], 0)
        self.assertLessEqual(r["confidence"], 100)
        self.assertEqual(len(r["reasons"]), 5)
        self.assertEqual(len(r["votes"]), 6)

    def test_uptrend_calls_buy_and_target_above_price(self):
        r = self._rec(RISING)
        self.assertEqual(r["action"], "BUY")
        self.assertGreater(r["target"], r["price"])
        self.assertLess(r["stop"], r["price"])
        self.assertGreater(r["rr"], 0)

    def test_downtrend_calls_sell_and_target_below_price(self):
        r = self._rec(FALLING)
        self.assertEqual(r["action"], "SELL")
        self.assertLess(r["target"], r["price"])
        self.assertGreater(r["stop"], r["price"])

    def test_cache_returns_same_object(self):
        rec._cache.clear()
        with mock.patch.object(rec.market, "history", return_value={"closes": RISING, "simulated": False}), \
             mock.patch.object(rec.market, "price_of", return_value=RISING[-1]):
            a = rec.recommend("TCS")
            b = rec.recommend("TCS")
        self.assertIs(a, b)

    def test_batch_skips_bad_symbols(self):
        with mock.patch.object(rec, "recommend", side_effect=[{"symbol": "X"}, KeyError("bad")]):
            out = rec.batch(["X", "BAD"])
        self.assertEqual(out, [{"symbol": "X"}])


if __name__ == "__main__":
    unittest.main()

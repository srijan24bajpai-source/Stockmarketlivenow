import json
import unittest
from unittest import mock

from algotrader import market

FAKE = {"chart": {"result": [{"meta": {"currency": "USD", "regularMarketPrice": 110.0},
        "timestamp": [1, 2, 3], "indicators": {"quote": [{"close": [100.0, None, 110.0]}]}}]}}


class Resp:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    @staticmethod
    def read():
        return json.dumps(FAKE).encode()


class MarketTest(unittest.TestCase):
    def setUp(self):
        market._cache.clear()

    def test_yahoo_symbols_cover_nse_bse_and_us(self):
        self.assertEqual(market.by_id("TCS")["yahoo"], "TCS.NS")
        self.assertEqual(market.by_id("500325")["yahoo"], "500325.BO")
        self.assertEqual(market.by_id("AAPL")["yahoo"], "AAPL")
        self.assertEqual(market.by_id("^NSEI")["yahoo"], "^NSEI")
        self.assertEqual(market.by_id("BTC-USD")["market"], "CRYPTO")

    def test_futures_have_lot_and_margin(self):
        f = market.by_id("NIFTY-FUT")
        self.assertEqual(f["type"], "FUT")
        self.assertEqual(f["unit"], 75)
        self.assertLess(f["margin"], 1)

    def test_history_parses_and_drops_empty_closes(self):
        with mock.patch("urllib.request.urlopen", return_value=Resp()):
            h = market.history("AAPL")
        self.assertEqual(h["closes"], [100.0, 110.0])
        self.assertEqual(h["price"], 110.0)
        self.assertFalse(h["simulated"])

    def test_falls_back_to_simulation(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("down")):
            h = market.history("AAPL")
        self.assertTrue(h["simulated"])
        self.assertEqual(len(h["closes"]), 250)

    def test_quote_and_change(self):
        with mock.patch("urllib.request.urlopen", return_value=Resp()):
            q = market.quote("AAPL")
        self.assertEqual(q["price"], 110.0)
        self.assertEqual(q["change_pct"], 10.0)

    def test_unknown_symbol_raises(self):
        with self.assertRaises(KeyError):
            market.by_id("NOT-A-SYMBOL")

    def test_fx_falls_back(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("down")):
            self.assertEqual(market.usdinr(), 83.5)


if __name__ == "__main__":
    unittest.main()

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


class T(unittest.TestCase):
    def setUp(self):
        market._cache.clear()

    def test_symbol_mapping(self):
        self.assertEqual(market.yahoo_symbol("TCS"), "TCS.NS")
        self.assertEqual(market.yahoo_symbol("BRK.B"), "BRK-B")

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

    def test_unknown_and_bad_input(self):
        with self.assertRaises(KeyError):
            market.history("NOPE")
        self.assertEqual(market.quotes([]), [])

    def test_quote_change(self):
        with mock.patch("urllib.request.urlopen", return_value=Resp()):
            q = market.quote("AAPL")
        self.assertEqual(q["price"], 110.0)
        self.assertEqual(q["change_pct"], 10.0)


if __name__ == "__main__":
    unittest.main()

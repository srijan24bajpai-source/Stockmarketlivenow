import unittest
from unittest import mock

from algotrader import market
from algotrader.assets import INSTRUMENTS, LOTS

NIFTY50 = [i for i in INSTRUMENTS if i.get("nifty50")]
FAKE = {"price": 1200.0, "closes": [1100 + i for i in range(60)], "simulated": False, "currency": "INR"}


class OptionChainTest(unittest.TestCase):
    def setUp(self):
        market._cache.clear()

    def test_nifty50_has_exactly_fifty_and_all_have_lots(self):
        self.assertEqual(len(NIFTY50), 50)
        missing = [i["symbol"] for i in NIFTY50 if i["symbol"] not in LOTS]
        self.assertEqual(missing, [])

    def test_chain_ids_and_lot(self):
        with mock.patch.object(market, "_chart", return_value=FAKE):
            c = market.option_chain("RELIANCE", strikes=3, target=70)
        self.assertEqual(c["lot"], 500)
        self.assertEqual(len(c["strikes"]), 7)
        self.assertTrue(all(r["ce"]["id"].endswith("-CE") for r in c["strikes"]))
        self.assertEqual(c["near_target"]["id"].split("-")[0], "RELIANCE")
        self.assertLess(abs(c["near_target"]["price"] - 70), 70)

    def test_index_chain_uses_nifty_prefix_and_lot(self):
        with mock.patch.object(market, "_chart", return_value=FAKE):
            c = market.option_chain("^NSEI", strikes=2)
        self.assertEqual(c["id_prefix"], "NIFTY")
        self.assertEqual(c["lot"], 75)
        self.assertTrue(c["strikes"][0]["ce"]["id"].startswith("NIFTY-"))

    def test_option_id_resolves_to_lot_sized_instrument(self):
        with mock.patch.object(market, "_chart", return_value=FAKE):
            inst = market.by_id("RELIANCE-1400-CE")
            px = market.price_of("RELIANCE-1400-CE")
        self.assertEqual(inst["unit"], 500)
        self.assertEqual(inst["strike"], 1400)
        self.assertGreaterEqual(px, 0)

    def test_bad_option_id_raises(self):
        with mock.patch.object(market, "_chart", return_value=FAKE):
            with self.assertRaises(KeyError):
                market.by_id("NOPE-100-CE")


if __name__ == "__main__":
    unittest.main()

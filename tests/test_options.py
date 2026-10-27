import unittest

from algotrader import options


class OptionsTest(unittest.TestCase):
    def test_call_falls_with_strike_put_rises(self):
        c1 = options.bs(100, 95, 0.1, 0.2, True)
        c2 = options.bs(100, 105, 0.1, 0.2, True)
        p1 = options.bs(100, 95, 0.1, 0.2, False)
        p2 = options.bs(100, 105, 0.1, 0.2, False)
        self.assertGreater(c1, c2)
        self.assertLess(p1, p2)

    def test_put_call_parity(self):
        S, K, T, sig, r = 24000, 24000, 7 / 365, 0.2, options.RATE
        c = options.bs(S, K, T, sig, True)
        p = options.bs(S, K, T, sig, False)
        self.assertAlmostEqual(c - p, S - K * 2.718281828459045 ** (-r * T), places=6)

    def test_realized_vol_is_clamped(self):
        flat = options.realized_vol([100] * 40)
        wild = options.realized_vol([100, 300, 100, 300] * 10)
        self.assertGreaterEqual(flat, 0.10)
        self.assertLessEqual(wild, 0.90)

    def test_chain_has_atm_strikes_both_sides(self):
        rows = options.chain("NIFTY", 24000, 3, 0.18, 3)
        self.assertEqual(len(rows), 14)
        self.assertTrue(any(r["atm"] and r["side"] == "CE" for r in rows))
        self.assertTrue(all(r["price"] >= 0 for r in rows))


if __name__ == "__main__":
    unittest.main()

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from algotrader.ui import PAGE

ROOT = Path(__file__).resolve().parent
NODE = shutil.which("node")


@unittest.skipUnless(NODE, "node not installed")
class UiScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.js = Path(cls.dir.name) / "page.js"
        cls.js.write_text(re.search(r"<script>(.*)</script>", PAGE, re.S).group(1))

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    def test_js_parses(self):
        subprocess.run([NODE, "--check", str(self.js)], check=True)

    def test_simulation_books_profit_and_charges_commission(self):
        r = subprocess.run([NODE, str(ROOT / "ui_sim_harness.js"), str(self.js)],
                           capture_output=True, text=True)
        self.assertIn("RESULT PASS", r.stdout, r.stdout + r.stderr)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()

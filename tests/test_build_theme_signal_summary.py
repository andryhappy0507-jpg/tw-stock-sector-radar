from __future__ import annotations

import unittest

import pandas as pd

from scripts.build_theme_signal_summary import aggregate


class ThemeSignalEligibilityTests(unittest.TestCase):
    def test_excluded_return_does_not_count_as_a_decliner(self):
        frame = pd.DataFrame(
            [
                {
                    "theme_id": "AI_SERVER",
                    "theme_name": "AI伺服器",
                    "stock_id": "2382",
                    "weekly_return_pct": 1.5,
                    "price_strong": False,
                    "volume_strong": False,
                    "abc_group": "",
                },
                {
                    "theme_id": "AI_SERVER",
                    "theme_name": "AI伺服器",
                    "stock_id": "6669",
                    "weekly_return_pct": None,
                    "price_strong": False,
                    "volume_strong": False,
                    "abc_group": "",
                },
            ]
        )

        result = aggregate(frame, "theme_id", "theme_name").iloc[0]

        self.assertEqual(result["mapped_stock_count"], 2)
        self.assertAlmostEqual(result["avg_weekly_return_pct"], 1.5)
        self.assertAlmostEqual(result["up_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()

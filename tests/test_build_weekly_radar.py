from __future__ import annotations

import unittest

import pandas as pd

from scripts import build_weekly_radar as radar


def stock_rows(stock_id: str, closes: list[float], volumes: list[float] | None = None):
    volumes = volumes or [2_000_000.0] * len(closes)
    dates = pd.date_range("2026-08-26", periods=len(closes), freq="B")
    return pd.DataFrame(
        {
            "date": dates,
            "stock_id": stock_id,
            "close": closes,
            "volume_shares": volumes,
            "turnover_ntd": [close * volume for close, volume in zip(closes, volumes)],
        }
    )


class CorporateActionGuardTests(unittest.TestCase):
    def test_ex_rights_price_discontinuity_is_excluded_from_signals(self):
        frame = stock_rows("6669", [6785, 6800, 6820, 6790, 6785, 2610])

        enriched = radar.enrich(frame)
        snapshot = radar.snapshot_for_date(enriched, enriched["date"].max())
        row = snapshot.iloc[0]

        self.assertAlmostEqual(row["weekly_return_raw_pct"], -61.53279292557111)
        self.assertTrue(row["corporate_action_suspect"])
        self.assertTrue(pd.isna(row["weekly_return_pct"]))
        self.assertFalse(row["signal_eligible"])
        self.assertFalse(row["price_strong"])
        self.assertFalse(row["volume_strong"])
        self.assertEqual(row["abc_group"], "")
        self.assertEqual(
            row["signal_exclusion_reason"],
            "corporate_action_or_price_discontinuity",
        )

    def test_normal_weekly_return_remains_eligible(self):
        frame = stock_rows("1234", [100, 101, 102, 103, 104, 106])

        enriched = radar.enrich(frame)
        snapshot = radar.snapshot_for_date(enriched, enriched["date"].max())
        row = snapshot.iloc[0]

        self.assertAlmostEqual(row["weekly_return_raw_pct"], 6.0)
        self.assertAlmostEqual(row["weekly_return_pct"], 6.0)
        self.assertFalse(row["corporate_action_suspect"])
        self.assertTrue(row["signal_eligible"])
        self.assertTrue(row["price_strong"])
        self.assertEqual(row["abc_group"], "B")

    def test_five_limit_up_sessions_are_not_falsely_excluded(self):
        frame = stock_rows("5678", [100, 110, 121, 133.1, 146.41, 161.051])

        enriched = radar.enrich(frame)
        snapshot = radar.snapshot_for_date(enriched, enriched["date"].max())
        row = snapshot.iloc[0]

        self.assertAlmostEqual(row["weekly_return_pct"], 61.051, places=3)
        self.assertFalse(row["corporate_action_suspect"])
        self.assertTrue(row["signal_eligible"])


if __name__ == "__main__":
    unittest.main()

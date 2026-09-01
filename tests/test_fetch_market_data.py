from __future__ import annotations

from datetime import date
import sys
import types
import unittest
from unittest.mock import patch

try:
    import requests  # noqa: F401
except ModuleNotFoundError:
    # The test exercises injected fake sessions; keep it runnable in the
    # bundled offline Python runtime where requests may not be installed.
    requests_stub = types.ModuleType("requests")
    requests_stub.Session = object
    sys.modules["requests"] = requests_stub

from scripts import fetch_market_data as market


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


def tpex_payload():
    return {
        "tables": [{
            "fields": ["代號", "名稱", "開盤", "最高", "最低", "收盤", "成交量", "成交金額"],
            "data": [["1234", "測試", "10", "11", "9", "10.5", "1,000", "10,500"]],
        }]
    }


class TpexSessionTests(unittest.TestCase):
    def test_prepare_tpex_session_visits_first_party_page(self):
        session = FakeSession([FakeResponse()])

        market.prepare_tpex_session(session)

        self.assertEqual(session.calls[0][0], market.TPEX_PAGE)
        self.assertEqual(session.calls[0][1]["headers"], market.HEADERS)

    @patch.object(market.time, "sleep", return_value=None)
    def test_edge_error_refreshes_cookie_and_retries_query(self, _sleep):
        session = FakeSession([
            FakeResponse(status_code=520),
            FakeResponse(),
            FakeResponse(payload=tpex_payload()),
        ])

        frame = market.fetch_tpex_for_day(session, date(2026, 8, 28))

        self.assertEqual([call[0] for call in session.calls], [
            market.TPEX_HIST,
            market.TPEX_PAGE,
            market.TPEX_HIST,
        ])
        self.assertEqual(session.calls[0][1]["headers"], market.TPEX_HEADERS)
        self.assertEqual(len(frame), 1)
        self.assertEqual(frame.iloc[0]["market"], "TPEx")
        self.assertEqual(frame.iloc[0]["stock_id"], "1234")


if __name__ == "__main__":
    unittest.main()

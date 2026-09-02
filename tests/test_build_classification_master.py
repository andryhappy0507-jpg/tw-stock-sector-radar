from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import patch

try:
    import requests  # noqa: F401
except ModuleNotFoundError:
    requests_stub = types.ModuleType("requests")
    requests_stub.Session = object
    sys.modules["requests"] = requests_stub

from scripts import build_classification_master as classification


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


class ClassificationApiTests(unittest.TestCase):
    @patch.object(classification.time, "sleep", return_value=None)
    def test_non_json_response_cools_down_and_retries(self, sleep):
        session = FakeSession([
            FakeResponse(ValueError("empty response")),
            FakeResponse([{"公司代號": "1234"}]),
        ])

        payload = classification.fetch_json(session, classification.TWSE_URL)

        self.assertEqual(payload, [{"公司代號": "1234"}])
        self.assertEqual(len(session.calls), 2)
        sleep.assert_called_once_with(classification.API_RETRY_BASE_SECONDS)

    @patch.object(classification.time, "sleep", return_value=None)
    def test_retry_delay_is_capped(self, sleep):
        failures = [FakeResponse(ValueError("empty response")) for _ in range(5)]
        session = FakeSession(failures + [FakeResponse([])])

        self.assertEqual(classification.fetch_json(session, classification.TWSE_URL), [])
        self.assertEqual(
            [call.args[0] for call in sleep.call_args_list],
            [10, 20, 40, 60, 60],
        )


if __name__ == "__main__":
    unittest.main()

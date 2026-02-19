from __future__ import annotations

import time
from typing import Any
import requests

from tests.integration.config import BASE_URL, REQUEST_TIMEOUT_SECONDS


def url(path: str) -> str:
    return f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def wait_for_api_ready(timeout_seconds: float = 60.0) -> None:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None

    while time.time() < deadline:
        try:
            response = requests.get(url("/openapi.json"), timeout=REQUEST_TIMEOUT_SECONDS)
            if response.status_code == 200:
                return
        except Exception as exc:  # pragma: no cover - integration reliability helper
            last_error = exc
        time.sleep(1)

    if last_error:
        raise AssertionError(f"API did not become ready. Last error: {last_error}")
    raise AssertionError("API did not become ready within timeout.")


def request_json(method: str, path: str, expected_status: int, payload: dict[str, Any] | None = None) -> dict[str, Any] | list[dict[str, Any]]:
    response = requests.request(
        method=method,
        url=url(path),
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    if response.status_code != expected_status:
        raise AssertionError(
            f"Unexpected status for {method} {path}. "
            f"Expected {expected_status}, got {response.status_code}. Body={response.text}"
        )

    if not response.content:
        return {}

    return response.json()

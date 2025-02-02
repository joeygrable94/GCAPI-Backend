from typing import Any
from unittest.mock import MagicMock

from app.entities.ipaddress.dependencies import get_request_ip


class MockRequest:
    def __init__(self, client_host: Any = None, headers: dict[str, str] = {}) -> None:
        if client_host is None:
            client_host = "::0"
        self.client = MagicMock(host=client_host)
        self.headers = headers

    def get(self, header_name: str) -> str | None:
        if self.headers:
            return self.headers.get(header_name)
        return None


def test_get_request_ip() -> None:
    # Create a mock Request with X-Forwarded-For header
    request = MockRequest(
        headers={"X-Forwarded-For": "192.168.1.1, 192.168.1.2, 192.168.1.3"}
    )
    assert get_request_ip(request) == "192.168.1.1"  # type: ignore

    # Create a mock Request with client host
    request = MockRequest(client_host="192.168.1.1")
    assert get_request_ip(request) == "192.168.1.1"  # type: ignore

    # Create a mock Request without X-Forwarded-For header or client host
    request = MockRequest()
    assert get_request_ip(request) == "::0"  # type: ignore

    # Create a mock Request with invalid X-Forwarded-For header
    request = MockRequest(headers={"X-Forwarded-For": "invalid_ip"})
    assert get_request_ip(request) == "invalid_ip"  # type: ignore

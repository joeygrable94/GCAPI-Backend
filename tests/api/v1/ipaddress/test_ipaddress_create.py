from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode

pytestmark = pytest.mark.asyncio


async def test_create_ipaddress_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    address: str = random_lower_string()
    data: Dict[str, str] = {"address": address}
    response: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["address"] == address


async def test_create_ipaddress_as_superuser_address_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    address: str = random_lower_string()
    data: Dict[str, str] = {"address": address}
    response: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["address"] == address
    data_2: Dict[str, str] = {"address": address}
    response_2: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == "IpAddress exists"


async def test_create_ipaddress_as_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
) -> None:
    address: str = random_lower_string()
    data: Dict[str, str] = {"address": address}
    response: Response = await client.post(
        "ip/",
        headers=testuser_token_headers,
        json=data,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_create_ipaddress_as_superuser_address_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    address: str = "::"
    data: Dict[str, str] = {"address": address}
    response: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "ip addresses must contain 3 or more characters"


async def test_create_ipaddress_as_superuser_address_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    address: str = random_lower_string() * 10
    data: Dict[str, str] = {"address": address}
    response: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "ip addresses must contain less than 64 characters"
    )


async def test_create_ipaddress_as_superuser_isp_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    address: str = random_lower_string()
    isp: str = random_lower_string() * 10
    data: Dict[str, str] = {"address": address, "isp": isp}
    response: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "ip internet service providers must contain less than 255 characters"
    )


async def test_create_ipaddress_as_superuser_location_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    address: str = random_lower_string()
    location: str = random_lower_string() * 50
    data: Dict[str, str] = {"address": address, "location": location}
    response: Response = await client.post(
        "ip/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "ip location must contain less than 500 characters"
    )

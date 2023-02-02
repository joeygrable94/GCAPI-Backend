from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.ipaddress import create_random_ipaddress
from tests.utils.utils import random_lower_string

from app.db.schemas import IpAddressRead, IpAddressUpdate

pytestmark = pytest.mark.asyncio


async def test_update_ipaddress_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: IpAddressRead = await create_random_ipaddress(db_session)
    entry_b: IpAddressRead = await create_random_ipaddress(db_session)
    update_dict = IpAddressUpdate(
        address=entry_b.address,
    )
    response: Response = await client.patch(
        f"ip/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.dict(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == "IpAddress exists"


async def test_update_ipaddress_as_superuser_address_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: IpAddressRead = await create_random_ipaddress(db_session)
    address: str = "::"
    data: Dict[str, str] = {"address": address}
    response: Response = await client.patch(
        f"ip/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "ip addresses must contain 3 or more characters"
    )


async def test_update_ipaddress_as_superuser_address_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: IpAddressRead = await create_random_ipaddress(db_session)
    address: str = random_lower_string() * 10
    data: Dict[str, str] = {"address": address}
    response: Response = await client.patch(
        f"ip/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "ip addresses must contain less than 64 characters"
    )


async def test_update_ipaddress_as_superuser_isp_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: IpAddressRead = await create_random_ipaddress(db_session)
    isp: str = random_lower_string() * 10
    data: Dict[str, str] = {"isp": isp}
    response: Response = await client.patch(
        f"ip/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "ip internet service providers must contain less than 255 characters"
    )


async def test_update_ipaddress_as_superuser_location_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: IpAddressRead = await create_random_ipaddress(db_session)
    location: str = random_lower_string() * 50
    data: Dict[str, str] = {"location": location}
    response: Response = await client.patch(
        f"ip/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "ip location must contain less than 500 characters"
    )

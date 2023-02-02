from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.ipaddress import create_random_ipaddress

from app.api.errors import ErrorCode
from app.db.schemas.ipaddress import IpAddressRead

pytestmark = pytest.mark.asyncio


async def test_list_ipaddress_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_1: IpAddressRead = await create_random_ipaddress(db_session)
    entry_2: IpAddressRead = await create_random_ipaddress(db_session)
    response: Response = await client.get("ip/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) > 1
    for entry in all_entries:
        assert "address" in entry
        if entry["address"] == entry_1.address:
            assert entry["address"] == entry_1.address
        if entry["address"] == entry_2.address:
            assert entry["address"] == entry_2.address


async def test_list_ipaddress_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry_1: IpAddressRead = await create_random_ipaddress(db_session)  # noqa: F841
    entry_2: IpAddressRead = await create_random_ipaddress(db_session)  # noqa: F841
    response: Response = await client.get("ip/", headers=testuser_token_headers)
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS

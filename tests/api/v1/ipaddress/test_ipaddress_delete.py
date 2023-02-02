from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.ipaddress import create_random_ipaddress

from app.api.errors import ErrorCode
from app.db.repositories.ipaddress import IpAddressRepository
from app.db.schemas.ipaddress import IpAddressRead

pytestmark = pytest.mark.asyncio


async def test_delete_ipaddress_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: IpAddressRead = await create_random_ipaddress(db_session)
    response: Response = await client.delete(
        f"ip/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: IpAddressRepository = IpAddressRepository(db_session)
    data_not_found: Optional[Any] = await repo.read_by("address", entry.address)
    assert data_not_found is None


async def test_delete_ipaddress_by_id_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry: IpAddressRead = await create_random_ipaddress(db_session)
    response_b: Response = await client.delete(
        f"ip/{entry.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response_b.json()
    assert response_b.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS

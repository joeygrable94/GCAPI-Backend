from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.api.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.db.repositories import ClientRepository
from app.db.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_read_client_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    repo: ClientRepository = ClientRepository(db_session)
    existing_data: Any = await repo.read_by("title", entry.title)
    assert existing_data
    assert existing_data.title == data["title"]


async def test_read_client_by_id_as_superuser_client_not_found(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"clients/{entry_id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Client not found"


async def test_read_client_by_id_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS

from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.api.exceptions import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import ClientRepository
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_read_client_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    repo: ClientRepository = ClientRepository(db_session)
    existing_data: Any = await repo.read_by("title", entry.title)
    assert existing_data
    assert existing_data.title == data["title"]


async def test_read_client_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"clients/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND

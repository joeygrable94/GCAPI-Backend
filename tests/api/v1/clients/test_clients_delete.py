from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.crud import ClientRepository
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_delete_client_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.delete(
        f"clients/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: ClientRepository = ClientRepository(db_session)
    data_not_found: Optional[Any] = await repo.read_by("title", entry.title)
    assert data_not_found is None

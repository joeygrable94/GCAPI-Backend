from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.sharpspring import create_random_sharpspring

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import SharpspringRepository
from app.models import Sharpspring
from app.schemas import ClientRead, SharpspringRead

pytestmark = pytest.mark.asyncio


async def test_read_sharpspring_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    response: Response = await client.get(
        f"sharpspring/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "api_key" in data
    assert "secret_key" in data
    assert data["client_id"] == str(a_client.id)
    repo: SharpspringRepository = SharpspringRepository(db_session)
    existing_data: Sharpspring | None = await repo.read_by("api_key", entry.api_key)
    assert existing_data
    assert existing_data.api_key == data["api_key"]
    assert existing_data.secret_key == data["secret_key"]
    assert str(existing_data.client_id) == data["client_id"]


async def test_read_sharpspring_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"sharpspring/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.SHARPSPRING_NOT_FOUND

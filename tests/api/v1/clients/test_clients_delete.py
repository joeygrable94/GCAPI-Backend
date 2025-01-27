from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models import User
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_delete_client_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.delete(
        f"clients/{entry.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_delete_client_by_id_as_client_a(
    client: AsyncClient,
    db_session: AsyncSession,
    client_a_token_headers: Dict[str, str],
) -> None:
    client_a: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_client_a
    )
    a_client: ClientRead = await create_random_client(db_session)
    await assign_user_to_client(db_session, client_a, a_client)
    response: Response = await client.delete(
        f"clients/{a_client.id}",
        headers=client_a_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["message"] == "Client requested to be deleted"
    assert data["user_id"] == str(client_a.id)
    assert data["client_id"] == str(a_client.id)

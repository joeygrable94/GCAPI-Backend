from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import create_random_client

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,user_count",
    [
        ("admin_user", 4),
        ("manager_user", 4),
        ("verified_user", 4),
    ],
)
async def test_list_public_clients_as_superuser(
    client_user: Any,
    user_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    entry_1 = await create_random_client(db_session)
    await create_random_client(db_session, is_active=False)
    entry_3 = await create_random_client(db_session)
    response: Response = await client.get(
        "clients/public", headers=current_user.token_headers
    )
    assert 200 <= response.status_code < 300
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == user_count
    assert data["size"] == 1000
    assert len(data["results"]) == user_count
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry

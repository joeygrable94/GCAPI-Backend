from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.client.constants import ERROR_MESSAGE_CLIENT_NOT_FOUND
from app.entities.client.crud import ClientRepository
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,status_code",
    [
        ("admin_user", 200),
        ("manager_user", 200),
        ("employee_user", 200),
        ("verified_user", 403),
    ],
)
async def test_read_client_by_id_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_client = await create_random_client(db_session)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    response: Response = await client.get(
        f"clients/{a_client.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert data["id"] == str(a_client.id)
        repo = ClientRepository(db_session)
        existing_data = await repo.read_by("title", a_client.title)
        assert existing_data
        assert existing_data.title == data["title"]


async def test_read_client_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"clients/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ERROR_MESSAGE_CLIENT_NOT_FOUND

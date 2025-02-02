from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        ("employee_user"),
        ("client_a_user"),
        ("client_b_user"),
    ],
)
async def test_read_website_by_id_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    if this_user.is_superuser:
        a_website = await create_random_website(db_session)
    else:
        a_website = await create_random_website(db_session)
        a_client = await create_random_client(db_session)
        await assign_website_to_client(db_session, a_website.id, a_client.id)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    response: Response = await client.get(
        f"websites/{a_website.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(a_website.id)


async def test_read_website_by_id_as_superuser_website_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"websites/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

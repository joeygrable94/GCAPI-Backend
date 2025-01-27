from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_client",
    [
        ("admin_user", False),
        ("manager_user", True),
        ("employee_user", True),
        pytest.param(
            "manager_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "employee_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
    ],
    ids=[
        "admin user read any website page",
        "manager user read assiged website page",
        "employee user read assigned website page",
        "manager user fails on read unassigned website page",
        "employee user fails on read unassigned website page",
    ],
)
async def test_delete_website_page_by_id_as_user(
    client_user: Any,
    assign_client: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    a_entry = await create_random_website_page(db_session, a_website.id)
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
        await assign_website_to_client(db_session, a_website.id, a_client.id)
    response: Response = await client.get(
        f"webpages/{a_entry.id}",
        headers=current_user.token_headers,
    )
    assert 200 <= response.status_code < 300


async def test_read_website_page_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"webpages/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]

from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

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
    "client_user,user_count,query_website,query_inactive,assign_user",
    [
        ("admin_user", 7, False, False, False),
        ("admin_user", 3, True, False, False),
        ("admin_user", 1, False, True, False),
        ("employee_user", 0, False, False, False),
        ("employee_user", 1, False, False, True),
        ("client_a_user", 1, False, False, True),
    ],
    ids=[
        "admin user list all website pages",
        "admin user list all website pages by website",
        "admin user list all website pages by is_active=False",
        "employee user do not list unassigned website pages",
        "employee user list assigned website pages",
        "client user list assigned website pages",
    ],
)
async def test_list_all_websites_as_user(
    client_user: Any,
    user_count: int,
    query_website: bool,
    query_inactive: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_client = await create_random_client(db_session)
    b_client = await create_random_client(db_session)
    c_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session, is_secure=True)
    b_website = await create_random_website(db_session, is_secure=False)
    c_website = await create_random_website(db_session, is_secure=True)
    d_website = await create_random_website(db_session, is_secure=True)
    if assign_user:
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, b_client.id)
    await assign_website_to_client(db_session, b_website.id, a_client.id)
    await assign_website_to_client(db_session, b_website.id, b_client.id)
    await assign_website_to_client(db_session, c_website.id, c_client.id)
    await create_random_website_page(db_session, a_website.id)
    await create_random_website_page(db_session, a_website.id)
    await create_random_website_page(db_session, a_website.id)
    await create_random_website_page(db_session, b_website.id)
    await create_random_website_page(db_session, c_website.id)
    await create_random_website_page(db_session, d_website.id)
    await create_random_website_page(db_session, d_website.id, is_active=False)
    query_params: dict[str, Any] | None = None
    if query_website:
        query_params = {}
        query_params["website_id"] = str(a_website.id)
    if query_inactive:
        query_params = {} if query_params is None else query_params
        query_params["is_active"] = False
    print(query_params)
    response: Response = await client.get(
        "webpages/",
        headers=current_user.token_headers,
        params=query_params,
    )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == user_count
    assert data["size"] == 1000
    assert len(data["results"]) == user_count

from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.website_maps import create_random_website_map
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,user_count,query_website,query_sitemap,assign_user",
    [
        ("admin_user", 14, False, False, False),
        ("admin_user", 6, True, False, False),
        ("admin_user", 5, False, True, False),
        ("admin_user", 2, True, True, False),
        ("employee_user", 0, False, False, False),
        ("employee_user", 3, False, False, True),
        ("client_a_user", 3, False, False, True),
    ],
    ids=[
        "admin user list all website pages",
        "admin user list all website pages by website",
        "admin user list all website pages by sitemap",
        "admin user list all website pages by website and sitemap",
        "employee user do not list unassigned website pages",
        "employee user list assigned website pages",
        "client user list assigned website pages",
    ],
)
async def test_list_all_websites_as_user(
    client_user: Any,
    user_count: int,
    query_website: bool,
    query_sitemap: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user: User = await get_user_by_email(db_session, current_user.email)
    a_client = await create_random_client(db_session)
    b_client = await create_random_client(db_session)
    c_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session, is_secure=True)
    b_website = await create_random_website(db_session, is_secure=False)
    c_website = await create_random_website(db_session, is_secure=True)
    d_website = await create_random_website(db_session, is_secure=True)
    a_sitemap = await create_random_website_map(db_session, a_website.id)
    b_sitemap = await create_random_website_map(db_session, b_website.id)
    c_sitemap = await create_random_website_map(db_session, c_website.id)
    if assign_user:
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, b_client.id)
    await assign_website_to_client(db_session, b_website.id, a_client.id)
    await assign_website_to_client(db_session, b_website.id, b_client.id)
    await assign_website_to_client(db_session, c_website.id, c_client.id)

    await create_random_website_page(db_session, a_website.id, a_sitemap.id)
    await create_random_website_page(db_session, a_website.id, a_sitemap.id)
    await create_random_website_page(db_session, a_website.id, a_sitemap.id)
    await create_random_website_page(db_session, a_website.id, a_sitemap.id)
    await create_random_website_page(db_session, a_website.id, b_sitemap.id)
    await create_random_website_page(db_session, a_website.id, b_sitemap.id)
    await create_random_website_page(db_session, b_website.id, b_sitemap.id)
    await create_random_website_page(db_session, b_website.id, b_sitemap.id)
    await create_random_website_page(db_session, b_website.id, b_sitemap.id)
    await create_random_website_page(db_session, c_website.id, c_sitemap.id)
    await create_random_website_page(db_session, c_website.id, c_sitemap.id)
    await create_random_website_page(db_session, d_website.id)
    await create_random_website_page(db_session, d_website.id)
    await create_random_website_page(db_session, d_website.id)

    query_params: dict[str, Any] | None = (
        None if not query_website and not query_sitemap else {}
    )
    if query_website:
        query_params["website_id"] = str(a_website.id)
    if query_sitemap:
        query_params["sitemap_id"] = str(b_sitemap.id)

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

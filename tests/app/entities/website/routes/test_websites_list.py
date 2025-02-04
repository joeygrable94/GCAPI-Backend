from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,user_count,query_client,assign_user",
    [
        ("admin_user", 3, False, False),
        ("manager_user", 3, False, False),
        ("employee_user", 1, False, True),
        ("admin_user", 2, True, False),
        ("manager_user", 2, True, False),
        ("employee_user", 0, False, False),
    ],
)
async def test_list_all_websites_as_user(
    client_user: Any,
    user_count: int,
    query_client: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    c_organization = await create_random_organization(db_session)
    website_a = await create_random_website(db_session, is_secure=True)
    website_b = await create_random_website(db_session, is_secure=False)
    website_c = await create_random_website(db_session, is_secure=True)
    if not this_user.is_superuser and assign_user:
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    await assign_website_to_organization(db_session, website_a.id, b_organization.id)
    await assign_website_to_organization(db_session, website_b.id, a_organization.id)
    await assign_website_to_organization(db_session, website_b.id, b_organization.id)
    await assign_website_to_organization(db_session, website_c.id, c_organization.id)
    if query_client:
        response: Response = await client.get(
            "websites/",
            params={"organization_id": str(b_organization.id)},
            headers=current_user.token_headers,
        )
    else:
        response: Response = await client.get(
            "websites/", headers=current_user.token_headers
        )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == user_count
    assert data["size"] == 1000
    assert len(data["results"]) == user_count

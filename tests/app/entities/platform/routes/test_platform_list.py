from typing import Any

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_platform_to_client,
    assign_user_to_client,
    create_random_client,
)
from tests.utils.platform import create_random_platform, get_platform_by_slug
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,query_item,assign_client,item_count",
    [
        ("admin_user", False, False, 10),
        ("admin_user", True, False, 3),
        ("admin_user", {"is_active": False}, False, 2),
        ("manager_user", False, False, 10),
        ("admin_user", {"is_active": False}, False, 2),
        ("client_a_user", False, True, 3),
        ("client_a_user", {"is_active": False}, True, 1),
        ("employee_user", False, False, 3),
        ("client_b_user", False, False, 0),
    ],
    ids=[
        "admin user list all platforms",
        "admin user list platforms by client_id",
        "admin user list all inactive platforms",
        "manager list all platforms",
        "manager list all inactive platforms",
        "client user list all platforms assigned to client",
        "client user list all inactive platforms assigned to client",
        "employee user list all platforms assigned (default 3 assigned to client_a)",
        "client user list no platforms assigned to client_b",
    ],
)
async def test_list_all_platform_as_superuser(
    client_user: Any,
    query_item: bool | dict,
    assign_client: bool,
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await get_platform_by_slug(db_session, "bdx")
    b_platform = await get_platform_by_slug(db_session, "spsp")
    c_platform = await create_random_platform(db_session, is_active=False)
    d_platform = await get_platform_by_slug(db_session, "ga4")
    e_platform = await create_random_platform(db_session, is_active=False)
    a_client = await create_random_client(db_session)
    b_client = await create_random_client(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    await assign_platform_to_client(db_session, b_platform.id, a_client.id)
    await assign_platform_to_client(db_session, c_platform.id, a_client.id)
    await assign_platform_to_client(db_session, d_platform.id, b_client.id)
    await assign_platform_to_client(db_session, e_platform.id, b_client.id)
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)

    response: Response
    query_params: QueryParams | None = None
    if isinstance(query_item, dict):
        query_params = QueryParams(**query_item)
    elif query_item:
        query_params = QueryParams(client_id=a_client.id)
    response = await client.get(
        "platforms/",
        headers=current_user.token_headers,
        params=query_params,
    )
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == item_count
    assert data["size"] == 1000
    assert len(data["results"]) == item_count

from typing import Any

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas import ClientRead
from app.schemas.go import GooglePlatformType
from app.schemas.platform import PlatformRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_platform_to_client,
    assign_user_to_client,
    create_random_client,
)
from tests.utils.ga4 import create_random_ga4_property
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_client,item_count",
    [
        ("admin_user", False, 2),
        ("manager_user", False, 2),
        ("employee_user", False, 0),
        ("employee_user", True, 1),
        (
            "employee_user",
            False,
            0,
        ),
    ],
)
async def test_list_go_property_ga4_by_id_as_user(
    client_user: Any,
    assign_client: bool,
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform: PlatformRead = await create_random_platform(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_client: ClientRead = await create_random_client(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    await create_random_ga4_property(db_session, a_client.id, a_platform.id)
    await create_random_ga4_property(db_session, b_client.id, a_platform.id)
    if assign_client:
        this_user: User = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    query_params = QueryParams()
    response: Response = await client.get(
        f"go/{platform_type}",
        params=query_params,
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == item_count
    assert data["size"] == 1000
    assert len(data["results"]) == item_count


async def test_list_go_property_ga4_by_client_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_platform: PlatformRead = await create_random_platform(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_client: ClientRead = await create_random_client(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    await create_random_ga4_property(db_session, a_client.id, a_platform.id)
    await create_random_ga4_property(db_session, b_client.id, a_platform.id)

    this_user: User = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    query_params = QueryParams(client_id=a_client.id)
    response: Response = await client.get(
        f"go/{platform_type}",
        params=query_params,
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1

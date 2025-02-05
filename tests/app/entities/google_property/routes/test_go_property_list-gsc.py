from typing import Any

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.go_property.schemas import GooglePlatformType
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.go_sc import create_random_go_search_console_property
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_organization,item_count",
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
async def test_list_go_property_gsc_by_id_as_user(
    client_user: Any,
    assign_organization: bool,
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    await create_random_go_search_console_property(
        db_session, a_organization.id, a_website.id, a_platform.id
    )
    await create_random_go_search_console_property(
        db_session, b_organization.id, b_website.id, a_platform.id
    )
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_website_to_organization(db_session, a_website.id, a_organization.id)
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


async def test_list_go_property_gsc_as_superuser_by_organization_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    await create_random_go_search_console_property(
        db_session, a_organization.id, a_website.id, a_platform.id
    )
    await create_random_go_search_console_property(
        db_session, b_organization.id, b_website.id, a_platform.id
    )
    query_params = QueryParams(organization_id=a_organization.id)
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


async def test_list_go_property_gsc_as_superuser_by_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    await create_random_go_search_console_property(
        db_session, a_organization.id, a_website.id, a_platform.id
    )
    await create_random_go_search_console_property(
        db_session, b_organization.id, b_website.id, a_platform.id
    )
    query_params = QueryParams(website_id=a_website.id)
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

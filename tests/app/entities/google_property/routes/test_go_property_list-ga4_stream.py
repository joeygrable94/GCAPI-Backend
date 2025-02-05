from typing import Any

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.go_property.schemas import GooglePlatformType
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION,
)
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,item_count",
    [
        ("admin_user", 2),
        ("manager_user", 2),
        ("employee_user", 0),
        pytest.param(
            "verified_user",
            0,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION
            ),
        ),
    ],
)
async def test_list_go_property_ga4_stream_by_id_as_user(
    client_user: Any,
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    a_ga4 = await create_random_ga4_property(db_session, a_organization.id, a_platform.id)
    b_ga4 = await create_random_ga4_property(db_session, b_organization.id, a_platform.id)
    await create_random_ga4_stream(db_session, a_ga4.id, a_website.id)
    await create_random_ga4_stream(db_session, b_ga4.id, b_website.id)
    response: Response = await client.get(
        f"go/{platform_type}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == item_count
    assert data["size"] == 1000
    assert len(data["results"]) == item_count


async def test_list_go_property_ga4_stream_as_superuser_by_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    a_ga4 = await create_random_ga4_property(db_session, a_organization.id, a_platform.id)
    b_ga4 = await create_random_ga4_property(db_session, b_organization.id, a_platform.id)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    await assign_website_to_organization(db_session, b_website.id, b_organization.id)
    await create_random_ga4_stream(db_session, a_ga4.id, a_website.id)
    await create_random_ga4_stream(db_session, b_ga4.id, b_website.id)
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


async def test_list_go_property_ga4_stream_as_superuser_by_ga4_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    a_ga4 = await create_random_ga4_property(db_session, a_organization.id, a_platform.id)
    b_ga4 = await create_random_ga4_property(db_session, b_organization.id, a_platform.id)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    await assign_website_to_organization(db_session, b_website.id, b_organization.id)
    await create_random_ga4_stream(db_session, a_ga4.id, a_website.id)
    await create_random_ga4_stream(db_session, b_ga4.id, b_website.id)
    query_params = QueryParams(ga4_id=b_ga4.id)
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

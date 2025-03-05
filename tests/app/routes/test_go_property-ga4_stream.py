from typing import Any, AsyncGenerator

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
    ERROR_MESSAGE_INPUT_SCHEMA_INVALID,
)
from app.entities.go_property.schemas import GooglePlatformType
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform, get_platform_by_slug
from tests.utils.users import get_user_by_auth_id
from tests.utils.utils import random_lower_string
from tests.utils.websites import assign_ga4_to_website, create_random_website

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="module")
async def ga4_stream_db_session(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    await create_random_platform(
        db_session, GooglePlatformType.ga4.value, "Google Analytics 4"
    )
    yield db_session


async def perform_test_list(
    status_code: int,
    error_msg: str | None,
    item_count: int,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await create_random_platform(ga4_stream_db_session)
    a_organization = await create_random_organization(ga4_stream_db_session)
    b_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    b_website = await create_random_website(ga4_stream_db_session)
    await assign_platform_to_organization(
        ga4_stream_db_session, a_platform.id, a_organization.id
    )
    a_ga4 = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )
    b_ga4 = await create_random_ga4_property(
        ga4_stream_db_session, b_organization.id, a_platform.id
    )
    await create_random_ga4_stream(ga4_stream_db_session, a_ga4.id, a_website.id)
    await create_random_ga4_stream(ga4_stream_db_session, b_ga4.id, b_website.id)
    response: Response = await client.get(
        f"go/{platform_type}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert data["page"] == 1
        assert data["total"] == item_count
        assert data["size"] == 1000
        assert len(data["results"]) == item_count
    else:
        assert error_msg in data["detail"]


async def perform_test_create(
    assign_organization: bool,
    assign_website: bool,
    expected_status_code: int,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(
        ga4_stream_db_session, GooglePlatformType.ga4.value
    )
    a_organization = await create_random_organization(ga4_stream_db_session)
    b_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    b_website = await create_random_website(ga4_stream_db_session)
    a_ga4_property = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )

    if assign_organization:
        this_user = await get_user_by_auth_id(
            ga4_stream_db_session, current_user.auth_id
        )
        await assign_user_to_organization(
            ga4_stream_db_session, this_user.id, a_organization.id
        )
        await assign_user_to_organization(
            ga4_stream_db_session, this_user.id, b_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, a_website.id, a_organization.id
        )

    data_in = {
        "title": random_lower_string(),
        "stream_id": random_lower_string(10),
        "measurement_id": random_lower_string(10),
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }

    if assign_website:
        data_in["organization_id"] = str(b_organization.id)
        data_in["website_id"] = str(b_website.id)

    response: Response = await client.post(
        f"go/{platform_type}",
        headers=current_user.token_headers,
        json=data_in,
    )

    entry = response.json()
    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        del data_in["organization_id"]
        assert all(item in entry.items() for item in data_in.items())


async def perform_test_limits_create(
    title: str,
    stream_id: str,
    measurement_id: str,
    expected_status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(
        ga4_stream_db_session, GooglePlatformType.ga4.value
    )
    a_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    a_ga4_property = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )
    this_user = await get_user_by_auth_id(ga4_stream_db_session, admin_user.auth_id)
    await assign_user_to_organization(
        ga4_stream_db_session, this_user.id, a_organization.id
    )
    await assign_website_to_organization(
        ga4_stream_db_session, a_website.id, a_organization.id
    )
    data_in = {
        "title": title,
        "stream_id": stream_id,
        "measurement_id": measurement_id,
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry = response.json()
    assert expected_status_code == response.status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]
    if error_type is None:
        del data_in["organization_id"]
        assert all(item in entry.items() for item in data_in.items())


async def perform_test_read(
    assign_organization: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await create_random_platform(ga4_stream_db_session)
    a_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    await assign_platform_to_organization(
        ga4_stream_db_session, a_platform.id, a_organization.id
    )
    a_ga4_property = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )
    a_ga4_stream_property = await create_random_ga4_stream(
        ga4_stream_db_session, a_ga4_property.id, a_website.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(
            ga4_stream_db_session, current_user.auth_id
        )
        await assign_user_to_organization(
            ga4_stream_db_session, this_user.id, a_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, a_website.id, a_organization.id
        )
        await assign_ga4_to_website(
            ga4_stream_db_session, a_ga4_property.id, a_website.id
        )
    response: Response = await client.get(
        f"go/{platform_type}/{a_ga4_stream_property.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data["id"] == str(a_ga4_stream_property.id)


async def perform_test_update(
    assign_organization: bool,
    assign_website: bool,
    status_code: int,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(
        ga4_stream_db_session, GooglePlatformType.ga4.value
    )
    a_organization = await create_random_organization(ga4_stream_db_session)
    b_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    b_website = await create_random_website(ga4_stream_db_session)
    a_ga4_property = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )
    a_ga4_stream = await create_random_ga4_stream(
        ga4_stream_db_session, a_ga4_property.id, a_website.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(
            ga4_stream_db_session, current_user.auth_id
        )
        await assign_user_to_organization(
            ga4_stream_db_session, this_user.id, a_organization.id
        )
        await assign_user_to_organization(
            ga4_stream_db_session, this_user.id, b_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, a_website.id, a_organization.id
        )
    data_in: dict[str, Any] = {
        "title": random_lower_string(),
        "website_id": str(a_website.id),
    }
    if assign_website:
        data_in["website_id"] = str(b_website.id)
    response: Response = await client.patch(
        f"go/{platform_type}/{a_ga4_stream.id}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert all(item in entry.items() for item in data_in.items())


async def perform_test_limits_update(
    title: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(
        ga4_stream_db_session, GooglePlatformType.ga4.value
    )
    a_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    a_ga4_property = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )
    a_ga4_stream = await create_random_ga4_stream(
        ga4_stream_db_session, a_ga4_property.id, a_website.id
    )
    this_user = await get_user_by_auth_id(ga4_stream_db_session, admin_user.auth_id)
    await assign_user_to_organization(
        ga4_stream_db_session, this_user.id, a_organization.id
    )
    await assign_website_to_organization(
        ga4_stream_db_session, a_website.id, a_organization.id
    )
    data_in: dict[str, Any] = {
        "title": title,
        "website_id": str(a_website.id),
    }
    response: Response = await client.patch(
        f"go/{platform_type}/{a_ga4_stream.id}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]
    if error_type is None:
        assert all(item in entry.items() for item in data_in.items())


async def perform_test_delete(
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    ga4_stream_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await create_random_platform(ga4_stream_db_session)
    a_organization = await create_random_organization(ga4_stream_db_session)
    a_website = await create_random_website(ga4_stream_db_session)
    await assign_platform_to_organization(
        ga4_stream_db_session, a_platform.id, a_organization.id
    )
    a_ga4_property = await create_random_ga4_property(
        ga4_stream_db_session, a_organization.id, a_platform.id
    )
    a_ga4_stream = await create_random_ga4_stream(
        ga4_stream_db_session, a_ga4_property.id, a_website.id
    )
    this_user = await get_user_by_auth_id(ga4_stream_db_session, current_user.auth_id)
    await assign_user_to_organization(
        ga4_stream_db_session, this_user.id, a_organization.id
    )
    await assign_website_to_organization(
        ga4_stream_db_session, a_website.id, a_organization.id
    )
    response: Response = await client.delete(
        f"go/{platform_type}/{a_ga4_stream.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] | None = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data is None


class TestListGoPropertyGa4Stream:
    # AUTHORIZED CLIENTS
    async def test_list_go_property_ga4_stream_by_id_as_admin_user(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_list(200, None, 2, client, ga4_stream_db_session, admin_user)

    async def test_list_go_property_ga4_stream_by_id_as_manager_user(
        self, client, ga4_stream_db_session, manager_user
    ) -> None:
        await perform_test_list(
            200, None, 4, client, ga4_stream_db_session, manager_user
        )

    async def test_list_go_property_ga4_stream_by_id_as_employee_user(
        self, client, ga4_stream_db_session, employee_user
    ) -> None:
        await perform_test_list(
            200, None, 0, client, ga4_stream_db_session, employee_user
        )

    async def test_list_go_property_ga4_stream_by_id_as_verified_user(
        self, client, ga4_stream_db_session, verified_user
    ) -> None:
        await perform_test_list(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION,
            0,
            client,
            ga4_stream_db_session,
            verified_user,
        )

    # CASES
    async def test_list_go_property_ga4_stream_as_superuser_by_website_id(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await create_random_platform(ga4_stream_db_session)
        a_organization = await create_random_organization(ga4_stream_db_session)
        b_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        b_website = await create_random_website(ga4_stream_db_session)
        a_ga4 = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        b_ga4 = await create_random_ga4_property(
            ga4_stream_db_session, b_organization.id, a_platform.id
        )
        await assign_platform_to_organization(
            ga4_stream_db_session, a_platform.id, a_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, a_website.id, a_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, b_website.id, b_organization.id
        )
        await create_random_ga4_stream(ga4_stream_db_session, a_ga4.id, a_website.id)
        await create_random_ga4_stream(ga4_stream_db_session, b_ga4.id, b_website.id)
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
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await create_random_platform(ga4_stream_db_session)
        a_organization = await create_random_organization(ga4_stream_db_session)
        b_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        b_website = await create_random_website(ga4_stream_db_session)
        a_ga4 = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        b_ga4 = await create_random_ga4_property(
            ga4_stream_db_session, b_organization.id, a_platform.id
        )
        await assign_platform_to_organization(
            ga4_stream_db_session, a_platform.id, a_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, a_website.id, a_organization.id
        )
        await assign_website_to_organization(
            ga4_stream_db_session, b_website.id, b_organization.id
        )
        await create_random_ga4_stream(ga4_stream_db_session, a_ga4.id, a_website.id)
        await create_random_ga4_stream(ga4_stream_db_session, b_ga4.id, b_website.id)
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


class TestCreateGoPropertyGa4Stream:
    # AUTHORIZED CLIENTS
    async def test_create_go_property_ga4_stream_as_admin_user(
        self, client, ga4_stream_db_session, admin_user
    ):
        await perform_test_create(
            False, False, 200, client, ga4_stream_db_session, admin_user
        )

    async def test_create_go_property_ga4_stream_as_manager_user(
        self, client, ga4_stream_db_session, manager_user
    ):
        await perform_test_create(
            False, False, 200, client, ga4_stream_db_session, manager_user
        )

    async def test_create_go_property_ga4_stream_as_employee_user(
        self, client, ga4_stream_db_session, employee_user
    ):
        await perform_test_create(
            False, False, 405, client, ga4_stream_db_session, employee_user
        )

    async def test_create_go_property_ga4_stream_as_client_a_user(
        self, client, ga4_stream_db_session, client_a_user
    ):
        await perform_test_create(
            False, False, 405, client, ga4_stream_db_session, client_a_user
        )

    async def test_create_go_property_ga4_stream_as_client_a_user_with_org(
        self, client, ga4_stream_db_session, client_a_user
    ):
        await perform_test_create(
            True, False, 200, client, ga4_stream_db_session, client_a_user
        )

    async def test_create_go_property_ga4_stream_as_client_a_user_with_org_and_website(
        self, client, ga4_stream_db_session, client_a_user
    ):
        await perform_test_create(
            True, True, 405, client, ga4_stream_db_session, client_a_user
        )

    # LIMITS
    async def test_create_go_property_ga4_stream_as_superuser_success(
        self, client, ga4_stream_db_session, admin_user
    ):
        await perform_test_limits_create(
            random_lower_string(5),
            random_lower_string(10),
            random_lower_string(10),
            200,
            None,
            None,
            client,
            ga4_stream_db_session,
            admin_user,
        )

    async def test_create_go_property_ga4_stream_as_superuser_title_too_short(
        self, client, ga4_stream_db_session, admin_user
    ):
        await perform_test_limits_create(
            random_lower_string(4),
            random_lower_string(10),
            random_lower_string(10),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
            client,
            ga4_stream_db_session,
            admin_user,
        )

    async def test_create_go_property_ga4_stream_as_superuser_title_too_long(
        self, client, ga4_stream_db_session, admin_user
    ):
        await perform_test_limits_create(
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            random_lower_string(10),
            random_lower_string(10),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
            client,
            ga4_stream_db_session,
            admin_user,
        )

    # CASES
    async def test_create_go_property_ga4_stream_as_superuser_invalid_schema(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await get_platform_by_slug(
            ga4_stream_db_session, GooglePlatformType.ga4.value
        )
        a_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        a_ga4_property = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        title = random_lower_string()
        stream_id = random_lower_string()
        measurement_id = random_lower_string()
        data_in: dict[str, Any] = {
            "title": title,
            "stream_id": stream_id,
            "property_id": measurement_id,
            "ga4_id": str(a_ga4_property.id),
            "organization_id": str(a_organization.id),
            "website_id": str(a_website.id),
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 422
        assert ERROR_MESSAGE_INPUT_SCHEMA_INVALID in entry["detail"]

    async def test_create_go_property_ga4_stream_as_superuser_title_exists(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await get_platform_by_slug(
            ga4_stream_db_session, GooglePlatformType.ga4.value
        )
        a_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        a_ga4_property = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        a_ga4_stream = await create_random_ga4_stream(
            ga4_stream_db_session, a_ga4_property.id, a_website.id
        )
        stream_id = random_lower_string(10)
        measurement_id = random_lower_string(10)
        data_in: dict[str, Any] = {
            "title": a_ga4_stream.title,
            "stream_id": stream_id,
            "measurement_id": measurement_id,
            "ga4_id": str(a_ga4_property.id),
            "organization_id": str(a_organization.id),
            "website_id": str(a_website.id),
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]
        assert "GoAnalytics4Stream" in entry["detail"]

    async def test_create_go_property_ga4_stream_as_superuser_website_not_found(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await get_platform_by_slug(
            ga4_stream_db_session, GooglePlatformType.ga4.value
        )
        a_organization = await create_random_organization(ga4_stream_db_session)
        a_ga4_property = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        title = random_lower_string(10)
        stream_id = random_lower_string(10)
        measurement_id = random_lower_string(10)
        bad_website_id = get_uuid_str()
        data_in: dict[str, Any] = {
            "title": title,
            "stream_id": stream_id,
            "measurement_id": measurement_id,
            "ga4_id": str(a_ga4_property.id),
            "organization_id": str(a_organization.id),
            "website_id": bad_website_id,
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]

    async def test_create_go_property_ga4_stream_as_superuser_ga4_property_not_found(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        title = random_lower_string(10)
        stream_id = random_lower_string(10)
        measurement_id = random_lower_string(10)
        bad_ga4_id = get_uuid_str()
        data_in: dict[str, Any] = {
            "title": title,
            "stream_id": stream_id,
            "measurement_id": measurement_id,
            "ga4_id": bad_ga4_id,
            "organization_id": str(a_organization.id),
            "website_id": str(a_website.id),
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]


class TestReadGoPropertyGa4Stream:
    # AUTHORIZED CLIENTS
    async def test_read_go_property_ga4_stream_by_id_as_admin_user(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_read(
            False, 200, None, None, client, ga4_stream_db_session, admin_user
        )

    async def test_read_go_property_ga4_stream_by_id_as_manager_user(
        self, client, ga4_stream_db_session, manager_user
    ) -> None:
        await perform_test_read(
            False, 200, None, None, client, ga4_stream_db_session, manager_user
        )

    async def test_read_go_property_ga4_stream_by_id_as_employee_user(
        self, client, ga4_stream_db_session, employee_user
    ) -> None:
        await perform_test_read(
            False,
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            ga4_stream_db_session,
            employee_user,
        )

    async def test_read_go_property_ga4_stream_by_id_as_client_a_user(
        self, client, ga4_stream_db_session, client_a_user
    ) -> None:
        await perform_test_read(
            False,
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            ga4_stream_db_session,
            client_a_user,
        )

    async def test_read_go_property_ga4_stream_by_id_as_client_a_user_assoc_organzation(
        self, client, ga4_stream_db_session, client_a_user
    ) -> None:
        await perform_test_read(
            True, 200, None, None, client, ga4_stream_db_session, client_a_user
        )

    # CASES
    async def test_read_go_property_ga4_stream_by_id_as_superuser_not_found(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"go/{platform_type}/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestUpdateGoPropertyGa4Stream:
    # AUTHORIZED CLIENTS
    async def test_update_go_property_ga4_stream_as_admin_user(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_update(
            False, False, 200, client, ga4_stream_db_session, admin_user
        )

    async def test_update_go_property_ga4_stream_as_manager_user(
        self, client, ga4_stream_db_session, manager_user
    ) -> None:
        await perform_test_update(
            False, False, 200, client, ga4_stream_db_session, manager_user
        )

    async def test_update_go_property_ga4_stream_as_employee_user(
        self, client, ga4_stream_db_session, employee_user
    ) -> None:
        await perform_test_update(
            False, False, 405, client, ga4_stream_db_session, employee_user
        )

    async def test_update_go_property_ga4_stream_as_client_a_user(
        self, client, ga4_stream_db_session, client_a_user
    ) -> None:
        await perform_test_update(
            False, False, 405, client, ga4_stream_db_session, client_a_user
        )

    async def test_update_go_property_ga4_stream_as_client_a_user_assign_org(
        self, client, ga4_stream_db_session, client_a_user
    ) -> None:
        await perform_test_update(
            True, False, 200, client, ga4_stream_db_session, client_a_user
        )

    async def test_update_go_property_ga4_stream_as_client_a_user_assign_org_assigned_website(
        self, client, ga4_stream_db_session, client_a_user
    ) -> None:
        await perform_test_update(
            True, True, 405, client, ga4_stream_db_session, client_a_user
        )

    # LIMITS
    async def test_update_go_property_ga4_stream_as_superuser_limits(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(5),
            200,
            None,
            None,
            client,
            ga4_stream_db_session,
            admin_user,
        )

    async def test_update_go_property_ga4_stream_as_superuser_limits_title_short(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(4),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
            client,
            ga4_stream_db_session,
            admin_user,
        )

    async def test_update_go_property_ga4_stream_as_superuser_limits_title_long(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
            client,
            ga4_stream_db_session,
            admin_user,
        )

    # CASES
    async def test_update_go_property_ga4_stream_as_superuser_title_exists(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await get_platform_by_slug(
            ga4_stream_db_session, GooglePlatformType.ga4.value
        )
        a_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        b_website = await create_random_website(ga4_stream_db_session)
        a_ga4_property = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        a_ga4_stream = await create_random_ga4_stream(
            ga4_stream_db_session, a_ga4_property.id, a_website.id
        )
        b_ga4_stream = await create_random_ga4_stream(
            ga4_stream_db_session, a_ga4_property.id, b_website.id
        )
        data_in: dict[str, Any] = {
            "title": b_ga4_stream.title,
            "website_id": str(a_website.id),
        }
        response: Response = await client.patch(
            f"go/{platform_type}/{a_ga4_stream.id}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]
        assert "GoAnalytics4Stream" in entry["detail"]

    async def test_update_go_property_ga4_stream_as_superuser_website_not_found(
        self,
        client: AsyncClient,
        ga4_stream_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        a_platform = await get_platform_by_slug(
            ga4_stream_db_session, GooglePlatformType.ga4.value
        )
        a_organization = await create_random_organization(ga4_stream_db_session)
        a_website = await create_random_website(ga4_stream_db_session)
        a_ga4_property = await create_random_ga4_property(
            ga4_stream_db_session, a_organization.id, a_platform.id
        )
        a_ga4_stream = await create_random_ga4_stream(
            ga4_stream_db_session, a_ga4_property.id, a_website.id
        )
        title = random_lower_string(10)
        bad_website_id = get_uuid_str()
        data_in: dict[str, Any] = {
            "title": title,
            "website_id": bad_website_id,
        }
        response: Response = await client.patch(
            f"go/{platform_type}/{a_ga4_stream.id}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]


class TestDeleteGoPropertyGa4Stream:
    # AUTHORIZED CLIENTS
    async def test_delete_go_property_ga4_stream_by_id_as_admin_user(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        await perform_test_delete(
            200, None, None, client, ga4_stream_db_session, admin_user
        )

    async def test_delete_go_property_ga4_stream_by_id_as_manager_user(
        self, client, ga4_stream_db_session, manager_user
    ) -> None:
        await perform_test_delete(
            200, None, None, client, ga4_stream_db_session, manager_user
        )

    async def test_delete_go_property_ga4_stream_by_id_as_employee_user(
        self, client, ga4_stream_db_session, employee_user
    ) -> None:
        await perform_test_delete(
            403,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            ga4_stream_db_session,
            employee_user,
        )

    # CASES
    async def test_delete_go_property_ga4_stream_by_id_as_superuser_not_found(
        self, client, ga4_stream_db_session, admin_user
    ) -> None:
        platform_type = GooglePlatformType.ga4_stream.value
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"go/{platform_type}/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

from typing import Any, AsyncGenerator

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
    ERROR_MESSAGE_INPUT_SCHEMA_INVALID,
)
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
)
from app.entities.go_property.schemas import GooglePlatformType
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.ga4 import create_random_ga4_property
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform, get_platform_by_slug
from tests.utils.users import get_user_by_auth_id
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="module")
async def ga4_db_session(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    await create_random_platform(
        db_session, GooglePlatformType.ga4.value, "Google Analytics 4"
    )
    yield db_session


async def perform_test_create(
    assign_organization: bool,
    status_code: int,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_platform = await get_platform_by_slug(
        ga4_db_session, GooglePlatformType.ga4.value
    )
    a_organization = await create_random_organization(ga4_db_session)
    if assign_organization:
        this_user = await get_user_by_auth_id(ga4_db_session, current_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
    data_in: dict[str, Any] = {
        "title": random_lower_string(),
        "property_id": random_lower_string(10),
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert all(item in entry.items() for item in data_in.items())
        assert entry["platform_id"] == str(a_platform.id)


async def perform_test_limits_create(
    title: str,
    property_id: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(
        ga4_db_session, GooglePlatformType.ga4.value
    )
    platform_type = GooglePlatformType.ga4.value
    a_organization = await create_random_organization(ga4_db_session)
    this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
    await assign_user_to_organization(ga4_db_session, this_user.id, a_organization.id)
    data_in: dict[str, Any] = {
        "title": title,
        "property_id": property_id,
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
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
        assert entry["platform_id"] == str(a_platform.id)


async def perform_test_list(
    assign_organization: bool,
    item_count: int,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_platform = await create_random_platform(ga4_db_session)
    b_organization = await create_random_organization(ga4_db_session)
    a_organization = await create_random_organization(ga4_db_session)
    await assign_platform_to_organization(
        ga4_db_session, a_platform.id, a_organization.id
    )
    await create_random_ga4_property(ga4_db_session, a_organization.id, a_platform.id)
    await create_random_ga4_property(ga4_db_session, b_organization.id, a_platform.id)
    if assign_organization:
        this_user = await get_user_by_auth_id(ga4_db_session, current_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
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


async def perform_test_read(
    assign_organization: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_platform = await create_random_platform(ga4_db_session)
    a_organization = await create_random_organization(ga4_db_session)
    await assign_platform_to_organization(
        ga4_db_session, a_platform.id, a_organization.id
    )
    a_ga4_property = await create_random_ga4_property(
        ga4_db_session, a_organization.id, a_platform.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(ga4_db_session, current_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
    response: Response = await client.get(
        f"go/{platform_type}/{a_ga4_property.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data["id"] == str(a_ga4_property.id)


async def perform_test_update(
    assign_organization: bool | None,
    status_code: int,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_platform = await get_platform_by_slug(
        ga4_db_session, GooglePlatformType.ga4.value
    )
    a_organization = await create_random_organization(ga4_db_session)
    if assign_organization:
        this_user = await get_user_by_auth_id(ga4_db_session, current_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
    a_ga4 = await create_random_ga4_property(
        ga4_db_session, a_organization.id, a_platform.id
    )
    data_in: dict[str, Any] = {
        "title": random_lower_string(),
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.patch(
        f"go/{platform_type}/{a_ga4.id}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert all(item in entry.items() for item in data_in.items())
        assert entry["platform_id"] == str(a_platform.id)


async def perform_test_limits_update(
    title: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(
        ga4_db_session, GooglePlatformType.ga4.value
    )
    platform_type = GooglePlatformType.ga4.value
    a_organization = await create_random_organization(ga4_db_session)
    this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
    await assign_user_to_organization(ga4_db_session, this_user.id, a_organization.id)
    a_ga4 = await create_random_ga4_property(
        ga4_db_session, a_organization.id, a_platform.id
    )
    data_in: dict[str, Any] = {
        "title": title,
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.patch(
        f"go/{platform_type}/{a_ga4.id}",
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
        assert entry["platform_id"] == str(a_platform.id)


async def perform_test_delete(
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    ga4_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_platform = await create_random_platform(ga4_db_session)
    a_organization = await create_random_organization(ga4_db_session)
    await assign_platform_to_organization(
        ga4_db_session, a_platform.id, a_organization.id
    )
    a_ga4_property = await create_random_ga4_property(
        ga4_db_session, a_organization.id, a_platform.id
    )
    this_user = await get_user_by_auth_id(ga4_db_session, current_user.auth_id)
    await assign_user_to_organization(ga4_db_session, this_user.id, a_organization.id)
    response: Response = await client.delete(
        f"go/{platform_type}/{a_ga4_property.id}",
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


class TestListGoPropertyGa4Property:
    # AUTHORIZED CLIENTS
    async def test_list_go_property_ga4_by_id_as_admin_user(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_list(False, 2, client, ga4_db_session, admin_user)

    async def test_list_go_property_ga4_by_id_as_manager_user(
        self, client, ga4_db_session, manager_user
    ) -> None:
        await perform_test_list(False, 4, client, ga4_db_session, manager_user)

    async def test_list_go_property_ga4_by_id_as_employee_user_not_assoc_with_organization(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_list(False, 0, client, ga4_db_session, employee_user)

    async def test_list_go_property_ga4_by_id_as_employee_user_assoc_with_organization(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_list(True, 1, client, ga4_db_session, employee_user)

    # CASES
    async def test_list_go_property_ga4_by_organization_id(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4.value
        a_platform = await create_random_platform(ga4_db_session)
        b_organization = await create_random_organization(ga4_db_session)
        a_organization = await create_random_organization(ga4_db_session)
        await assign_platform_to_organization(
            ga4_db_session, a_platform.id, a_organization.id
        )
        await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        await create_random_ga4_property(
            ga4_db_session, b_organization.id, a_platform.id
        )

        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
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


class TestCreateGoPropertyGa4Property:
    # AUTHORIZED CLIENTS
    async def test_create_go_property_ga4_as_admin_user(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_create(False, 200, client, ga4_db_session, admin_user)

    async def test_create_go_property_ga4_as_manager_user(
        self, client, ga4_db_session, manager_user
    ) -> None:
        await perform_test_create(False, 200, client, ga4_db_session, manager_user)

    async def test_create_go_property_ga4_as_employee_user(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_create(False, 405, client, ga4_db_session, employee_user)

    async def test_create_go_property_ga4_as_client_a_user(
        self, client, ga4_db_session, client_a_user
    ) -> None:
        await perform_test_create(False, 405, client, ga4_db_session, client_a_user)

    async def test_create_go_property_ga4_as_client_a_user_assoc_with_organization(
        self, client, ga4_db_session, client_a_user
    ) -> None:
        await perform_test_create(True, 200, client, ga4_db_session, client_a_user)

    # LIMITS
    async def test_create_go_property_ga4_as_superuser_limits(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(5),
            random_lower_string(16),
            200,
            None,
            None,
            client,
            ga4_db_session,
            admin_user,
        )

    async def test_create_go_property_ga4_as_superuser_title_too_short(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(4),
            random_lower_string(16),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
            client,
            ga4_db_session,
            admin_user,
        )

    async def test_create_go_property_ga4_as_superuser_title_too_long(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            random_lower_string(16),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
            client,
            ga4_db_session,
            admin_user,
        )

    async def test_create_go_property_ga4_as_superuser_property_id_required(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            "",
            422,
            "detail",
            "Value error, property_id is required",
            client,
            ga4_db_session,
            admin_user,
        )

    async def test_create_go_property_ga4_as_superuser_property_id_too_long(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            random_lower_string(DB_STR_16BIT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, property_id must be {DB_STR_16BIT_MAXLEN_INPUT} characters or less",
            client,
            ga4_db_session,
            admin_user,
        )

    # CASES
    async def test_create_go_property_ga4_as_superuser_invalid_schema(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4.value
        a_organization = await create_random_organization(ga4_db_session)
        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
        title = random_lower_string()
        property_id = random_lower_string(10)
        data_in: dict[str, Any] = {
            "title": title,
            "measurement_id": property_id,
            "organization_id": str(a_organization.id),
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 422
        assert ERROR_MESSAGE_INPUT_SCHEMA_INVALID in entry["detail"]

    async def test_create_go_property_ga4_as_superuser_title_exists(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_platform = await get_platform_by_slug(
            ga4_db_session, GooglePlatformType.ga4.value
        )
        platform_type = GooglePlatformType.ga4.value
        a_organization = await create_random_organization(ga4_db_session)
        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
        a_ga4_property = await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        property_id = random_lower_string(10)
        data_in: dict[str, Any] = {
            "title": a_ga4_property.title,
            "property_id": property_id,
            "organization_id": str(a_organization.id),
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]

    async def test_create_go_property_ga4_as_superuser_property_id_exists(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_platform = await get_platform_by_slug(
            ga4_db_session, GooglePlatformType.ga4.value
        )
        platform_type = GooglePlatformType.ga4.value
        a_organization = await create_random_organization(ga4_db_session)
        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
        a_ga4_property = await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        title = random_lower_string()
        data_in: dict[str, Any] = {
            "title": title,
            "property_id": a_ga4_property.property_id,
            "organization_id": str(a_organization.id),
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]

    async def test_create_go_property_ga4_as_superuser_organization_not_found(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_platform = await get_platform_by_slug(
            ga4_db_session, GooglePlatformType.ga4.value
        )
        platform_type = GooglePlatformType.ga4.value
        a_organization = await create_random_organization(ga4_db_session)
        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
        await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        title = random_lower_string()
        property_id = random_lower_string(10)
        bad_organization_id = get_uuid_str()
        data_in: dict[str, Any] = {
            "title": title,
            "property_id": property_id,
            "organization_id": bad_organization_id,
        }
        response: Response = await client.post(
            f"go/{platform_type}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ORGANIZATION_NOT_FOUND in entry["detail"]


class TestReadGoPropertyGa4Property:
    # AUTHORIZED CLIENTS
    async def test_read_go_property_ga4_by_id_as_admin_user(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_read(
            False, 200, None, None, client, ga4_db_session, admin_user
        )

    async def test_read_go_property_ga4_by_id_as_manager_user(
        self, client, ga4_db_session, manager_user
    ) -> None:
        await perform_test_read(
            False, 200, None, None, client, ga4_db_session, manager_user
        )

    async def test_read_go_property_ga4_by_id_as_employee_user_assoc_with_organization(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_read(
            True, 200, None, None, client, ga4_db_session, employee_user
        )

    async def test_read_go_property_ga4_by_id_as_employee_user_not_assoc_with_organization(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_read(
            False,
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            ga4_db_session,
            employee_user,
        )

    # CASES
    async def test_read_go_property_ga4_by_id_as_superuser_not_found(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4.value
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"go/{platform_type}/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestUpdateGoPropertyGa4Property:
    # AUTHORIZED CLIENTS
    async def test_update_go_property_ga4_as_admin_user(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_update(False, 200, client, ga4_db_session, admin_user)

    async def test_update_go_property_ga4_as_manager_user(
        self, client, ga4_db_session, manager_user
    ) -> None:
        await perform_test_update(False, 200, client, ga4_db_session, manager_user)

    async def test_update_go_property_ga4_as_employee_user(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_update(False, 405, client, ga4_db_session, employee_user)

    async def test_update_go_property_ga4_as_client_a_user(
        self, client, ga4_db_session, client_a_user
    ) -> None:
        await perform_test_update(False, 405, client, ga4_db_session, client_a_user)

    async def test_update_go_property_ga4_as_client_a_user_assign_org(
        self, client, ga4_db_session, client_a_user
    ) -> None:
        await perform_test_update(True, 200, client, ga4_db_session, client_a_user)

    # LIMITS
    async def test_update_go_property_ga4_as_superuser_limits_success(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(5), 200, None, None, client, ga4_db_session, admin_user
        )

    async def test_update_go_property_ga4_as_superuser_limits_title_short(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(4),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
            client,
            ga4_db_session,
            admin_user,
        )

    async def test_update_go_property_ga4_as_superuser_limits_title_long(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
            client,
            ga4_db_session,
            admin_user,
        )

    # CASES
    async def test_update_go_property_ga4_as_superuser_title_exists(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4.value
        a_platform = await get_platform_by_slug(ga4_db_session, platform_type)
        a_organization = await create_random_organization(ga4_db_session)
        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
        a_ga4 = await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        b_ga4 = await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        data_in: dict[str, Any] = {
            "title": b_ga4.title,
            "organization_id": str(a_organization.id),
        }
        response: Response = await client.patch(
            f"go/{platform_type}/{a_ga4.id}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]

    async def test_update_go_property_ga4_as_superuser_organization_not_found(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_platform = await get_platform_by_slug(
            ga4_db_session, GooglePlatformType.ga4.value
        )
        platform_type = GooglePlatformType.ga4.value
        a_organization = await create_random_organization(ga4_db_session)
        this_user = await get_user_by_auth_id(ga4_db_session, admin_user.auth_id)
        await assign_user_to_organization(
            ga4_db_session, this_user.id, a_organization.id
        )
        a_ga4 = await create_random_ga4_property(
            ga4_db_session, a_organization.id, a_platform.id
        )
        title = random_lower_string()
        bad_organization_id = get_uuid_str()
        data_in: dict[str, Any] = {
            "title": title,
            "organization_id": bad_organization_id,
        }
        response: Response = await client.patch(
            f"go/{platform_type}/{a_ga4.id}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ORGANIZATION_NOT_FOUND in entry["detail"]


class TestDeleteGoPropertyGa4Property:
    # AUTHORIZED CLIENTS
    async def test_delete_go_property_ga4_by_id_as_admin_user(
        self, client, ga4_db_session, admin_user
    ) -> None:
        await perform_test_delete(200, None, None, client, ga4_db_session, admin_user)

    async def test_delete_go_property_ga4_by_id_as_manager_user(
        self, client, ga4_db_session, manager_user
    ) -> None:
        await perform_test_delete(200, None, None, client, ga4_db_session, manager_user)

    async def test_delete_go_property_ga4_by_id_as_employee_user(
        self, client, ga4_db_session, employee_user
    ) -> None:
        await perform_test_delete(
            403,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            ga4_db_session,
            employee_user,
        )

    # CASES
    async def test_delete_go_property_ga4_by_id_as_superuser_not_found(
        self,
        client: AsyncClient,
        ga4_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        platform_type = GooglePlatformType.ga4.value
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"go/{platform_type}/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

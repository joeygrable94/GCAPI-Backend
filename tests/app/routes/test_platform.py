from typing import Any, AsyncGenerator

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
)
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.go_property.schemas import GooglePlatformType
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform, get_platform_by_slug
from tests.utils.users import get_user_by_auth_id
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.anyio


DUPLICATE_PLATFORM_SLUG = random_lower_string()
DUPLICATE_PLATFORM_TITLE = random_lower_string()
DUPLICATE_PLATFORM_SLUG = random_lower_string()
DUPLICATE_PLATFORM_TITLE = random_lower_string()


@pytest.fixture(scope="module")
async def platform_db_session(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    await create_random_platform(
        db_session, GooglePlatformType.ga4.value, "Google Analytics 4"
    )
    await create_random_platform(
        db_session, GooglePlatformType.gsc.value, "Google Search Console"
    )
    await create_random_platform(
        db_session, GooglePlatformType.gads.value, "Google Ads"
    )
    await create_random_platform(
        db_session, DUPLICATE_PLATFORM_SLUG, DUPLICATE_PLATFORM_TITLE
    )
    yield db_session


async def perform_test_list(
    query_item: bool | dict,
    assign_organization: bool,
    item_count: int,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(platform_db_session, "gsc")
    b_platform = await get_platform_by_slug(platform_db_session, "gads")
    c_platform = await create_random_platform(platform_db_session, is_active=False)
    d_platform = await get_platform_by_slug(platform_db_session, "ga4")
    e_platform = await create_random_platform(platform_db_session, is_active=False)
    a_organization = await create_random_organization(platform_db_session)
    b_organization = await create_random_organization(platform_db_session)
    await assign_platform_to_organization(
        platform_db_session, a_platform.id, a_organization.id
    )
    await assign_platform_to_organization(
        platform_db_session, b_platform.id, a_organization.id
    )
    await assign_platform_to_organization(
        platform_db_session, c_platform.id, a_organization.id
    )
    await assign_platform_to_organization(
        platform_db_session, d_platform.id, b_organization.id
    )
    await assign_platform_to_organization(
        platform_db_session, e_platform.id, b_organization.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(platform_db_session, current_user.auth_id)
        await assign_user_to_organization(
            platform_db_session, this_user.id, a_organization.id
        )
    response: Response
    query_params: QueryParams | None = None
    if isinstance(query_item, dict):
        query_params = QueryParams(**query_item)
    elif query_item:
        query_params = QueryParams(organization_id=a_organization.id)
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


async def perform_test_create(
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    data_in: dict[str, Any] = {
        "slug": random_lower_string(),
        "title": random_lower_string(),
    }
    response: Response = await client.post(
        "platforms/",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert all(item in entry.items() for item in data_in.items())
    else:
        assert entry["detail"] == error_msg


async def perform_test_limits_create(
    slug: str,
    title: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data_in: dict[str, Any] = {
        "slug": slug,
        "title": title,
    }
    response: Response = await client.post(
        "platforms/",
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


async def perform_test_read(
    assign_organization: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_platform = await create_random_platform(platform_db_session)
    a_organization = await create_random_organization(platform_db_session)
    await assign_platform_to_organization(
        platform_db_session, a_platform.id, a_organization.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(platform_db_session, current_user.auth_id)
        await assign_user_to_organization(
            platform_db_session, this_user.id, a_organization.id
        )
    response: Response = await client.get(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data["id"] == str(a_platform.id)


async def perform_test_update(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(platform_db_session)
    a_platform = await get_platform_by_slug(
        platform_db_session, DUPLICATE_PLATFORM_SLUG
    )
    await assign_platform_to_organization(
        platform_db_session, a_organization.id, a_platform.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(platform_db_session, current_user.auth_id)
        await assign_user_to_organization(
            platform_db_session, this_user.id, a_organization.id
        )
    data_in: dict[str, Any] = {
        "description": random_lower_string(),
    }
    response: Response = await client.patch(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert all(item in entry.items() for item in data_in.items())
    else:
        assert entry["detail"] == error_msg


async def perform_test_limits_update(
    assign_organization: bool,
    title: str | None,
    desc: str | None,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(platform_db_session)
    a_platform = await get_platform_by_slug(
        platform_db_session, DUPLICATE_PLATFORM_SLUG
    )
    await assign_platform_to_organization(
        platform_db_session, a_organization.id, a_platform.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(platform_db_session, current_user.auth_id)
        await assign_user_to_organization(
            platform_db_session, this_user.id, a_organization.id
        )
    data_in: dict[str, Any] = {}
    if title is not None:
        data_in["title"] = title
    if desc is not None:
        data_in["description"] = desc
    response: Response = await client.patch(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
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
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    platform_db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(platform_db_session)
    a_platform = await create_random_platform(platform_db_session)
    await assign_platform_to_organization(
        platform_db_session, a_platform.id, a_organization.id
    )
    if assign_organization:
        this_user = await get_user_by_auth_id(platform_db_session, current_user.auth_id)
        await assign_user_to_organization(
            platform_db_session, this_user.id, a_organization.id
        )
    response: Response = await client.delete(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        response: Response = await client.get(
            f"platforms/{a_platform.id}",
            headers=current_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
    else:
        assert entry["detail"] == error_msg


class TestListPlatform:
    # AUTHORIZED CLIENTS
    async def test_list_all_platform_as_admin_user(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_list(
            False, False, 6, client, platform_db_session, admin_user
        )

    async def test_list_all_platform_as_admin_user_by_org(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_list(True, False, 3, client, platform_db_session, admin_user)

    async def test_list_all_platform_as_admin_user_by_inactive(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_list(
            {"is_active": False}, False, 6, client, platform_db_session, admin_user
        )

    async def test_list_all_platform_as_manager_user(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_list(
            False, False, 12, client, platform_db_session, manager_user
        )

    async def test_list_all_platform_as_client_a_user(
        self, client, platform_db_session, client_a_user
    ) -> None:
        await perform_test_list(
            False, True, 3, client, platform_db_session, client_a_user
        )

    async def test_list_all_platform_as_client_a_user_by_inactive(
        self, client, platform_db_session, client_a_user
    ) -> None:
        await perform_test_list(
            {"is_active": False}, True, 2, client, platform_db_session, client_a_user
        )

    async def test_list_all_platform_as_employee_user(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_list(
            False, False, 0, client, platform_db_session, employee_user
        )

    async def test_list_all_platform_as_client_b_user(
        self, client, platform_db_session, client_b_user
    ) -> None:
        await perform_test_list(
            False, False, 0, client, platform_db_session, client_b_user
        )


class TestCreatePlatform:
    # AUTHORIZED CLIENTS
    async def test_create_platform_as_admin_user(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_create(200, None, client, platform_db_session, admin_user)

    async def test_create_platform_as_manager_user(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_create(200, None, client, platform_db_session, manager_user)

    async def test_create_platform_as_employee_user(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            employee_user,
        )

    async def test_create_platform_as_client_a_user(
        self, client, platform_db_session, client_a_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            client_a_user,
        )

    async def test_create_platform_as_client_b_user(
        self, client, platform_db_session, client_b_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            client_b_user,
        )

    async def test_create_platform_as_verified_user(
        self, client, platform_db_session, verified_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            verified_user,
        )

    async def test_create_platform_as_unverified_user(
        self, client, platform_db_session, unverified_user
    ) -> None:
        await perform_test_create(
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            platform_db_session,
            unverified_user,
        )

    # LIMITS
    async def test_create_platform_limits_as_admin(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            random_lower_string(),
            200,
            None,
            None,
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_slug_req(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            None,
            random_lower_string(),
            422,
            "detail",
            "Value error, slug is required",
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_slug_too_short(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            "aa",
            random_lower_string(),
            422,
            "detail",
            f"Value error, slug must be {3} characters or more",
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_slug_too_long(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            "a" * (DB_STR_64BIT_MAXLEN_INPUT + 1),
            random_lower_string(),
            422,
            "detail",
            f"Value error, slug must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less",
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_title_req(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            "",
            422,
            "detail",
            "Value error, title is required",
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_title_too_short(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            "aa",
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_title_too_long(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_duplicate_slug_and_title(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            DUPLICATE_PLATFORM_SLUG,
            DUPLICATE_PLATFORM_TITLE,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_duplicate_slug(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            DUPLICATE_PLATFORM_SLUG,
            random_lower_string(),
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            client,
            platform_db_session,
            admin_user,
        )

    async def test_create_platform_limits_as_admin_duplicate_title(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(),
            DUPLICATE_PLATFORM_TITLE,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            client,
            platform_db_session,
            admin_user,
        )


class TestReadPlatform:
    # AUTHORIZED CLIENTS
    async def test_read_platform_by_id_as_admin_user(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_read(
            False, 200, None, None, client, platform_db_session, admin_user
        )

    async def test_read_platform_by_id_as_manager_user(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_read(
            False, 200, None, None, client, platform_db_session, manager_user
        )

    async def test_read_platform_by_id_as_employee_user_assoc_organization(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_read(
            True, 200, None, None, client, platform_db_session, employee_user
        )

    async def test_read_platform_by_id_as_employee_user_not_assoc_organization(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_read(
            False,
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            employee_user,
        )

    # CASES
    async def test_read_platform_by_id_as_superuser_not_found(
        self,
        client: AsyncClient,
        platform_db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"platforms/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestUpdatePlatform:
    # AUTHORIZED CLIENTS
    async def test_update_platform_as_admin_user(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_update(
            False, 200, None, client, platform_db_session, admin_user
        )

    async def test_update_platform_as_manager_user(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_update(
            False, 200, None, client, platform_db_session, manager_user
        )

    async def test_update_platform_as_employee_user(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_update(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            employee_user,
        )

    async def test_update_platform_as_client_a_user(
        self, client, platform_db_session, client_a_user
    ) -> None:
        await perform_test_update(
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            platform_db_session,
            client_a_user,
        )

    async def test_update_platform_as_unverified_user(
        self, client, platform_db_session, unverified_user
    ) -> None:
        await perform_test_update(
            False,
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            platform_db_session,
            unverified_user,
        )

    # LIMITS
    async def test_update_platform_as_admin_user_assoc_org_and_platform_update_description(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            True,
            None,
            random_lower_string(),
            200,
            None,
            None,
            client,
            platform_db_session,
            admin_user,
        )

    async def test_update_platform_as_manager_user_assoc_org_and_platform_update_description(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_limits_update(
            True,
            None,
            random_lower_string(),
            200,
            None,
            None,
            client,
            platform_db_session,
            manager_user,
        )

    async def test_update_platform_as_manager_user_assoc_org_and_platform_update_description_and_title(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_limits_update(
            True,
            random_lower_string(),
            random_lower_string(),
            200,
            None,
            None,
            client,
            platform_db_session,
            manager_user,
        )

    async def test_update_platform_as_employee_user_assoc_org_and_platform_update_title_action_not_allowed(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_limits_update(
            True,
            random_lower_string(),
            random_lower_string(),
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
            client,
            platform_db_session,
            employee_user,
        )

    async def test_update_platform_as_employee_user_not_assoc_org_not_platform(
        self, client, platform_db_session, employee_user
    ) -> None:
        await perform_test_limits_update(
            False,
            None,
            random_lower_string(),
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            platform_db_session,
            employee_user,
        )

    async def test_update_platform_as_manager_user_assoc_org_and_platform_update_title_already_exists(
        self, client, platform_db_session, manager_user
    ) -> None:
        a_organization = await create_random_organization(platform_db_session)
        a_platform = await get_platform_by_slug(
            platform_db_session, DUPLICATE_PLATFORM_SLUG
        )
        await assign_platform_to_organization(
            platform_db_session, a_organization.id, a_platform.id
        )
        data_in: dict[str, Any] = {}
        data_in["title"] = a_platform.title
        data_in["description"] = random_lower_string()
        response: Response = await client.patch(
            f"platforms/{a_platform.id}",
            headers=manager_user.token_headers,
            json=data_in,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]


class TestDeletePlatform:
    # AUTHORIZED CLIENTS
    async def test_delete_platform_as_admin_user(
        self, client, platform_db_session, admin_user
    ) -> None:
        await perform_test_delete(
            False, 200, None, client, platform_db_session, admin_user
        )

    async def test_delete_platform_as_manager_user_not_assoc_org(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_delete(
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            platform_db_session,
            manager_user,
        )

    async def test_delete_platform_as_manager_user_assoc_org(
        self, client, platform_db_session, manager_user
    ) -> None:
        await perform_test_delete(
            True,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            platform_db_session,
            manager_user,
        )

    async def test_delete_platform_as_employee_user_not_assoc_org(
        self, client, platform_db_session, unverified_user
    ) -> None:
        await perform_test_delete(
            False,
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            platform_db_session,
            unverified_user,
        )

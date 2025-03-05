from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import (
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_EXISTS,
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
)
from app.entities.core_organization.crud import OrganizationRepository
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_auth_id
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.anyio


DUPLICATE_URL = "/%s/%s/" % (random_lower_string(16), random_lower_string(16))


async def perform_test_list(
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    await create_random_organization(db_session)
    await create_random_organization(db_session)
    response: Response = await client.get(
        "organizations/", headers=current_user.token_headers
    )
    assert 200 <= response.status_code < 300
    data = response.json()
    assert data["page"] == 1
    assert data["total"] == item_count
    assert data["size"] == 1000
    assert len(data["results"]) == item_count


async def perform_test_list_public(
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    entry_1 = await create_random_organization(db_session)
    await create_random_organization(db_session, is_active=False)
    entry_3 = await create_random_organization(db_session)
    response: Response = await client.get(
        "organizations/public", headers=current_user.token_headers
    )
    assert 200 <= response.status_code < 300
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == item_count
    assert data["size"] == 1000
    assert len(data["results"]) == item_count
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry


async def perform_test_create(
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    slug: str = random_lower_string(8)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "organizations/",
        headers=current_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry["slug"] == slug
        assert entry["title"] == title
        assert entry["description"] == description
    else:
        assert error_msg in entry["detail"]


async def perform_test_create_error_exists(
    slug: str,
    title: str,
    description: str,
    exists_by: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data: dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "organizations/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: dict[str, Any] = response.json()
    assert entry["slug"] == slug
    assert entry["title"] == title
    assert entry["description"] == description
    data_2: dict[str, str]
    if exists_by == "title":
        slug_2: str = random_lower_string(8)
        description_2: str = random_lower_string()
        data_2: dict[str, str] = {
            "slug": slug_2,
            "title": title,
            "description": description_2,
        }
    if exists_by == "slug":
        title_2: str = random_lower_string()
        description_2: str = random_lower_string()
        data_2: dict[str, str] = {
            "slug": slug,
            "title": title_2,
            "description": description,
        }
    response_2: Response = await client.post(
        "organizations/",
        headers=admin_user.token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ERROR_MESSAGE_ORGANIZATION_EXISTS


async def perform_test_limits_create(
    slug: str,
    title: str,
    description: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data: dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "organizations/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == error_msg


async def perform_test_read(
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
    a_organization = await create_random_organization(db_session)
    await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    response: Response = await client.get(
        f"organizations/{a_organization.id}",
        headers=current_user.token_headers,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry["id"] == str(a_organization.id)
        repo = OrganizationRepository(db_session)
        existing_data = await repo.read_by("title", a_organization.title)
        assert existing_data
        assert existing_data.title == entry["title"]
    else:
        assert error_msg in entry["detail"]


async def perform_test_update(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    title: str = random_lower_string()
    data: dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"organizations/{a_organization.id}",
        headers=current_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry["id"] == str(a_organization.id)
        assert entry["title"] == title
        assert entry["description"] == a_organization.description
    else:
        assert error_msg in entry["detail"]


async def perform_test_limits_update(
    title: str | None,
    description: str | None,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    data: dict[str, str]
    if title is not None:
        data = {"title": title}
    if description is not None:
        data = {"description": description}
    if title is None and description is None:
        data = {"title": a_organization.title}
    response: Response = await client.patch(
        f"organizations/{a_organization.id}",
        headers=admin_user.token_headers,
        json=data,
    )
    if title is not None or description is not None:
        updated_entry: dict[str, Any] = response.json()
        assert response.status_code == 422
        assert updated_entry["detail"][0]["msg"] == error_msg
    else:
        assert response.status_code == 400
        updated_entry: dict[str, Any] = response.json()
        assert updated_entry["detail"] == error_msg


async def perform_test_delete(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    response: Response = await client.delete(
        f"organizations/{a_organization.id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None and entry is None:
        response: Response = await client.get(
            f"organizations/{a_organization.id}",
            headers=current_user.token_headers,
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_NOT_FOUND
    elif error_msg is None and entry is not None:
        assert entry["organization_id"] == str(a_organization.id)
    else:
        assert error_msg in entry["detail"]


class TestListOrganization:
    # AUTHORIZED CLIENTS
    async def test_list_all_organizations_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(2, client, db_session, admin_user)

    async def test_list_all_organizations_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list(4, client, db_session, manager_user)

    async def test_list_all_organizations_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(0, client, db_session, employee_user)

    async def test_list_public_organizations_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_public(8, client, db_session, admin_user)

    async def test_list_public_organizations_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list_public(10, client, db_session, manager_user)

    async def test_list_public_organizations_as_verified_user(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_list_public(12, client, db_session, verified_user)


class TestCreateOrganization:
    # AUTHORIZED CLIENTS
    async def test_create_organization_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(200, None, client, db_session, admin_user)

    async def test_create_organization_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_create(200, None, client, db_session, manager_user)

    async def test_create_organization_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            employee_user,
        )

    async def test_create_organization_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_create_organization_as_client_b_user(
        self, client, db_session, client_b_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_b_user,
        )

    async def test_create_organization_as_unverified_user(
        self, client, db_session, unverified_user
    ) -> None:
        await perform_test_create(
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            db_session,
            unverified_user,
        )

    # EXISTS
    async def test_create_organization_as_superuser_aleady_exists_by_title(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create_error_exists(
            random_lower_string(8),
            random_lower_string(),
            random_lower_string(),
            "title",
            client,
            db_session,
            admin_user,
        )

    async def test_create_organization_as_superuser_aleady_exists_by_slug(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create_error_exists(
            random_lower_string(8),
            random_lower_string(),
            random_lower_string(),
            "slug",
            client,
            db_session,
            admin_user,
        )

    # LIMITS
    async def test_create_organization_as_superuser_limits_slug_short(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(2),
            random_lower_string(),
            random_lower_string(),
            "Value error, slug must be 3 characters or more",
            client,
            db_session,
            admin_user,
        )

    async def test_create_organization_as_superuser_limits_slug_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(65),
            random_lower_string(),
            random_lower_string(),
            f"Value error, slug must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less",
            client,
            db_session,
            admin_user,
        )

    async def test_create_organization_as_superuser_limits_title_short(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(8),
            random_lower_string(4),
            random_lower_string(),
            "Value error, title must be 5 characters or more",
            client,
            db_session,
            admin_user,
        )

    async def test_create_organization_as_superuser_limits_title_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(8),
            random_lower_string() * 100,
            random_lower_string(),
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
            client,
            db_session,
            admin_user,
        )

    async def test_create_organization_as_superuser_limits_description_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            random_lower_string(8),
            random_lower_string(),
            random_lower_string() * 160,
            f"Value error, description must be {DB_STR_DESC_MAXLEN_INPUT} characters or less",
            client,
            db_session,
            admin_user,
        )


class TestReadOrganization:
    # AUTHORIZED CLIENTS
    async def test_read_organization_by_id_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_read(200, None, client, db_session, admin_user)

    async def test_read_organization_by_id_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(200, None, client, db_session, manager_user)

    async def test_read_organization_by_id_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_read(200, None, client, db_session, employee_user)

    async def test_read_organization_by_id_as_verified_user(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_read(
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            verified_user,
        )

    # CASES
    async def test_read_organization_by_id_as_superuser_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"organizations/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_NOT_FOUND


class TestUpdateOrganization:
    # AUTHORIZED CLIENTS
    async def test_update_organization_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_update(False, 200, None, client, db_session, admin_user)

    async def test_update_organization_as_admin_user_assoc_org(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, admin_user)

    async def test_update_organization_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_update(False, 200, None, client, db_session, manager_user)

    async def test_update_organization_as_manager_user_assoc_org(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, manager_user)

    async def test_update_organization_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_update(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            employee_user,
        )

    async def test_update_organization_as_employee_user_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, employee_user)

    async def test_update_organization_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_update(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_update_organization_as_client_a_user_assoc_org(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, client_a_user)

    async def test_update_organization_as_unverified_user(
        self, client, db_session, unverified_user
    ) -> None:
        await perform_test_update(
            False,
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            db_session,
            unverified_user,
        )

    async def test_update_organization_as_unverified_user_assoc_org(
        self, client, db_session, unverified_user
    ) -> None:
        await perform_test_update(
            True,
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            db_session,
            unverified_user,
        )

    # LIMITS
    async def test_update_organization_as_superuser_limits_title_short(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string(4),
            None,
            "Value error, title must be 5 characters or more",
            client,
            db_session,
            admin_user,
        )

    async def test_update_organization_as_superuser_limits_title_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            random_lower_string() * 100,
            None,
            "Value error, title must be {} characters or less".format(
                DB_STR_TINYTEXT_MAXLEN_INPUT
            ),
            client,
            db_session,
            admin_user,
        )

    async def test_update_organization_as_superuser_limits_description_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            None,
            random_lower_string() * 160,
            "Value error, description must be {} characters or less".format(
                DB_STR_DESC_MAXLEN_INPUT
            ),
            client,
            db_session,
            admin_user,
        )

    async def test_update_organization_as_superuser_limits_already_exists(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            None,
            None,
            ERROR_MESSAGE_ORGANIZATION_EXISTS,
            client,
            db_session,
            admin_user,
        )


class TestDeleteOrganization:
    # AUTHORIZED CLIENTS
    async def test_delete_organization_by_id_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_delete(False, 200, None, client, db_session, admin_user)

    async def test_delete_organization_by_id_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            manager_user,
        )

    async def test_delete_organization_by_id_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_delete_organization_by_id_as_client_a_user_assoc_org(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(True, 200, None, client, db_session, client_a_user)

    async def test_delete_organization_by_id_as_client_b_user_assoc_org(
        self, client, db_session, client_b_user
    ) -> None:
        await perform_test_delete(True, 200, None, client, db_session, client_b_user)

    # CASES
    async def test_delete_organization_by_id_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        bad_organization_id = get_uuid_str()
        response: Response = await client.delete(
            f"organizations/{bad_organization_id}",
            headers=admin_user.token_headers,
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert ERROR_MESSAGE_ORGANIZATION_NOT_FOUND in data["detail"]

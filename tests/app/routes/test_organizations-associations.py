from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
    ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND,
)
from app.entities.core_user.constants import ERROR_MESSAGE_USER_NOT_FOUND
from app.services.permission.constants import ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS
from app.utilities.uuids import get_uuid
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform
from tests.utils.users import create_random_user, get_user_by_auth_id
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.anyio


async def perform_test_assign_user(
    assign_random: bool,
    assign_bad_user_id: bool,
    assign_bad_org_id: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
    assign_user_id = this_user.id
    a_organization = await create_random_organization(db_session)
    assign_org_id = a_organization.id
    if assign_random:
        a_user = await create_random_user(db_session)
        assign_user_id = a_user.id
    if assign_bad_user_id:
        assign_user_id = get_uuid()
    if assign_bad_org_id:
        assign_org_id = get_uuid()
    a_user_organization = {
        "user_id": str(assign_user_id),
        "organization_id": str(assign_org_id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/user",
        headers=current_user.token_headers,
        json=a_user_organization,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None:
        assert entry["id"] is not None
        assert entry["user_id"] == str(assign_user_id)
        assert entry["organization_id"] == str(assign_org_id)
    else:
        assert error_msg in entry["detail"]


async def perform_test_remove_user(
    assign_random: bool,
    assign_bad_user_id: bool,
    assign_bad_org_id: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
    assign_user_id = this_user.id
    a_organization = await create_random_organization(db_session)
    assign_org_id = a_organization.id
    user_organization_rel = await assign_user_to_organization(
        db_session, this_user.id, a_organization.id
    )
    if assign_random:
        a_user = await create_random_user(db_session)
        user_organization_rel = await assign_user_to_organization(
            db_session, a_user.id, a_organization.id
        )
        assign_user_id = a_user.id
    if assign_bad_user_id:
        assign_user_id = get_uuid()
    if assign_bad_org_id:
        assign_org_id = get_uuid()
    user_organization_in = {
        "user_id": str(assign_user_id),
        "organization_id": str(assign_org_id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/remove/user",
        headers=current_user.token_headers,
        json=user_organization_in,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None:
        assert entry["id"] is not None
        assert entry["user_id"] == str(user_organization_rel.user_id)
        assert entry["organization_id"] == str(user_organization_rel.organization_id)
    else:
        assert error_msg in entry["detail"]


async def perform_test_assign_website(
    assign_bad_org_id: bool,
    assign_bad_site_id: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    assign_org_id = get_uuid() if assign_bad_org_id else a_organization.id
    assign_site_id = get_uuid() if assign_bad_site_id else a_website.id
    organization_website = {
        "organization_id": str(assign_org_id),
        "website_id": str(assign_site_id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/website",
        headers=current_user.token_headers,
        json=organization_website,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None:
        assert entry["id"] is not None
        assert entry["organization_id"] == str(assign_org_id)
        assert entry["website_id"] == str(assign_site_id)
    else:
        assert error_msg in entry["detail"]


async def perform_test_remove_website(
    assign_bad_org_id: bool,
    assign_bad_site_id: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    assign_org_id = get_uuid() if assign_bad_org_id else a_organization.id
    assign_site_id = get_uuid() if assign_bad_site_id else a_website.id
    organization_website = {
        "organization_id": str(assign_org_id),
        "website_id": str(assign_site_id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/remove/website",
        headers=current_user.token_headers,
        json=organization_website,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None:
        assert entry["id"] is not None
        assert entry["organization_id"] == str(assign_org_id)
        assert entry["website_id"] == str(assign_site_id)
    else:
        assert error_msg in entry["detail"]


async def perform_test_assign_platform(
    assign_bad_org_id: bool,
    assign_bad_platform_id: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    assign_org_id = get_uuid() if assign_bad_org_id else a_organization.id
    assign_platform_id = get_uuid() if assign_bad_platform_id else a_platform.id
    organization_platform = {
        "organization_id": str(assign_org_id),
        "platform_id": str(assign_platform_id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/platform",
        headers=current_user.token_headers,
        json=organization_platform,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None:
        assert entry["id"] is not None
        assert entry["organization_id"] == str(assign_org_id)
        assert entry["platform_id"] == str(assign_platform_id)
    else:
        assert error_msg in entry["detail"]


async def perform_test_remove_platform(
    assign_bad_org_id: bool,
    assign_bad_platform_id: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    assign_org_id = get_uuid() if assign_bad_org_id else a_organization.id
    assign_platform_id = get_uuid() if assign_bad_platform_id else a_platform.id
    organization_platform = {
        "organization_id": str(assign_org_id),
        "platform_id": str(assign_platform_id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/remove/platform",
        headers=current_user.token_headers,
        json=organization_platform,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is None:
        assert entry["id"] is not None
        assert entry["organization_id"] == str(assign_org_id)
        assert entry["platform_id"] == str(assign_platform_id)
    else:
        assert error_msg in entry["detail"]


class TestOrganizationAssociateUsers:
    # ASSIGN
    async def test_organization_assign_random_user_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_user(
            True, False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_assign_random_user_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_user(
            True, False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_assign_random_user_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_assign_user(
            True,
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_assign_user_as_admin_user_assoc_org(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_user(
            False, False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_assign_user_as_manager_user_assoc_org(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_user(
            False, False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_assign_user_as_employee_user_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_assign_user(
            False,
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_assign_user_as_admin_user_user_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_user(
            False,
            True,
            False,
            404,
            ERROR_MESSAGE_USER_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_assign_user_as_admin_user_org_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_user(
            False,
            False,
            True,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    # REMOVE
    async def test_organization_remove_random_user_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_user(
            True, False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_remove_random_user_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_user(
            True, False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_remove_random_user_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_remove_user(
            True,
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_remove_user_as_admin_user_assoc_org(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_user(
            False, False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_remove_user_as_manager_user_assoc_org(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_user(
            False, False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_remove_user_as_employee_user_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_remove_user(
            False,
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_remove_user_as_admin_user_user_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_user(
            False,
            True,
            False,
            404,
            ERROR_MESSAGE_USER_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_remove_user_as_admin_user_org_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_user(
            False,
            False,
            True,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    # CASES
    async def test_organization_remove_user_as_superuser_relation_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_user = await create_random_user(db_session)
        a_organization = await create_random_organization(db_session)
        user_organization_in = {
            "user_id": str(a_user.id),
            "organization_id": str(a_organization.id),
        }
        response: Response = await client.post(
            f"organizations/{a_organization.id}/remove/user",
            headers=admin_user.token_headers,
            json=user_organization_in,
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND


class TestOrganizationAssociateWebsites:
    # ASSIGN
    async def test_organization_assign_random_website_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_website(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_assign_random_website_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_website(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_assign_random_website_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_assign_website(
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_assign_random_website_as_admin_user_website_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_website(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_assign_random_website_as_manager_user_website_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_website(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    async def test_organization_assign_random_website_as_employee_user_website_not_found(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_assign_website(
            True,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_assign_random_website_as_admin_user_org_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_website(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_assign_random_website_as_manager_user_org_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_website(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    # REMOVE
    async def test_organization_remove_random_website_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_website(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_remove_random_website_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_website(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_remove_random_website_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_remove_website(
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_remove_random_website_as_admin_user_website_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_website(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_remove_random_website_as_manager_user_website_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_website(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    async def test_organization_remove_random_website_as_employee_user_website_not_found(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_remove_website(
            True,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_remove_random_website_as_admin_user_org_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_website(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_remove_random_website_as_manager_user_org_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_website(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    # CASES
    async def test_organization_remove_website_as_superuser_relation_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_website = await create_random_website(db_session)
        a_organization = await create_random_organization(db_session)
        organization_website = {
            "organization_id": str(a_organization.id),
            "website_id": str(a_website.id),
        }
        response: Response = await client.post(
            f"organizations/{a_organization.id}/remove/website",
            headers=admin_user.token_headers,
            json=organization_website,
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND


class TestOrganizationAssociatePlatforms:
    # ASSIGN
    async def test_organization_assign_random_platform_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_platform(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_assign_random_platform_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_platform(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_assign_random_platform_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_assign_platform(
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_assign_random_platform_as_admin_user_platform_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_platform(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_assign_random_platform_as_manager_user_platform_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_platform(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    async def test_organization_assign_random_platform_as_employee_user_platform_not_found(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_assign_platform(
            True,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_assign_random_platform_as_admin_user_org_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_assign_platform(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_assign_random_platform_as_manager_user_org_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_assign_platform(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    # REMOVE
    async def test_organization_remove_random_platform_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_platform(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_organization_remove_random_platform_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_platform(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_organization_remove_random_platform_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_remove_platform(
            False,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_remove_random_platform_as_admin_user_platform_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_platform(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_remove_random_platform_as_manager_user_platform_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_platform(
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    async def test_organization_remove_random_platform_as_employee_user_platform_not_found(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_remove_platform(
            True,
            False,
            403,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
            client,
            db_session,
            employee_user,
        )

    async def test_organization_remove_random_platform_as_admin_user_org_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_remove_platform(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_organization_remove_random_platform_as_manager_user_org_not_found(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_remove_platform(
            True,
            False,
            404,
            ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
            client,
            db_session,
            manager_user,
        )

    # CASES
    async def test_organization_remove_platform_as_superuser_relation_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_platform = await create_random_platform(db_session)
        a_organization = await create_random_organization(db_session)
        organization_platform = {
            "organization_id": str(a_organization.id),
            "platform_id": str(a_platform.id),
        }
        response: Response = await client.post(
            f"organizations/{a_organization.id}/remove/platform",
            headers=admin_user.token_headers,
            json=organization_platform,
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND

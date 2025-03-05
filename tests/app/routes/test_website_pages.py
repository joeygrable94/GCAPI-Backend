from typing import Any

import pytest
from httpx import AsyncClient, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
)
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid, get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.anyio


DUPLICATE_URL = "/%s/%s/" % (random_lower_string(16), random_lower_string(16))


async def perform_test_list(
    user_count: int,
    query_website: bool,
    query_inactive: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_email(db_session, current_user.email)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    c_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session, is_secure=True)
    b_website = await create_random_website(db_session, is_secure=False)
    c_website = await create_random_website(db_session, is_secure=True)
    d_website = await create_random_website(db_session, is_secure=True)
    if assign_user:
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    await assign_website_to_organization(db_session, a_website.id, b_organization.id)
    await assign_website_to_organization(db_session, b_website.id, a_organization.id)
    await assign_website_to_organization(db_session, b_website.id, b_organization.id)
    await assign_website_to_organization(db_session, c_website.id, c_organization.id)
    await create_random_website_page(db_session, a_website.id)
    await create_random_website_page(db_session, a_website.id)
    await create_random_website_page(db_session, a_website.id)
    await create_random_website_page(db_session, b_website.id)
    await create_random_website_page(db_session, c_website.id)
    await create_random_website_page(db_session, d_website.id)
    await create_random_website_page(db_session, d_website.id, is_active=False)
    query_params: dict[str, Any] | None = None
    if query_website:
        query_params = {}
        query_params["website_id"] = str(a_website.id)
    if query_inactive:
        query_params = {} if query_params is None else query_params
        query_params["is_active"] = False
    response: Response = await client.get(
        "webpages/",
        headers=current_user.token_headers,
        params=query_params,
    )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == user_count
    assert data["size"] == 1000
    assert len(data["results"]) == user_count


async def perform_test_create(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_website_to_organization(
            db_session, a_website.id, a_organization.id
        )
    data = {
        "url": "/",
        "status": 200,
        "priority": 0.5,
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=current_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry["url"] == "/"
        assert entry["status"] == 200
        assert entry["priority"] == 0.5
        assert entry["website_id"] == str(a_website.id)
    else:
        assert error_msg in entry["detail"]


async def perform_test_limits_create(
    url: str,
    status: int,
    priority: float,
    fake_website: bool,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    await create_random_website_page(db_session, a_website.id, path=DUPLICATE_URL)
    data = {
        "url": url,
        "status": status,
        "priority": priority,
    }
    if fake_website:
        data["website_id"] = get_uuid_str()
    else:
        data["website_id"] = str(a_website.id)
    response: Response = await client.post(
        "webpages/",
        headers=admin_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]


async def perform_test_read(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    a_entry = await create_random_website_page(db_session, a_website.id)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_website_to_organization(
            db_session, a_website.id, a_organization.id
        )
    response: Response = await client.get(
        f"webpages/{a_entry.id}",
        headers=current_user.token_headers,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry["url"] == a_entry.url
        assert entry["status"] == a_entry.status
        assert entry["priority"] == a_entry.priority
        assert entry["website_id"] == str(a_entry.website_id)
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
    a_website = await create_random_website(db_session)
    a_webpage = await create_random_website_page(db_session, a_website.id)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_website_to_organization(
            db_session, a_website.id, a_organization.id
        )
    update_dict = {"is_active": not a_webpage.is_active}
    response: Response = await client.patch(
        f"webpages/{a_webpage.id}",
        headers=current_user.token_headers,
        json=update_dict,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry["id"] == str(a_webpage.id)
        assert entry["url"] == a_webpage.url
        assert entry["is_active"] is not a_webpage.is_active
    else:
        assert error_msg in entry["detail"]


async def perform_test_limits_update(
    url: str,
    status: int,
    priority: float,
    fake_website: bool,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    a_webpage = await create_random_website_page(
        db_session, a_website.id, path=DUPLICATE_URL
    )
    data = {
        "url": url,
        "status": status,
        "priority": priority,
    }
    if fake_website:
        data["website_id"] = get_uuid_str()
    else:
        data["website_id"] = str(a_website.id)
    response: Response = await client.patch(
        f"webpages/{a_webpage.id}",
        headers=admin_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]


async def perform_test_delete(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    a_entry = await create_random_website_page(db_session, a_website.id)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_website_to_organization(
            db_session, a_website.id, a_organization.id
        )
    response: Response = await client.delete(
        f"webpages/{a_entry.id}",
        headers=current_user.token_headers,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert entry is None
        response: Response = await client.get(
            f"webpages/{a_entry.id}",
            headers=current_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
    else:
        assert error_msg in entry["detail"]


class TestListWebsitePage:
    # AUTHORIZED CLIENTS
    async def test_list_all_websites_as_admin_user_list_all_website_pages(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(7, False, False, False, client, db_session, admin_user)

    async def test_list_all_websites_as_admin_user_list_all_website_pages_by_website(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(3, True, False, False, client, db_session, admin_user)

    async def test_list_all_websites_as_admin_user_list_all_website_pages_by_not_active(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(3, False, True, False, client, db_session, admin_user)

    async def test_list_all_websites_as_employee_user_do_not_list_unassigned_website_pages(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(
            0, False, False, False, client, db_session, employee_user
        )

    async def test_list_all_websites_as_employee_user_list_assigned_website_pages(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(
            1, False, False, True, client, db_session, employee_user
        )

    async def test_list_all_websites_as_client_user_list_assigned_website_pages(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_list(
            1, False, False, True, client, db_session, client_a_user
        )


class TestCreateWebsitePage:
    # AUTHORIZED CLIENTS
    async def test_create_website_page_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(True, 200, None, client, db_session, admin_user)

    async def test_create_website_page_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_create(True, 200, None, client, db_session, manager_user)

    async def test_create_website_page_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_create(True, 200, None, client, db_session, employee_user)

    async def test_create_website_page_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_create(True, 200, None, client, db_session, client_a_user)

    async def test_create_website_page_as_client_b_user(
        self, client, db_session, client_b_user
    ) -> None:
        await perform_test_create(True, 200, None, client, db_session, client_b_user)

    async def test_create_website_page_as_verified_user(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_create(True, 200, None, client, db_session, verified_user)

    async def test_create_website_page_as_unverified_user_not_assoc_org(
        self, client, db_session, unverified_user
    ) -> None:
        await perform_test_create(
            False,
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            db_session,
            unverified_user,
        )

    # LIMITS
    async def test_create_website_page_as_superuser_website_limits_valid_url(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            "/" + random_lower_string(),
            200,
            0.5,
            False,
            200,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_page_as_superuser_website_limits_duplicate_url(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            DUPLICATE_URL,
            200,
            0.5,
            False,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_page_as_superuser_website_limits_url_required(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            "",
            200,
            0.5,
            False,
            422,
            "detail",
            "Value error, url is required",
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_page_as_superuser_website_limits_url_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            "/" + "a" * DB_STR_URLPATH_MAXLEN_INPUT,
            200,
            0.5,
            False,
            422,
            "detail",
            f"Value error, url must be {DB_STR_URLPATH_MAXLEN_INPUT} characters or less",
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_page_as_superuser_website_limits_fake_website(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            "/" + random_lower_string(),
            200,
            0.5,
            True,
            404,
            "message",
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )


class TestReadWebsitePage:
    # AUTHORIZED CLIENTS
    async def test_read_website_page_by_id_as_admin_user_read_any_website_page(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_read(False, 200, None, client, db_session, admin_user)

    async def test_read_website_page_by_id_as_manager_user_read_assiged_website_page(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(True, 200, None, client, db_session, manager_user)

    async def test_read_website_page_by_id_as_employee_user_read_assigned_website_page(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_read(True, 200, None, client, db_session, employee_user)

    async def test_read_website_page_by_id_as_manager_user_cannot_read_unassigned_website_page(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_read(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_read_website_page_by_id_as_employee_user_cannot_read_unassigned_website_page(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_read(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            employee_user,
        )

    # CASES
    async def test_read_website_page_by_id_as_superuser_page_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"webpages/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestUpdateWebsitePage:
    # AUTHORIZED CLIENTS
    async def test_update_website_page_as_admin_update_website_page(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_update(False, 200, None, client, db_session, admin_user)

    async def test_update_website_page_as_manager_update_website_page(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_update(False, 200, None, client, db_session, manager_user)

    async def test_update_website_page_as_employee_update_website_page_assigned_to_associated_client(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, employee_user)

    async def test_update_website_page_as_employee_not_allowed_to_update_unassigned_website_page(
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

    async def test_update_website_page_as_client_not_allowed_to_update_unassigned_website_page(
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

    async def test_update_website_page_as_unverified_user_not_allowed_to_update_any_website_page(
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

    # LIMITS
    async def test_update_website_page_as_superuser_limits_success(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            "/" + random_lower_string(),
            200,
            0.5,
            False,
            200,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_page_as_superuser_limits_duplicate_url(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            DUPLICATE_URL,
            200,
            0.5,
            False,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_page_as_superuser_limits_url_required(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            "",
            200,
            0.5,
            False,
            422,
            "detail",
            "Value error, url must be 1 characters or more",
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_page_as_superuser_limits_url_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            "/" + "a" * DB_STR_URLPATH_MAXLEN_INPUT,
            200,
            0.5,
            False,
            422,
            "detail",
            f"Value error, url must be {DB_STR_URLPATH_MAXLEN_INPUT} characters or less",
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_page_as_superuser_limits_website_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            "/" + random_lower_string(),
            200,
            0.5,
            True,
            404,
            "message",
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )


class TestDeleteWebsitePage:
    # AUTHORIZED CLIENTS
    async def test_delete_website_page_by_id_as_admin_user_delete_any_website_page(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_delete(False, 200, None, client, db_session, admin_user)

    async def test_delete_website_page_by_id_as_manager_user_delete_assiged_website_page(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(True, 200, None, client, db_session, manager_user)

    async def test_delete_website_page_by_id_as_employee_user_delete_assigned_website_page(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_delete(True, 200, None, client, db_session, employee_user)

    async def test_delete_website_page_by_id_as_client_a_user_delete_assigned_website_page(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(True, 200, None, client, db_session, client_a_user)

    async def test_delete_website_page_by_id_as_manager_user_fails_on_delete_unassigned_website_page(
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

    async def test_delete_website_page_by_id_as_employee_user_fails_on_delete_unassigned_website_page(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_delete(
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            employee_user,
        )


class TestFetchWebsitePageSpeedInsightsById:
    # AUTHORIZED CLIENTS
    async def test_fetch_website_page_speed_insights_by_id_as_superuser(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry = await create_random_website_page(db_session)
        response: Response = await client.post(
            f"webpages/{entry.id}/process-psi", headers=admin_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 200
        assert data["id"] == str(entry.id)
        assert data["is_active"] == entry.is_active
        assert data["url"] == entry.url
        assert data["status"] == entry.status
        assert data["priority"] == entry.priority
        assert data["website_id"] == str(entry.website_id)

    async def test_fetch_website_page_psi_by_id_as_superuser_website_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        web_fake_id: UUID4 = get_uuid()
        entry = await create_random_website_page(
            db_session,
            website_id=web_fake_id,
        )
        response: Response = await client.post(
            f"webpages/{entry.id}/process-psi", headers=admin_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

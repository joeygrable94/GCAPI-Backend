import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
)
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.website.constants import ERROR_MESSAGE_DOMAIN_INVALID
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_auth_id
from tests.utils.utils import random_boolean, random_domain, random_lower_string
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.anyio


async def perform_test_list(
    user_count: int,
    query_client: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    c_organization = await create_random_organization(db_session)
    website_a = await create_random_website(db_session, is_secure=True)
    website_b = await create_random_website(db_session, is_secure=False)
    website_c = await create_random_website(db_session, is_secure=True)
    if not this_user.is_superuser and assign_user:
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    await assign_website_to_organization(db_session, website_a.id, b_organization.id)
    await assign_website_to_organization(db_session, website_b.id, a_organization.id)
    await assign_website_to_organization(db_session, website_b.id, b_organization.id)
    await assign_website_to_organization(db_session, website_c.id, c_organization.id)
    if query_client:
        response: Response = await client.get(
            "websites/",
            params={"organization_id": str(b_organization.id)},
            headers=current_user.token_headers,
        )
    else:
        response: Response = await client.get(
            "websites/", headers=current_user.token_headers
        )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == user_count
    assert data["size"] == 1000
    assert len(data["results"]) == user_count


async def perform_test_create(
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    domain: str = random_domain(16, "com")
    is_secure: bool = random_boolean()
    data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    with unittest.mock.patch(
        "app.entities.website.crud.WebsiteRepository.validate"
    ) as mock_validate_website_domain:
        mock_validate_website_domain.return_value = True
        response: Response = await client.post(
            "websites/",
            headers=current_user.token_headers,
            json=data,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == status_code
        if error_msg is not None:
            assert error_msg in entry["detail"]
        else:
            assert entry["domain"] == domain
            assert entry["is_secure"] == is_secure


async def perform_test_limits_create(
    check_domain: bool,
    domain: str,
    is_secure: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    valid_domain: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response
    if check_domain:
        response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=data,
        )
    else:
        with unittest.mock.patch(
            "app.entities.website.crud.WebsiteRepository.validate"
        ) as mock_validate_website_domain:
            mock_validate_website_domain.return_value = valid_domain
            response = await client.post(
                "websites/",
                headers=admin_user.token_headers,
                json=data,
            )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]


async def perform_test_read(
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
    if this_user.is_superuser:
        a_website = await create_random_website(db_session)
    else:
        a_website = await create_random_website(db_session)
        a_organization = await create_random_organization(db_session)
        await assign_website_to_organization(
            db_session, a_website.id, a_organization.id
        )
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    response: Response = await client.get(
        f"websites/{a_website.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(a_website.id)


async def perform_test_update(
    assign_organization: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    update_dict = {"is_secure": not a_website.is_secure}
    response: Response = await client.patch(
        f"websites/{a_website.id}",
        headers=current_user.token_headers,
        json=update_dict,
    )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_msg is not None:
        assert error_msg in entry["detail"]
    else:
        assert entry["id"] == str(a_website.id)
        assert entry["domain"] == a_website.domain
        assert entry["is_secure"] is not a_website.is_secure


async def perform_test_limits_update(
    check_domain: bool,
    domain: str | None,
    status_code: int,
    error_type: str,
    error_msg: str,
    valid_domain: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    update_dict: dict[str, Any] = {"is_secure": not a_website.is_secure}
    if domain is None:
        update_dict = {"domain": a_website.domain, "is_secure": not a_website.is_secure}
    else:
        update_dict = {"domain": domain, "is_secure": not a_website.is_secure}
    response: Response
    if check_domain:
        response: Response = await client.patch(
            f"websites/{a_website.id}",
            headers=admin_user.token_headers,
            json=update_dict,
        )
    else:
        with unittest.mock.patch(
            "app.entities.website.crud.WebsiteRepository.validate"
        ) as mock_validate_website_domain:
            mock_validate_website_domain.return_value = valid_domain
            response: Response = await client.patch(
                f"websites/{a_website.id}",
                headers=admin_user.token_headers,
                json=update_dict,
            )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]


async def perform_test_delete(
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    entry = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{entry.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is not None:
        assert error_msg in data["detail"]
    else:
        response: Response = await client.get(
            f"websites/{entry.id}",
            headers=current_user.token_headers,
        )
        assert response.status_code == 404


class TestListWebsite:
    # AUTHORIZED CLIENTS
    async def test_list_all_websites_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(3, False, False, client, db_session, admin_user)

    async def test_list_all_websites_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list(6, False, False, client, db_session, manager_user)

    async def test_list_all_websites_as_employee_user_not_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(0, False, False, client, db_session, employee_user)

    async def test_list_all_websites_as_employee_user_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(1, False, True, client, db_session, employee_user)

    async def test_list_all_websites_as_admin_user_query_client(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(2, True, False, client, db_session, admin_user)

    async def test_list_all_websites_as_manager_user_query_client(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list(2, True, False, client, db_session, manager_user)


class TestCreateWebsite:
    # AUTHORIZED CLIENTS
    async def test_create_website_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(200, None, client, db_session, admin_user)

    async def test_create_website_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_create(200, None, client, db_session, manager_user)

    async def test_create_website_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            employee_user,
        )

    async def test_create_website_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_create(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_create_website_as_unverified_user(
        self, client, db_session, unverified_user
    ) -> None:
        await perform_test_create(
            403,
            ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
            client,
            db_session,
            unverified_user,
        )

    # LIMITS
    async def test_create_website_as_admin_user_website_limits_domain_invalid(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            True,
            random_domain(16, "co"),
            random_boolean(),
            422,
            "message",
            ERROR_MESSAGE_DOMAIN_INVALID,
            True,
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_as_admin_user_website_limits_domain_short(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            False,
            random_domain(1, "co"),
            random_boolean(),
            422,
            "detail",
            "Value error, domain must be 5 characters or more",
            False,
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_as_admin_user_website_limits_domain_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            False,
            random_domain(DB_STR_TINYTEXT_MAXLEN_INPUT + 1, "com"),
            random_boolean(),
            422,
            "detail",
            "Value error, domain must be {} characters or less".format(
                DB_STR_TINYTEXT_MAXLEN_INPUT
            ),
            False,
            client,
            db_session,
            admin_user,
        )

    async def test_create_website_as_admin_user_website_limits_domain_schema_invalid(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_create(
            False,
            "https://" + random_domain(3, "pub"),
            random_boolean(),
            422,
            "detail",
            "Value error, invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)",
            False,
            client,
            db_session,
            admin_user,
        )

    # CASES
    async def test_create_website_as_superuser_website_already_exists(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        domain: str = random_domain(16, "com")
        is_secure: bool = random_boolean()
        data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
        with unittest.mock.patch(
            "app.entities.website.crud.WebsiteRepository.validate"
        ) as mock_validate_website_domain:
            mock_validate_website_domain.return_value = True
            response: Response = await client.post(
                "websites/",
                headers=admin_user.token_headers,
                json=data,
            )
            assert 200 <= response.status_code < 300
            entry: dict[str, Any] = response.json()
            assert entry["domain"] == domain
            assert entry["is_secure"] == is_secure
        is_secure_2: bool = random_boolean()
        data_2: dict[str, Any] = {"domain": domain, "is_secure": is_secure_2}
        response_2: Response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=data_2,
        )
        assert response_2.status_code == 400
        entry_2: dict[str, Any] = response_2.json()
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry_2["detail"]

    async def test_create_website_as_superuser_website_domain_invalid(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        domain: str = random_domain(16, "com")
        is_secure: bool = random_boolean()
        data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
        response: Response
        response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=data,
        )
        assert response.status_code == 422
        entry: dict[str, Any] = response.json()
        assert entry["detail"] == ERROR_MESSAGE_DOMAIN_INVALID


class TestReadWebsite:
    # AUTHORIZED CLIENTS
    async def test_read_website_by_id_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_read(client, db_session, admin_user)

    async def test_read_website_by_id_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(client, db_session, manager_user)

    async def test_read_website_by_id_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_read(client, db_session, employee_user)

    async def test_read_website_by_id_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_read(client, db_session, client_a_user)

    async def test_read_website_by_id_as_client_b_user(
        self, client, db_session, client_b_user
    ) -> None:
        await perform_test_read(client, db_session, client_b_user)

    # CASES
    async def test_read_website_by_id_as_superuser_website_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"websites/{entry_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestUpdateWebsite:
    # AUTHORIZED CLIENTS
    async def test_update_website_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_update(False, 200, None, client, db_session, admin_user)

    async def test_update_website_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_update(False, 200, None, client, db_session, manager_user)

    async def test_update_website_as_employee_user_assoc_with_organization(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, employee_user)

    async def test_update_website_as_client_a_user_assoc_with_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_update(True, 200, None, client, db_session, client_a_user)

    async def test_update_website_as_employee_user_not_assoc_with_organization(
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

    async def test_update_website_as_client_a_user_not_assoc_with_organization(
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

    async def test_update_website_as_unverified_user(
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
    async def test_update_website_as_superuser_website_limits_domain_exists(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            False,
            None,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            False,
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_as_superuser_website_limits_domain_invalid(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            True,
            random_domain(16, "co"),
            422,
            "message",
            ERROR_MESSAGE_DOMAIN_INVALID,
            True,
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_as_superuser_website_limits_domain_short(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            False,
            "a.co",
            422,
            "detail",
            "Value error, domain must be 5 characters or more",
            False,
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_as_superuser_website_limits_domain_long(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            False,
            random_lower_string() * 10 + ".com",
            422,
            "detail",
            "Value error, domain must be {} characters or less".format(
                DB_STR_TINYTEXT_MAXLEN_INPUT
            ),
            False,
            client,
            db_session,
            admin_user,
        )

    async def test_update_website_as_superuser_website_limits_domain_invalid_schema(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_limits_update(
            False,
            "https://" + random_lower_string() + ".com",
            422,
            "detail",
            "Value error, invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)",
            False,
            client,
            db_session,
            admin_user,
        )

    # CASES
    async def test_update_website_as_superuser_website_domain_invalid(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_website = await create_random_website(db_session)
        domain: str = random_domain(16, "com")
        update_dict: dict[str, Any] = {
            "domain": domain,
            "is_secure": not a_website.is_secure,
        }
        response: Response
        response: Response = await client.patch(
            f"websites/{a_website.id}",
            headers=admin_user.token_headers,
            json=update_dict,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == 422
        assert entry["detail"] == ERROR_MESSAGE_DOMAIN_INVALID


class TestDeleteWebsite:
    # AUTHORIZED CLIENTS
    async def test_delete_website_by_id_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_delete(200, None, client, db_session, admin_user)

    async def test_delete_website_by_id_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(200, None, client, db_session, manager_user)

    async def test_delete_website_by_id_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    # CASES
    async def test_delete_website_as_admin_user_by_id_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        bad_website_id = get_uuid_str()
        response: Response = await client.delete(
            f"websites/{bad_website_id}",
            headers=admin_user.token_headers,
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

    async def test_delete_website_as_manager_user_by_id_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        bad_website_id = get_uuid_str()
        response: Response = await client.delete(
            f"websites/{bad_website_id}",
            headers=manager_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

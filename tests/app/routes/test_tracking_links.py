from typing import Any

from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_EXISTS
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
)
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.tracking_link import (
    create_random_tracking_link,
    create_random_tracking_link_url,
)
from tests.utils.users import get_user_by_auth_id
from tests.utils.utils import random_lower_string


async def perform_test_list(
    link_count: int,
    query_client: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, b_organization.id)
    if not this_user.is_superuser and assign_user:
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    if query_client:
        response: Response = await client.get(
            "utmlinks/",
            params={"organization_id": str(b_organization.id)},
            headers=current_user.token_headers,
        )
    else:
        response: Response = await client.get(
            "utmlinks/", headers=current_user.token_headers
        )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == link_count
    assert data["size"] == 1000
    assert len(data["results"]) == link_count


async def perform_test_list_query(
    link_count: int,
    q_client: bool | None,
    q_scheme: str | None,
    q_domain: str | None,
    q_destination: str | None,
    q_url_path: str | None,
    q_campaign: str | None,
    q_medium: str | None,
    q_source: str | None,
    q_content: str | None,
    q_term: str | None,
    q_active: bool | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    await create_random_tracking_link(
        db_session,
        b_organization.id,
    )
    await create_random_tracking_link(
        db_session,
        b_organization.id,
    )
    await create_random_tracking_link(db_session, a_organization.id, scheme="http")
    await create_random_tracking_link(db_session, a_organization.id, scheme="https")
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", domain="example.com"
    )
    await create_random_tracking_link(
        db_session,
        a_organization.id,
        scheme="https",
        domain="another.com",
        path="/destination",
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", path="/example-path"
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", utm_campaign="campaign-name"
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", utm_medium="medium-name"
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", utm_source="source-name"
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", utm_content="content-name"
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", utm_term="term-name"
    )
    await create_random_tracking_link(
        db_session, a_organization.id, scheme="https", is_active=False
    )
    query_params = {}
    if q_client:
        query_params["organization_id"] = str(b_organization.id)
    if q_scheme:
        query_params["scheme"] = q_scheme
    if q_domain:
        query_params["domain"] = q_domain
    if q_destination:
        query_params["destination"] = q_destination
    if q_url_path:
        query_params["url_path"] = q_url_path
    if q_campaign:
        query_params["utm_campaign"] = q_campaign
    if q_medium:
        query_params["utm_medium"] = q_medium
    if q_source:
        query_params["utm_source"] = q_source
    if q_content:
        query_params["utm_content"] = q_content
    if q_term:
        query_params["utm_term"] = q_term
    if q_active:
        query_params["is_active"] = False
    response: Response = await client.get(
        "utmlinks/",
        params=query_params,
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == link_count
    assert data["size"] == 1000
    assert len(data["results"]) == link_count


async def perform_test_create(
    assign_organization: bool,
    assign_wrong_client: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, b_organization.id)
    a_url = await create_random_tracking_link_url()
    data_in = {
        "url": a_url,
        "is_active": True,
    }
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        assert this_user is not None
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        if assign_wrong_client:
            data_in["organization_id"] = str(b_organization.id)
        else:
            data_in["organization_id"] = str(a_organization.id)
    response: Response = await client.post(
        "utmlinks/",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert all(item in entry.items() for item in data_in.items())
    else:
        assert entry["detail"] == error_msg


async def perform_test_read(
    assign_organization: bool,
    assign_wrong_client: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    await create_random_tracking_link(db_session, a_organization.id)
    a_link = await create_random_tracking_link(db_session, a_organization.id)
    b_link = await create_random_tracking_link(db_session, b_organization.id)
    ready_id = a_link.id
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        if assign_wrong_client:
            ready_id = b_link.id
    response: Response = await client.get(
        f"utmlinks/{ready_id}",
        headers=current_user.token_headers,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        if not assign_wrong_client:
            assert entry["id"] == str(a_link.id)
        else:
            entry["id"] == str(b_link.id)
    else:
        assert entry["detail"] == error_msg


async def perform_test_update(
    assign_organization: bool,
    assign_wrong_client: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_link = await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, b_organization.id)
    a_url = await create_random_tracking_link_url()
    data_in = {
        "url": a_url,
        "is_active": True,
    }
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        if assign_wrong_client:
            data_in["organization_id"] = str(b_organization.id)
        else:
            data_in["organization_id"] = str(a_organization.id)
    response: Response = await client.patch(
        f"utmlinks/{a_link.id}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is None:
        assert all(item in entry.items() for item in data_in.items())
    else:
        assert entry["detail"] == error_msg


async def perform_test_delete(
    assign_organization: bool,
    assign_wrong_client: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    await create_random_tracking_link(db_session, a_organization.id)
    a_link = await create_random_tracking_link(db_session, a_organization.id)
    b_link = await create_random_tracking_link(db_session, b_organization.id)
    delete_link_id = a_link.id
    if assign_organization:
        this_user = await get_user_by_auth_id(db_session, current_user.auth_id)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        if assign_wrong_client:
            delete_link_id = b_link.id
    response: Response = await client.delete(
        f"utmlinks/{delete_link_id}",
        headers=current_user.token_headers,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is not None:
        assert entry["detail"] == error_msg


class TestListTrackingLinks:
    # AUTHORIZED CLIENTS
    async def test_list_all_tracking_link_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(2, False, False, client, db_session, admin_user)

    async def test_list_all_tracking_link_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list(4, False, False, client, db_session, manager_user)

    async def test_list_all_tracking_link_as_employee_user_not_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(0, False, False, client, db_session, employee_user)

    async def test_list_all_tracking_link_as_employee_user_assoc_org(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_list(1, False, True, client, db_session, employee_user)

    async def test_list_all_tracking_link_as_admin_user_query_org(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(1, True, False, client, db_session, admin_user)

    async def test_list_all_tracking_link_as_manager_user_query_org(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list(1, True, False, client, db_session, manager_user)

    # CASES
    async def test_list_all_tracking_links_as_admin_user_query_utm(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            25,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_organization_id(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            2,
            True,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_scheme_http(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            3,
            None,
            "http",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_scheme_https(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            60,
            None,
            "https",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_domain(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            5,
            None,
            None,
            "example.com",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_destination(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            6,
            None,
            None,
            None,
            "https://another.com/destination",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_url_path(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            7,
            None,
            None,
            None,
            None,
            "/example-path",
            None,
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_utm_campaign(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            8,
            None,
            None,
            None,
            None,
            None,
            "campaign-name",
            None,
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_utm_medium(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            9,
            None,
            None,
            None,
            None,
            None,
            None,
            "medium-name",
            None,
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_utm_source(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            10,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "source-name",
            None,
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_utm_content(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            11,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "content-name",
            None,
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_utm_term(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            12,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "term-name",
            None,
            client,
            db_session,
            admin_user,
        )

    async def test_list_all_tracking_links_as_admin_user_query_utm_by_is_active(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list_query(
            13,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            True,
            client,
            db_session,
            admin_user,
        )


class TestCreateTrackingLinks:
    # AUTHORIZED CLIENTS
    async def test_create_tracking_link_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_create_tracking_link_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_create(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_create_tracking_link_as_client_a_user_not_assoc_org(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_create(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_create_tracking_link_as_client_a_user_assoc_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_create(
            True, False, 200, None, client, db_session, client_a_user
        )

    async def test_create_tracking_link_as_client_a_user_assoc_wrong_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_create(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_create_tracking_link_as_employee_user_assoc_organization(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_create(
            True, False, 200, None, client, db_session, employee_user
        )

    async def test_create_tracking_link_as_verified_user_not_assoc_org(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_create(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

    async def test_create_tracking_link_as_verified_user_assoc_organization(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_create(
            True, False, 200, None, client, db_session, verified_user
        )

    async def test_create_tracking_link_as_verified_user_assoc_wrong_organization(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_create(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

    # CASES
    async def test_create_tracking_link_as_superuser_already_exists(
        self, client, db_session, admin_user
    ) -> None:
        a_organization = await create_random_organization(db_session)
        b_organization = await create_random_organization(db_session)
        a_link = await create_random_tracking_link(db_session, a_organization.id)
        await create_random_tracking_link(db_session, a_organization.id)
        await create_random_tracking_link(db_session, b_organization.id)
        data_in = {
            "url": a_link.url,
            "is_active": True,
        }
        response: Response = await client.post(
            "utmlinks/",
            headers=admin_user.token_headers,
            json=data_in,
        )
        data = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in data["detail"]

    async def test_create_tracking_link_as_superuser_organization_not_found(
        self, client, db_session, admin_user
    ) -> None:
        a_organization = await create_random_organization(db_session)
        client_b = get_uuid_str()
        await create_random_tracking_link(db_session, a_organization.id)
        await create_random_tracking_link(db_session, a_organization.id)
        link_url = "/" + random_lower_string(16)
        data_in = {
            "url": link_url,
            "is_active": True,
            "organization_id": client_b,
        }
        response: Response = await client.post(
            "utmlinks/",
            headers=admin_user.token_headers,
            json=data_in,
        )
        data = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ORGANIZATION_NOT_FOUND == data["detail"]


class TestReadTrackingLinks:
    # AUTHORIZED CLIENTS
    async def test_delete_tracking_link_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_read(False, False, 200, None, client, db_session, admin_user)

    async def test_delete_tracking_link_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_delete_tracking_link_as_manager_user_assoc_with_organization(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(
            True, False, 200, None, client, db_session, manager_user
        )

    async def test_delete_tracking_link_as_manager_user_assoc_with_wrong_organization(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(True, True, 200, None, client, db_session, manager_user)

    async def test_delete_tracking_link_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_read(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_delete_tracking_link_as_client_a_user_assoc_with_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_read(
            True, False, 200, None, client, db_session, client_a_user
        )

    async def test_delete_tracking_link_as_client_a_user_assoc_with_wrong_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_read(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_delete_tracking_link_as_employee_user_assoc_with_organization(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_read(
            True, False, 200, None, client, db_session, employee_user
        )

    async def test_delete_tracking_link_as_verified_user(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_read(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

    async def test_delete_tracking_link_as_verified_user_assoc_with_organization(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_read(
            True, False, 200, None, client, db_session, verified_user
        )

    async def test_delete_tracking_link_as_verified_user_assoc_with_wrong_organization(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_read(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )


class TestUpdateTrackingLinks:
    # AUTHORIZED CLIENTS
    async def test_update_tracking_link_as_admin_user_update_any_tracking_link(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_update(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_update_tracking_link_as_manager_user_update_tracking_link(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_update(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_update_tracking_link_as_client_a_user_cannot_update_tracking_link_not_assigned(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_update(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_update_tracking_link_as_client_a_user_update_tracking_link_assigned_to_client(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_update(
            True, False, 200, None, client, db_session, client_a_user
        )

    async def test_update_tracking_link_as_client_a_user_update_tracking_link_assigned_to_wrong_client(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_update(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_update_tracking_link_as_employee_user_update_tracking_link_assigned_to_client(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_update(
            True, False, 200, None, client, db_session, employee_user
        )

    async def test_update_tracking_link_as_verified_user_update_tracking_link_not_assigned(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_update(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

    async def test_update_tracking_link_as_verified_user_update_tracking_link_assigned_to_client(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_update(
            True, False, 200, None, client, db_session, verified_user
        )

    async def test_update_tracking_link_as_verified_user_update_tracking_link_assigned_to_wrong_client(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_update(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

    # CASES
    async def test_update_tracking_link_as_superuser_already_exists(
        self,
        admin_user: ClientAuthorizedUser,
        client: AsyncClient,
        db_session: AsyncSession,
    ) -> None:
        a_organization = await create_random_organization(db_session)
        b_organization = await create_random_organization(db_session)
        a_link = await create_random_tracking_link(db_session, a_organization.id)
        await create_random_tracking_link(db_session, a_organization.id)
        b_link = await create_random_tracking_link(db_session, b_organization.id)
        data_in = {
            "url": a_link.url,
            "is_active": True,
        }
        response: Response = await client.patch(
            f"utmlinks/{b_link.id}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        data = response.json()
        assert response.status_code == 400
        assert ERROR_MESSAGE_ENTITY_EXISTS in data["detail"]

    async def test_update_tracking_link_as_superuser_organization_not_found(
        self,
        admin_user: ClientAuthorizedUser,
        client: AsyncClient,
        db_session: AsyncSession,
    ) -> None:
        a_organization = await create_random_organization(db_session)
        client_b = get_uuid_str()
        a_link = await create_random_tracking_link(db_session, a_organization.id)
        await create_random_tracking_link(db_session, a_organization.id)
        link_url = "/" + random_lower_string(16)
        data_in = {
            "url": link_url,
            "is_active": True,
            "organization_id": client_b,
        }
        response: Response = await client.patch(
            f"utmlinks/{a_link.id}",
            headers=admin_user.token_headers,
            json=data_in,
        )
        data = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ORGANIZATION_NOT_FOUND == data["detail"]


class TestDeleteTrackingLinks:
    # AUTHORIZED CLIENTS
    async def test_delete_tracking_link_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_delete(
            False, False, 200, None, client, db_session, admin_user
        )

    async def test_delete_tracking_link_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(
            False, False, 200, None, client, db_session, manager_user
        )

    async def test_delete_tracking_link_as_manager_user_assoc_with_organization(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(
            True, False, 200, None, client, db_session, manager_user
        )

    async def test_delete_tracking_link_as_manager_user_assoc_with_wrong_organization(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(
            True, True, 200, None, client, db_session, manager_user
        )

    async def test_delete_tracking_link_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_delete_tracking_link_as_client_a_user_assoc_with_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(
            True, False, 200, None, client, db_session, client_a_user
        )

    async def test_delete_tracking_link_as_client_a_user_assoc_with_wrong_organization(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_delete(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            client_a_user,
        )

    async def test_delete_tracking_link_as_employee_user_assoc_with_organization(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_delete(
            True, False, 200, None, client, db_session, employee_user
        )

    async def test_delete_tracking_link_as_verified_user(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_delete(
            False,
            False,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

    async def test_delete_tracking_link_as_verified_user_assoc_with_organization(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_delete(
            True, False, 200, None, client, db_session, verified_user
        )

    async def test_delete_tracking_link_as_verified_user_assoc_with_wrong_organization(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_delete(
            True,
            True,
            405,
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
            client,
            db_session,
            verified_user,
        )

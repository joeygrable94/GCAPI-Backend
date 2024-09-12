from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.tracking_link import build_utm_link, create_random_tracking_link
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_domain, random_lower_string

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.models import User, UserClient
from app.schemas import ClientRead, TrackingLinkRead

pytestmark = pytest.mark.asyncio


async def test_create_client_tracking_link_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    domain_name = random_domain()
    url_path = "/%s" % random_lower_string(16)
    utm_cmpn = random_lower_string(16)
    utm_mdm = random_lower_string(16)
    utm_src = random_lower_string(16)
    utm_cnt = random_lower_string(16)
    utm_trm = random_lower_string(16)
    tracked_url = build_utm_link(
        domain_name, url_path, utm_cmpn, utm_mdm, utm_src, utm_cnt, utm_trm
    )
    data_in: Dict[str, Any] = dict(
        url=tracked_url, is_active=True, client_id=str(a_client.id)
    )
    response: Response = await client.post(
        "links/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert len(data["url_hash"]) == 64
    assert data["url"] == tracked_url
    assert data["utm_campaign"] == utm_cmpn
    assert data["utm_medium"] == utm_mdm
    assert data["utm_source"] == utm_src
    assert data["utm_content"] == utm_cnt
    assert data["utm_term"] == utm_trm
    assert data["is_active"] is True


async def test_create_client_tracking_link_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(
        db_session, a_client.id
    )
    fake_client_id = get_uuid_str()
    data_in: Dict[str, Any] = dict(
        url=a_tacked_link.url, is_active=True, client_id=fake_client_id
    )
    response: Response = await client.post(
        "links/",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_client_tracking_link_as_superuser_url_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(
        db_session, a_client.id
    )
    data_in: Dict[str, Any] = dict(
        url=a_tacked_link.url, is_active=True, client_id=str(a_tacked_link.client_id)
    )
    response: Response = await client.post(
        "links/",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert data["detail"] == ErrorCode.TRACKING_LINK_EXISTS


async def test_create_client_tracking_link_as_superuser_utm_params_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    domain_name = random_domain()
    url_path = "/%s" % random_lower_string(16)
    utm_cmpn = random_lower_string(256)
    utm_mdm = random_lower_string(16)
    utm_src = random_lower_string(16)
    utm_cnt = random_lower_string(16)
    utm_trm = random_lower_string(16)
    tracked_url = build_utm_link(
        domain_name, url_path, utm_cmpn, utm_mdm, utm_src, utm_cnt, utm_trm
    )
    data_in: Dict[str, Any] = dict(
        url=tracked_url, is_active=True, client_id=str(a_client.id)
    )
    response: Response = await client.post(
        "links/",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert data["detail"] == ErrorCode.TRACKING_LINK_UTM_PARAMS_INVALID


async def test_create_client_tracking_link_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    domain_name = random_domain()
    url_path = "/%s" % random_lower_string(16)
    utm_cmpn = random_lower_string(16)
    utm_mdm = random_lower_string(16)
    utm_src = random_lower_string(16)
    utm_cnt = random_lower_string(16)
    utm_trm = random_lower_string(16)
    tracked_url = build_utm_link(
        domain_name, url_path, utm_cmpn, utm_mdm, utm_src, utm_cnt, utm_trm
    )
    data_in: Dict[str, Any] = dict(
        url=tracked_url, is_active=True, client_id=str(a_client.id)
    )
    response: Response = await client.post(
        "links/",
        headers=employee_token_headers,
        json=data_in,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert len(data["url_hash"]) == 64
    assert data["url"] == tracked_url
    assert data["utm_campaign"] == utm_cmpn
    assert data["utm_medium"] == utm_mdm
    assert data["utm_source"] == utm_src
    assert data["utm_content"] == utm_cnt
    assert data["utm_term"] == utm_trm
    assert data["is_active"] is True


async def test_create_client_tracking_link_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_employee
    )
    a_client: ClientRead = await create_random_client(db_session)
    domain_name = random_domain()
    url_path = "/%s" % random_lower_string(16)
    utm_cmpn = random_lower_string(16)
    utm_mdm = random_lower_string(16)
    utm_src = random_lower_string(16)
    utm_cnt = random_lower_string(16)
    utm_trm = random_lower_string(16)
    tracked_url = build_utm_link(
        domain_name, url_path, utm_cmpn, utm_mdm, utm_src, utm_cnt, utm_trm
    )
    data_in: Dict[str, Any] = dict(
        url=tracked_url, is_active=True, client_id=str(a_client.id)
    )
    response: Response = await client.post(
        "links/",
        headers=employee_token_headers,
        json=data_in,
    )
    assert response.status_code == 405
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS

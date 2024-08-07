from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.tracking_link import create_random_tracking_link
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.models import User, UserClient
from app.schemas import ClientRead, TrackingLinkRead

pytestmark = pytest.mark.asyncio


async def test_update_client_tracking_link_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    parsed_url = urlparse(a_tacked_link.url)
    old_utm_cmpn = parse_qs(parsed_url.query)["utm_campaign"][0]
    new_utm_cmpn = "new_utm_campaign"
    new_url = a_tacked_link.url.replace(old_utm_cmpn, new_utm_cmpn)
    data_in: Dict[str, Any] = dict(
        url=new_url,
        is_active=True,
    )
    response: Response = await client.patch(
        f"clients/links/{a_client.id}/{a_tacked_link.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert len(data["url_hash"]) == 64
    assert data["url_hash"] != a_tacked_link.url_hash
    assert data["url"] == new_url
    assert data["utm_campaign"] == new_utm_cmpn
    assert data["utm_medium"] == a_tacked_link.utm_medium
    assert data["utm_source"] == a_tacked_link.utm_source
    assert data["utm_content"] == a_tacked_link.utm_content
    assert data["utm_term"] == a_tacked_link.utm_term
    assert data["is_active"] == a_tacked_link.is_active


async def test_update_client_tracking_link_by_id_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_fake_client = get_uuid_str()
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    parsed_url = urlparse(a_tacked_link.url)
    old_utm_cmpn = parse_qs(parsed_url.query)["utm_campaign"][0]
    new_utm_cmpn = "new_utm_campaign"
    new_url = a_tacked_link.url.replace(old_utm_cmpn, new_utm_cmpn)
    data_in: Dict[str, Any] = dict(
        url=new_url,
        is_active=True,
    )
    response: Response = await client.patch(
        f"clients/links/{a_fake_client}/{a_tacked_link.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_update_client_tracking_link_by_id_as_superuser_url_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    b_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    data_in: Dict[str, Any] = dict(
        url=b_tacked_link.url,
        is_active=False,
    )
    response: Response = await client.patch(
        f"clients/links/{a_client.id}/{a_tacked_link.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert data["detail"] == ErrorCode.TRACKING_LINK_EXISTS


async def test_update_client_tracking_link_by_id_as_superuser_utm_params_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    parsed_url = urlparse(a_tacked_link.url)
    old_utm_cmpn = parse_qs(parsed_url.query)["utm_campaign"][0]
    new_utm_cmpn = random_lower_string(256)
    new_url = a_tacked_link.url.replace(old_utm_cmpn, new_utm_cmpn)
    data_in: Dict[str, Any] = dict(
        url=new_url,
        is_active=False,
    )
    response: Response = await client.patch(
        f"clients/links/{a_client.id}/{a_tacked_link.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert data["detail"] == ErrorCode.TRACKING_LINK_UTM_PARAMS_INVALID


async def test_update_client_tracking_link_by_id_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    parsed_url = urlparse(a_tacked_link.url)
    old_utm_cmpn = parse_qs(parsed_url.query)["utm_campaign"][0]
    new_utm_cmpn = "new_utm_campaign"
    new_url = a_tacked_link.url.replace(old_utm_cmpn, new_utm_cmpn)
    data_in: Dict[str, Any] = dict(
        url=new_url,
        is_active=True,
    )
    response: Response = await client.patch(
        f"clients/links/{a_client.id}/{a_tacked_link.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert len(data["url_hash"]) == 64
    assert data["url_hash"] != a_tacked_link.url_hash
    assert data["url"] == new_url
    assert data["utm_campaign"] == new_utm_cmpn
    assert data["utm_medium"] == a_tacked_link.utm_medium
    assert data["utm_source"] == a_tacked_link.utm_source
    assert data["utm_content"] == a_tacked_link.utm_content
    assert data["utm_term"] == a_tacked_link.utm_term
    assert data["is_active"] == a_tacked_link.is_active


async def test_update_client_tracking_link_by_id_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_employee
    )
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    parsed_url = urlparse(a_tacked_link.url)
    old_utm_cmpn = parse_qs(parsed_url.query)["utm_campaign"][0]
    new_utm_cmpn = "new_utm_campaign"
    new_url = a_tacked_link.url.replace(old_utm_cmpn, new_utm_cmpn)
    data_in: Dict[str, Any] = dict(
        url=new_url,
        is_active=True,
    )
    response: Response = await client.patch(
        f"clients/links/{a_client.id}/{a_tacked_link.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_update_client_tracking_link_by_id_as_employee_forbidden_client(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    parsed_url = urlparse(a_tacked_link.url)
    old_utm_cmpn = parse_qs(parsed_url.query)["utm_campaign"][0]
    new_utm_cmpn = "new_utm_campaign"
    new_url = a_tacked_link.url.replace(old_utm_cmpn, new_utm_cmpn)
    data_in: Dict[str, Any] = dict(
        url=new_url,
        is_active=True,
    )
    response: Response = await client.patch(
        f"clients/links/{b_client.id}/{a_tacked_link.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS

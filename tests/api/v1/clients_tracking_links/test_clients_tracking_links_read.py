from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.tracking_link import create_random_tracking_link
from tests.utils.users import get_user_by_email

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.db.utilities import hash_url
from app.models import User
from app.schemas import ClientRead, TrackingLinkRead

pytestmark = pytest.mark.asyncio


async def test_read_client_tracking_link_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_hashed_url = hash_url(a_tacked_link.url)
    response: Response = await client.get(
        f"clients/links/{a_client.id}/{a_tacked_link.id}", headers=admin_token_headers
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["id"] == str(a_tacked_link.id)
    assert data["url_hash"] == a_hashed_url
    assert data["url"] == a_tacked_link.url
    assert data["utm_campaign"] == a_tacked_link.utm_campaign
    assert data["utm_medium"] == a_tacked_link.utm_medium
    assert data["utm_source"] == a_tacked_link.utm_source
    assert data["utm_content"] == a_tacked_link.utm_content
    assert data["utm_term"] == a_tacked_link.utm_term


async def test_read_client_tracking_link_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_id = get_uuid_str()
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_admin
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(  # noqa: F841
        db_session
    )
    response: Response = await client.get(
        f"clients/links/{a_client.id}/{fake_id}", headers=admin_token_headers
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.TRACKING_LINK_NOT_FOUND

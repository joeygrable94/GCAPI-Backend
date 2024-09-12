from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.tracking_link import create_random_tracking_link
from tests.utils.users import get_user_by_email

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.models import User, UserClient
from app.schemas import ClientRead, TrackingLinkRead

pytestmark = pytest.mark.asyncio


async def test_delete_client_tracking_link_by_id_as_superuser(
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
    response: Response = await client.delete(
        f"links/{a_tacked_link.id}", headers=admin_token_headers
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"links/{a_tacked_link.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.TRACKING_LINK_NOT_FOUND


async def test_delete_client_tracking_link_by_id_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    a_tacked_link: TrackingLinkRead = await create_random_tracking_link(
        db_session, a_client.id
    )
    response: Response = await client.delete(
        f"links/{a_tacked_link.id}",
        headers=employee_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"links/{a_tacked_link.id}",
        headers=employee_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.TRACKING_LINK_NOT_FOUND

from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.tracking_link import (
    assign_tracking_link_to_client,
    create_random_tracking_link,
)
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.models import User, UserClient
from app.schemas import ClientRead, TrackingLinkRead

pytestmark = pytest.mark.asyncio


async def test_list_all_client_reports_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    tacked_link_1: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_1 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_1, a_client
    )
    tacked_link_2: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_2 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_2, a_client
    )
    tacked_link_3: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_3 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_3, a_client
    )
    tacked_link_4: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_4 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_4, a_client
    )
    tacked_link_5: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_5 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_5, a_client
    )
    response: Response = await client.get(
        "clients/links/",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 5
    assert data["size"] == 1000
    assert len(data["results"]) == 5


async def test_list_all_client_reports_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    tacked_link_1: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_1 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_1, a_client
    )
    tacked_link_2: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_2 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_2, a_client
    )
    tacked_link_3: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_3 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_3, b_client
    )
    tacked_link_4: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_4 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_4, b_client
    )
    tacked_link_5: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_5 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_5, b_client
    )
    response: Response = await client.get(
        "clients/links/",
        headers=employee_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2

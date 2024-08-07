from typing import Any, Dict

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.tracking_link import (
    assign_tracking_link_to_client,
    create_random_tracking_link,
)

from app.schemas import ClientRead, TrackingLinkRead

pytestmark = pytest.mark.asyncio


async def test_list_all_client_reports_as_superuser_by_not_active(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    tacked_link_1: TrackingLinkRead = await create_random_tracking_link(
        db_session, is_active=False
    )
    a_client_link_1 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_1, a_client
    )
    tacked_link_2: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_2 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_2, a_client
    )
    tacked_link_3: TrackingLinkRead = await create_random_tracking_link(
        db_session, is_active=False
    )
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
        params=QueryParams({"client_id": str(a_client.id), "is_active": False}),
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for item in data["results"]:
        assert item["is_active"] is False


async def test_list_all_client_reports_as_superuser_by_is_active(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    tacked_link_1: TrackingLinkRead = await create_random_tracking_link(
        db_session, is_active=False
    )
    a_client_link_1 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_1, a_client
    )
    tacked_link_2: TrackingLinkRead = await create_random_tracking_link(db_session)
    a_client_link_2 = await assign_tracking_link_to_client(  # noqa: F841
        db_session, tacked_link_2, a_client
    )
    tacked_link_3: TrackingLinkRead = await create_random_tracking_link(
        db_session, is_active=False
    )
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
        params=QueryParams({"client_id": str(a_client.id), "is_active": True}),
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 1000
    assert len(data["results"]) == 3
    for item in data["results"]:
        assert item["is_active"] is True

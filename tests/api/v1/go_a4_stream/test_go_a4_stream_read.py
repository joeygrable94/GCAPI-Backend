from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.websites import create_random_website

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import GoAnalytics4StreamRepository
from app.models import GoAnalytics4Stream, Website
from app.schemas import (
    ClientRead,
    GoAnalytics4PropertyRead,
    GoAnalytics4StreamRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_read_ga4_property_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    entry: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    response: Response = await client.get(
        f"ga4/stream/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert "stream_id" in data
    assert data["ga4_id"] == str(ga4_property.id)
    assert data["website_id"] == str(a_website.id)
    repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(db_session)
    existing_data: GoAnalytics4Stream | None = await repo.read(entry.id)
    assert existing_data
    assert existing_data.stream_id == data["stream_id"]
    assert existing_data.ga4_id == ga4_property.id
    assert str(existing_data.website_id) == data["website_id"]


async def test_read_ga4_property_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"ga4/stream/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GA4_STREAM_NOT_FOUND

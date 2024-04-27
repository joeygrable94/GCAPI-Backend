from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.ga4 import create_random_ga4_property
from tests.utils.websites import create_random_website

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.crud import GoAnalytics4PropertyRepository
from app.models import GoAnalytics4Property
from app.schemas import ClientRead, WebsiteRead
from app.schemas.go_a4 import GoAnalytics4PropertyRead

pytestmark = pytest.mark.asyncio


async def test_read_ga4_property_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    entry: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    response: Response = await client.get(
        f"ga4/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert "measurement_id" in data
    assert "property_id" in data
    assert data["client_id"] == str(a_client.id)
    assert data["website_id"] == str(a_website.id)
    repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(db_session)
    existing_data: GoAnalytics4Property | None = await repo.read(entry.id)
    assert existing_data
    assert existing_data.measurement_id == data["measurement_id"]
    assert existing_data.property_id == data["property_id"]
    assert str(existing_data.client_id) == data["client_id"]
    assert str(existing_data.website_id) == data["website_id"]


async def test_read_ga4_property_by_id_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"ga4/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GA4_PROPERTY_NOT_FOUND

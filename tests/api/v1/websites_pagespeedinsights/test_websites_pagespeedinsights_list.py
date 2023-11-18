from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)
from tests.utils.websites import create_random_website

from app.schemas import WebsitePageRead, WebsitePageSpeedInsightsRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_website_pagespeedinsights_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(db_session)
    )
    response: Response = await client.get("psi/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == entry_1.id:
            assert entry["strategy"] == entry_1.strategy
            assert entry["page_id"] == entry_1.page_id
            assert entry["website_id"] == entry_1.website_id
        if entry["id"] == entry_2.id:
            assert entry["strategy"] == entry_2.strategy
            assert entry["page_id"] == entry_2.page_id
            assert entry["website_id"] == entry_2.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id_devices_all(  # noqa: E501
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
            "page_id": str(webpage_a.id),
            "strategy": ["desktop", "mobile"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == entry_3.id:
            assert entry["strategy"] == entry_3.strategy
            assert entry["page_id"] == entry_3.page_id
            assert entry["website_id"] == entry_3.website_id
        if entry["id"] == entry_7.id:
            assert entry["strategy"] == entry_7.strategy
            assert entry["page_id"] == entry_7.page_id
            assert entry["website_id"] == entry_7.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id_devices_desktop(  # noqa: E501
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
            "page_id": str(webpage_a.id),
            "strategy": ["desktop"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
    for entry in data["results"]:
        if entry["id"] == entry_3.id:
            assert entry["strategy"] == entry_3.strategy
            assert entry["page_id"] == entry_3.page_id
            assert entry["website_id"] == entry_3.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id_devices_mobile(  # noqa: E501
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_b.id),
            "page_id": str(webpage_b.id),
            "strategy": ["mobile"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
    for entry in data["results"]:
        if entry["id"] == entry_9.id:
            assert entry["strategy"] == entry_9.strategy
            assert entry["page_id"] == entry_9.page_id
            assert entry["website_id"] == entry_9.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
            "page_id": str(webpage_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == entry_3.id:
            assert entry["strategy"] == entry_3.strategy
            assert entry["page_id"] == entry_3.page_id
            assert entry["website_id"] == entry_3.website_id
        if entry["id"] == entry_7.id:
            assert entry["strategy"] == entry_7.strategy
            assert entry["page_id"] == entry_7.page_id
            assert entry["website_id"] == entry_7.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_devices(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
            "strategy": ["mobile"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == entry_7.id:
            assert entry["strategy"] == entry_7.strategy
            assert entry["page_id"] == entry_7.page_id
            assert entry["website_id"] == entry_7.website_id
        if entry["id"] == entry_8.id:
            assert entry["strategy"] == entry_8.strategy
            assert entry["page_id"] == entry_8.page_id
            assert entry["website_id"] == entry_8.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_page_id_devices(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "page_id": str(webpage_b.id),
            "strategy": ["desktop"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == entry_4.id:
            assert entry["strategy"] == entry_4.strategy
            assert entry["page_id"] == entry_4.page_id
            assert entry["website_id"] == entry_4.website_id
        if entry["id"] == entry_5.id:
            assert entry["strategy"] == entry_5.strategy
            assert entry["page_id"] == entry_5.page_id
            assert entry["website_id"] == entry_5.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == entry_3.id:
            assert entry["strategy"] == entry_3.strategy
            assert entry["page_id"] == entry_3.page_id
            assert entry["website_id"] == entry_3.website_id
        if entry["id"] == entry_4.id:
            assert entry["strategy"] == entry_4.strategy
            assert entry["page_id"] == entry_4.page_id
            assert entry["website_id"] == entry_4.website_id
        if entry["id"] == entry_7.id:
            assert entry["strategy"] == entry_7.strategy
            assert entry["page_id"] == entry_7.page_id
            assert entry["website_id"] == entry_7.website_id
        if entry["id"] == entry_8.id:
            assert entry["strategy"] == entry_8.strategy
            assert entry["page_id"] == entry_8.page_id
            assert entry["website_id"] == entry_8.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_page_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "page_id": str(webpage_b.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == entry_4.id:
            assert entry["strategy"] == entry_4.strategy
            assert entry["page_id"] == entry_4.page_id
            assert entry["website_id"] == entry_4.website_id
        if entry["id"] == entry_5.id:
            assert entry["strategy"] == entry_5.strategy
            assert entry["page_id"] == entry_5.page_id
            assert entry["website_id"] == entry_5.website_id
        if entry["id"] == entry_8.id:
            assert entry["strategy"] == entry_8.strategy
            assert entry["page_id"] == entry_8.page_id
            assert entry["website_id"] == entry_8.website_id
        if entry["id"] == entry_9.id:
            assert entry["strategy"] == entry_9.strategy
            assert entry["page_id"] == entry_9.page_id
            assert entry["website_id"] == entry_9.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_devices_all(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    webpage_a: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id
    )
    webpage_b: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_2: WebsitePageSpeedInsightsRead = (  # noqa: F841
        await create_random_website_page_speed_insights(db_session)
    )
    entry_3: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_4: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_5: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="desktop",
        )
    )
    entry_6: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="desktop",
        )
    )
    entry_7: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    entry_8: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_a.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_9: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_b.id,
            device_strategy="mobile",
        )
    )
    entry_10: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(
            db_session,
            website_id=website_b.id,
            page_id=webpage_a.id,
            device_strategy="mobile",
        )
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_token_headers,
        params={
            "strategy": ["desktop", "mobile"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 94
    assert data["size"] == 1000
    assert len(data["results"]) == 94
    for entry in data["results"]:
        if entry["id"] == entry_3.id:
            assert entry["strategy"] == entry_3.strategy
            assert entry["page_id"] == entry_3.page_id
            assert entry["website_id"] == entry_3.website_id
        if entry["id"] == entry_4.id:
            assert entry["strategy"] == entry_4.strategy
            assert entry["page_id"] == entry_4.page_id
            assert entry["website_id"] == entry_4.website_id
        if entry["id"] == entry_5.id:
            assert entry["strategy"] == entry_5.strategy
            assert entry["page_id"] == entry_5.page_id
            assert entry["website_id"] == entry_5.website_id
        if entry["id"] == entry_6.id:
            assert entry["strategy"] == entry_6.strategy
            assert entry["page_id"] == entry_6.page_id
            assert entry["website_id"] == entry_6.website_id
        if entry["id"] == entry_7.id:
            assert entry["strategy"] == entry_7.strategy
            assert entry["page_id"] == entry_7.page_id
            assert entry["website_id"] == entry_7.website_id
        if entry["id"] == entry_8.id:
            assert entry["strategy"] == entry_8.strategy
            assert entry["page_id"] == entry_8.page_id
            assert entry["website_id"] == entry_8.website_id
        if entry["id"] == entry_9.id:
            assert entry["strategy"] == entry_9.strategy
            assert entry["page_id"] == entry_9.page_id
            assert entry["website_id"] == entry_9.website_id
        if entry["id"] == entry_10.id:
            assert entry["strategy"] == entry_10.strategy
            assert entry["page_id"] == entry_10.page_id
            assert entry["website_id"] == entry_10.website_id

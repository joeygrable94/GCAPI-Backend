from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_pages import create_random_website_page
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_list_all_website_pagespeedinsights_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_1 = await create_random_website_page_speed_insights(db_session)
    entry_2 = await create_random_website_page_speed_insights(db_session)
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == entry_1.id:
            assert entry["strategy"] == entry_1.strategy
            assert entry["page_id"] == entry_1.page_id
            assert entry["website_id"] == entry_1.website_id
        if entry["id"] == entry_2.id:
            assert entry["strategy"] == entry_2.strategy
            assert entry["page_id"] == entry_2.page_id
            assert entry["website_id"] == entry_2.website_id


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id_devices_all(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    entry_3 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_7 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id_devices_desktop(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    entry_3 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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


async def test_list_website_pagespeedinsights_as_superuser_by_website_id_page_id_devices_mobile(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    entry_9 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    entry_3 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_7 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )

    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )

    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_7 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    entry_8 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )

    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )

    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )

    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_4 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    entry_5 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    entry_3 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_4 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_7 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    entry_8 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_4 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    entry_5 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    entry_8 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    entry_9 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
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
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session)
    website_b = await create_random_website(db_session)
    webpage_a = await create_random_website_page(db_session, website_id=website_a.id)
    webpage_b = await create_random_website_page(db_session, website_id=website_b.id)
    # entries
    await create_random_website_page_speed_insights(db_session)
    await create_random_website_page_speed_insights(db_session)
    entry_3 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_4 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    entry_5 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="desktop",
    )
    entry_6 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="desktop",
    )
    entry_7 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    entry_8 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_a.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    entry_9 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_b.id,
        device_strategy="mobile",
    )
    entry_10 = await create_random_website_page_speed_insights(
        db_session,
        website_id=website_b.id,
        page_id=webpage_a.id,
        device_strategy="mobile",
    )
    response: Response = await client.get(
        "psi/",
        headers=admin_user.token_headers,
        params={
            "strategy": ["desktop", "mobile"],
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 10
    assert data["size"] == 1000
    assert len(data["results"]) == 10
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


async def test_list_all_website_pagespeedinsights_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get("psi/", headers=employee_user.token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 0
    assert data["size"] == 1000
    assert len(data["results"]) == 0

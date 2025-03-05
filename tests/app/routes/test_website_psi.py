from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
    ERROR_MESSAGE_ENTITY_RELATIONSHOP_NOT_FOUND,
)
from app.entities.website.schemas import WebsiteRead
from app.entities.website_pagespeedinsight.schemas import WebsitePageSpeedInsightsBase
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_boolean, random_lower_string
from tests.utils.website_pages import create_random_website_page
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
    generate_psi_base,
)
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.anyio


class TestListWebsitePageSpeedInsights:
    # AUTHORIZED CLIENTS
    async def test_list_all_website_pagespeedinsights_as_superuser(
        self,
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_a = await create_random_website(db_session)
        website_b = await create_random_website(db_session)
        webpage_a = await create_random_website_page(
            db_session, website_id=website_a.id
        )
        webpage_b = await create_random_website_page(
            db_session, website_id=website_b.id
        )
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
        assert data["total"] == 92
        assert data["size"] == 1000
        assert len(data["results"]) == 92
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

    async def test_list_all_website_pagespeedinsights_as_employee_user(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get(
            "psi/", headers=employee_user.token_headers
        )
        assert 200 <= response.status_code < 300
        data: Any = response.json()
        assert data["page"] == 1
        assert data["total"] == 0
        assert data["size"] == 1000
        assert len(data["results"]) == 0


class TestCreateWebsitePageSpeedInsights:
    # CASES
    async def test_create_website_pagespeedinsights_as_admin_user(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        a_website = await create_random_website(db_session)
        a_webpage = await create_random_website_page(
            db_session, a_website.id, "/" + random_lower_string(8)
        )
        d_strategy: str = "mobile"
        psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
            device_strategy=d_strategy
        )
        response: Response = await client.post(
            "psi/",
            params={"website_id": str(a_website.id), "page_id": str(a_webpage.id)},
            headers=admin_user.token_headers,
            json=psi_base.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data["id"] is not None
        assert data["strategy"] == d_strategy
        assert data["website_id"] == str(a_website.id)
        assert data["page_id"] == str(a_webpage.id)

    async def test_create_website_pagespeedinsights_as_admin_user_query_website_not_exists(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        webpage_id = get_uuid_str()
        d_strategy: str = "mobile"
        psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
            device_strategy=d_strategy
        )
        response: Response = await client.post(
            "psi/",
            params={"page_id": str(webpage_id)},
            headers=admin_user.token_headers,
            json=psi_base.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

    async def test_create_website_pagespeedinsights_as_admin_user_website_not_exists(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        website_id = get_uuid_str()
        webpage_id = get_uuid_str()
        d_strategy: str = "mobile"
        psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
            device_strategy=d_strategy
        )
        response: Response = await client.post(
            "psi/",
            params={"website_id": str(website_id), "page_id": str(webpage_id)},
            headers=admin_user.token_headers,
            json=psi_base.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

    async def test_create_website_pagespeedinsights_as_admin_user_webaite_page_not_exists(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        domain: str = "gcembed.getcommunity.com"
        is_secure: bool = random_boolean()
        w_data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
        response: Response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=w_data,
        )
        assert 200 <= response.status_code < 300
        a_website = WebsiteRead(**response.json())
        webpage_id = get_uuid_str()
        d_strategy: str = "mobile"
        psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
            device_strategy=d_strategy
        )
        response: Response = await client.post(
            "psi/",
            params={"website_id": str(a_website.id), "page_id": str(webpage_id)},
            headers=admin_user.token_headers,
            json=psi_base.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

    async def test_create_website_pagespeedinsights_as_admin_user_query_website_page_not_exists(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        domain: str = "giftgurugal.com"
        is_secure: bool = random_boolean()
        w_data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
        response: Response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=w_data,
        )
        assert 200 <= response.status_code < 300
        a_website = WebsiteRead(**response.json())
        d_strategy: str = "mobile"
        psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
            device_strategy=d_strategy
        )
        response: Response = await client.post(
            "psi/",
            params={"website_id": str(a_website.id)},
            headers=admin_user.token_headers,
            json=psi_base.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

    async def test_create_website_pagespeedinsights_as_admin_user_query_website_page_relationship_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        domain: str = "getcommunity.com"
        is_secure: bool = random_boolean()
        a_website = await create_random_website(db_session, domain, is_secure)
        await create_random_website_page(db_session, website_id=a_website.id)
        b_page = await create_random_website_page(
            db_session, path="/" + random_lower_string(8)
        )
        d_strategy: str = "mobile"
        psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
            device_strategy=d_strategy
        )
        response: Response = await client.post(
            "psi/",
            params={"website_id": str(a_website.id), "page_id": str(b_page.id)},
            headers=admin_user.token_headers,
            json=psi_base.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_RELATIONSHOP_NOT_FOUND in data["detail"]


class TestReadWebsitePageSpeedInsights:
    # CASES
    async def test_read_website_pagespeedinsights_by_id_as_superuser(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry = await create_random_website_page_speed_insights(db_session)
        response: Response = await client.get(
            f"psi/{entry.id}", headers=admin_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data["id"] == str(entry.id)
        assert data["strategy"] == entry.strategy
        assert data["website_id"] == str(entry.website_id)
        assert data["page_id"] == str(entry.page_id)

    async def test_read_website_pagespeedinsights_by_id_as_superuser_page_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry_id: str = get_uuid_str()
        response: Response = await client.get(
            f"psi/{entry_id}", headers=admin_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestDeleteWebsitePageSpeedInsights:
    # AUTHORIZED CLIENTS
    async def test_delete_website_pagespeedinsights_by_id_as_superuser(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        entry = await create_random_website_page_speed_insights(db_session)
        response: Response = await client.delete(
            f"psi/{entry.id}", headers=admin_user.token_headers
        )
        assert 200 <= response.status_code < 300
        response: Response = await client.get(
            f"psi/{entry.id}", headers=admin_user.token_headers
        )
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]

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
from tests.utils.utils import random_boolean
from tests.utils.website_pages import create_random_website_page
from tests.utils.website_pagespeedinsights import generate_psi_base
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_create_website_pagespeedinsights_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    a_webpage = await create_random_website_page(db_session, a_website.id, "/")
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


async def test_create_website_pagespeedinsights_as_superuser_query_website_not_exists(
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


async def test_create_website_pagespeedinsights_as_superuser_website_not_exists(
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


async def test_create_website_pagespeedinsights_as_superuser_webaite_page_not_exists(
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


async def test_create_website_pagespeedinsights_as_superuser_query_website_page_not_exists(
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


async def test_create_website_pagespeedinsights_as_superuser_query_website_page_relationship_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    domain: str = "giftgurugal.com"
    is_secure: bool = random_boolean()
    a_website = await create_random_website(db_session, domain, is_secure)
    await create_random_website_page(db_session, website_id=a_website.id)
    b_page = await create_random_website_page(db_session, path="/")
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

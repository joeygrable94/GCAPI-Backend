from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from tests.utils.utils import random_boolean
from tests.utils.website_pagespeedinsights import generate_psi_base

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.schemas import WebsiteMapRead
from app.schemas import WebsitePageRead
from app.schemas import WebsitePageSpeedInsightsBase
from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_create_website_pagespeedinsights_as_superuser(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    # create a website
    domain: str = "aestheticclimbinggym.com"
    is_secure: bool = random_boolean()
    w_data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=admin_token_headers,
        json=w_data,
    )
    assert 200 <= response.status_code < 300
    w_entry = response.json()
    a_website: WebsiteRead = WebsiteRead(**w_entry["website"])
    # create a website map
    s_data = {
        "url": "/sitemap_index.xml",
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_token_headers,
        json=s_data,
    )
    assert 200 <= response.status_code < 300
    a_sitemap: WebsiteMapRead = WebsiteMapRead(**response.json())
    # create a website page
    p_data = {
        "url": "/",
        "status": 200,
        "priority": 0.5,
        "website_id": str(a_website.id),
        "sitemap_id": str(a_sitemap.id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=admin_token_headers,
        json=p_data,
    )
    assert 200 <= response.status_code < 300
    p_entry: Dict[str, Any] = response.json()
    a_webpage: WebsitePageRead = WebsitePageRead(**p_entry)
    # create page speed insights
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response: Response = await client.post(
        "psi/",
        params={"website_id": str(a_website.id), "page_id": str(a_webpage.id)},
        headers=admin_token_headers,
        json=psi_base.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] is not None
    assert data["strategy"] == d_strategy
    assert data["website_id"] == str(a_website.id)
    assert data["page_id"] == str(a_webpage.id)


async def test_create_website_pagespeedinsights_as_superuser_query_website_not_exists(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    webpage_id = get_uuid_str()
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response: Response = await client.post(
        "psi/",
        params={"page_id": str(webpage_id)},
        headers=admin_token_headers,
        json=psi_base.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_create_website_pagespeedinsights_as_superuser_website_not_exists(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
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
        headers=admin_token_headers,
        json=psi_base.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_create_website_pagespeedinsights_as_superuser_webaite_page_not_exists(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    domain: str = "gcembed.getcommunity.com"
    is_secure: bool = random_boolean()
    w_data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=admin_token_headers,
        json=w_data,
    )
    assert 200 <= response.status_code < 300
    w_entry = response.json()
    a_website: WebsiteRead = WebsiteRead(**w_entry["website"])
    webpage_id = get_uuid_str()
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response: Response = await client.post(
        "psi/",
        params={"website_id": str(a_website.id), "page_id": str(webpage_id)},
        headers=admin_token_headers,
        json=psi_base.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_NOT_FOUND


async def test_create_website_pagespeedinsights_as_superuser_query_website_page_not_exists(  # noqa: E501
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    domain: str = "giftgurugal.com"
    is_secure: bool = random_boolean()
    w_data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=admin_token_headers,
        json=w_data,
    )
    assert 200 <= response.status_code < 300
    w_entry = response.json()
    a_website: WebsiteRead = WebsiteRead(**w_entry["website"])
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response: Response = await client.post(
        "psi/",
        params={"website_id": str(a_website.id)},
        headers=admin_token_headers,
        json=psi_base.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_NOT_FOUND

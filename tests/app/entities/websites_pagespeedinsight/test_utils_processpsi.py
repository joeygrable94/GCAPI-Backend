import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_pagespeedinsight.crud_utilities import (
    create_website_pagespeedinsights,
)
from app.entities.website_pagespeedinsight.schemas import WebsitePageSpeedInsightsBase
from app.utilities import get_uuid
from tests.utils.website_pages import create_random_website_page
from tests.utils.website_pagespeedinsights import generate_psi_base
from tests.utils.websites import create_random_website


@pytest.mark.anyio
async def test_create_website_pagespeedinsights(db_session: AsyncSession) -> None:
    website = await create_random_website(db_session)
    website_page = await create_random_website_page(db_session, website.id)
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response = await create_website_pagespeedinsights(  # type: ignore
        website_id=str(website.id),
        page_id=str(website_page.id),
        insights=psi_base,
    )
    assert response is None


@pytest.mark.anyio
async def test_create_website_pagespeedinsights_website_not_found(
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    website_page = await create_random_website_page(db_session, website_id)
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response = await create_website_pagespeedinsights(  # type: ignore
        website_id=str(website_id),
        page_id=str(website_page.id),
        insights=psi_base,
    )
    assert response is None


@pytest.mark.anyio
async def test_create_website_pagespeedinsights_website_page_not_found(
    db_session: AsyncSession,
) -> None:
    website = await create_random_website(db_session)
    website_page_id = get_uuid()
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=d_strategy
    )
    response = await create_website_pagespeedinsights(  # type: ignore
        website_id=str(website.id),
        page_id=str(website_page_id),
        insights=psi_base,
    )
    assert response is None

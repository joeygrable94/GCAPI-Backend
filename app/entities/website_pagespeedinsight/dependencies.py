from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.website_pagespeedinsight.crud import (
    WebsitePageSpeedInsights,
    WebsitePageSpeedInsightsRepository,
)
from app.utilities import parse_id


async def get_website_page_psi_or_404(
    db: AsyncDatabaseSession,
    psi_id: Any,
) -> WebsitePageSpeedInsights | None:
    """Parses uuid/int and fetches website page speed insights by id."""
    parsed_id: UUID = parse_id(psi_id)
    website_page_psi_repo: WebsitePageSpeedInsightsRepository = (
        WebsitePageSpeedInsightsRepository(session=db)
    )
    website_page_speed_insights: (
        WebsitePageSpeedInsights | None
    ) = await website_page_psi_repo.read(parsed_id)
    if website_page_speed_insights is None:
        raise EntityNotFound(
            entity_info="WebsitePageSpeedInsights {}".format(parsed_id)
        )
    return website_page_speed_insights


FetchWebPageSpeedInsightOr404 = Annotated[
    WebsitePageSpeedInsights, Depends(get_website_page_psi_or_404)
]

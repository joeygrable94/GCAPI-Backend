from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.db.session import get_db_session
from app.entities.api.errors import EntityNotFound
from app.entities.website.crud import WebsiteRepository
from app.entities.website.model import Website
from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.model import WebsitePage
from app.entities.website_pagespeedinsight.crud import (
    WebsitePageSpeedInsightsRepository,
)
from app.entities.website_pagespeedinsight.schemas import (
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
)
from app.utilities import parse_id


async def create_website_pagespeedinsights(
    website_id: str,
    page_id: str,
    insights: WebsitePageSpeedInsightsBase,
) -> None:
    try:
        website_uuid = parse_id(website_id)
        page_uuid = parse_id(page_id)
        session: AsyncSession
        website: Website | None
        website_page: WebsitePage | None
        # check if website exists
        async with get_db_session() as session:
            websites_repo: WebsiteRepository = WebsiteRepository(session)
            website = await websites_repo.read(
                entry_id=website_uuid,
            )
        if website is None:
            raise EntityNotFound(entity_info=f"Website {website_id}")
        # check if page exists
        async with get_db_session() as session:
            pages_repo: WebsitePageRepository = WebsitePageRepository(session)
            website_page = await pages_repo.read(
                entry_id=page_uuid,
            )
        if website_page is None:
            raise EntityNotFound(entity_info=f"WebsitePage {page_id}")
        # create website page speed insights
        async with get_db_session() as session:
            psi_repo: WebsitePageSpeedInsightsRepository = (
                WebsitePageSpeedInsightsRepository(session)
            )
            website_page_psi = await psi_repo.create(
                schema=WebsitePageSpeedInsightsCreate(
                    strategy=insights.strategy,
                    score_grade=insights.score_grade,
                    grade_data=insights.grade_data,
                    page_id=website_page.id,
                    website_id=website.id,
                )
            )
            logger.info(
                "Created Website Page Speed Insights for Website[{}] and Page[{}]".format(
                    website_page_psi.website_id, website_page_psi.page_id
                )
            )
    except Exception as e:
        logger.warning("Error Creating or Updating Website Page Speed Insights: %s" % e)
    finally:
        return None

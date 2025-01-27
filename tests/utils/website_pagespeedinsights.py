import json

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsitePageSpeedInsightsRepository
from app.models import Website, WebsitePageSpeedInsights
from app.schemas import (
    WebsitePageRead,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
    WebsitePageSpeedInsightsRead,
    WebsiteRead,
)
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website


def generate_psi_base(device_strategy: str = "mobile") -> WebsitePageSpeedInsightsBase:
    return WebsitePageSpeedInsightsBase(
        strategy=device_strategy,
        score_grade=0.5,
        grade_data=json.dumps(
            {
                "performance-score": {
                    "weight": 10,
                    "grade": 0.5,
                    "value": "50%",
                    "unit": "percent",
                },
                "first-contentful-paint": {
                    "weight": 10,
                    "grade": 0.5,
                    "value": 2500,
                    "unit": "milliseconds",
                },
                "longest-contentful-paint": {
                    "weight": 10,
                    "grade": 0.5,
                    "value": 2500,
                    "unit": "milliseconds",
                },
                "cumulative-layout-shift": {
                    "weight": 10,
                    "grade": 1.0,
                    "value": 0.0001,
                    "unit": "unitless",
                },
                "speed-index": {
                    "weight": 10,
                    "grade": 0.5,
                    "value": 2500.00,
                    "unit": "milliseconds",
                },
                "total-blocking-time": {
                    "weight": 10,
                    "grade": 0.5,
                    "value": 250.0,
                    "unit": "milliseconds",
                },
            }
        ),
    )


async def create_random_website_page_speed_insights(
    db_session: AsyncSession,
    website_id: UUID4 | None = None,
    page_id: UUID4 | None = None,
    device_strategy: str = "desktop",
) -> WebsitePageSpeedInsightsRead:
    repo: WebsitePageSpeedInsightsRepository
    repo = WebsitePageSpeedInsightsRepository(db_session)
    if website_id is None:
        website: Website | WebsiteRead = await create_random_website(db_session)
        website_id = website.id
    if page_id is None:
        website_page: WebsitePageRead = await create_random_website_page(db_session)
        page_id = website_page.id
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(
        device_strategy=device_strategy
    )
    web_page_psi: WebsitePageSpeedInsights = await repo.create(
        schema=WebsitePageSpeedInsightsCreate(
            page_id=page_id,
            website_id=website_id,
            **psi_base.model_dump(),
        )
    )
    return WebsitePageSpeedInsightsRead.model_validate(web_page_psi)

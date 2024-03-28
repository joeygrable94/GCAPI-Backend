from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

from app.crud import WebsitePageSpeedInsightsRepository
from app.models import WebsitePageSpeedInsights
from app.models.website import Website
from app.schemas import (
    WebsitePageRead,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
    WebsitePageSpeedInsightsRead,
    WebsiteRead,
)


def generate_psi_base(device_strategy: str = "mobile") -> WebsitePageSpeedInsightsBase:
    return WebsitePageSpeedInsightsBase(
        strategy=device_strategy,
        ps_weight=10,
        ps_grade=0.5,
        ps_value="50%",
        ps_unit="percent",
        fcp_weight=10,
        fcp_grade=0.5,
        fcp_value=2500,
        fcp_unit="milliseconds",
        lcp_weight=10,
        lcp_grade=0.5,
        lcp_value=2500,
        lcp_unit="milliseconds",
        cls_weight=10,
        cls_grade=1.0,
        cls_value=0.0001,
        cls_unit="unitless",
        si_weight=10,
        si_grade=0.5,
        si_value=2500.00,
        si_unit="milliseconds",
        tbt_weight=10,
        tbt_grade=0.5,
        tbt_value=250.0,
        tbt_unit="milliseconds",
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
    web_page_psi: WebsitePageSpeedInsights = await repo.create(
        schema=WebsitePageSpeedInsightsCreate(
            page_id=page_id,
            website_id=website_id,
            strategy=device_strategy,
            ps_weight=10,
            ps_grade=0.76,
            ps_value="76%",
            ps_unit="percent",
            fcp_weight=10,
            fcp_grade=0.67,
            fcp_value=2490,
            fcp_unit="milliseconds",
            lcp_weight=10,
            lcp_grade=0.88,
            lcp_value=2565,
            lcp_unit="milliseconds",
            cls_weight=10,
            cls_grade=1.0,
            cls_value=0.0007405598958333333,
            cls_unit="unitless",
            si_weight=10,
            si_grade=0.91,
            si_value=3280.8058937021365,
            si_unit="milliseconds",
            tbt_weight=10,
            tbt_grade=0.66,
            tbt_value=413.5,
            tbt_unit="milliseconds",
        )
    )
    return WebsitePageSpeedInsightsRead.model_validate(web_page_psi)

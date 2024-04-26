from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.core.utilities import fetch_url_status_code, parse_id
from app.crud import WebsitePageRepository
from app.db.session import get_db_session
from app.models import WebsitePage
from app.schemas import WebsiteMapPage, WebsitePageCreate, WebsitePageUpdate


async def create_or_update_website_page(
    website_id: str,
    sitemap_id: str,
    page: WebsiteMapPage,
) -> None:
    try:
        website_uuid = parse_id(website_id)
        sitemap_uuid = parse_id(sitemap_id)
        status_code: int = await fetch_url_status_code(page.url)
        session: AsyncSession
        website_page: WebsitePage | None
        pages_repo: WebsitePageRepository
        async with get_db_session() as session:
            pages_repo = WebsitePageRepository(session)
            website_page = await pages_repo.exists_by_two(
                field_name_a="url",
                field_value_a=page.url,
                field_name_b="website_id",
                field_value_b=website_uuid,
            )
            if website_page is not None:
                website_page = await pages_repo.update(
                    entry=website_page,
                    schema=WebsitePageUpdate(
                        url=page.url,
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                    ),
                )
            else:
                website_page = await pages_repo.create(
                    schema=WebsitePageCreate(
                        url=page.url,
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                        website_id=website_uuid,
                        sitemap_id=sitemap_uuid,
                    )
                )
    except Exception as e:  # pragma: no cover
        logger.warning("Error Creating or Updating Website Page: %s" % e)
    finally:
        return None

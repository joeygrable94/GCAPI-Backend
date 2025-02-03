import requests
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.db.session import get_db_session
from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.model import WebsitePage
from app.entities.website_page.schemas import (
    WebsitePageCreate,
    WebsitePageUpdate,
    WebsiteSitemapPage,
)
from app.utilities import parse_id


def fetch_url_status_code(url: str) -> int:
    resp = requests.head(url)
    return resp.status_code


async def create_or_update_website_page(
    website_id: str,
    page: WebsiteSitemapPage,
) -> None:
    try:
        website_uuid = parse_id(website_id)
        status_code: int = fetch_url_status_code(page.url)
        session: AsyncSession
        website_page: WebsitePage | None
        pages_repo: WebsitePageRepository
        async with get_db_session() as session:
            pages_repo = WebsitePageRepository(session)
            website_page = await pages_repo.exists_by_fields(
                {
                    "url": page.url,
                    "website_id": website_uuid,
                }
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
                    )
                )
    except Exception as e:  # pragma: no cover
        logger.warning("Error Creating or Updating Website Page: %s" % e)
    finally:
        return None

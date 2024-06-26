from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.core.utilities import parse_id
from app.crud import WebsiteMapRepository
from app.db.session import get_db_session
from app.models import WebsiteMap
from app.schemas import WebsiteMapCreate, WebsiteMapUpdate


async def create_or_update_website_map(
    website_id: str,
    sitemap_url: str,
) -> None:
    try:
        website_uuid = parse_id(website_id)
        session: AsyncSession
        sitemap: WebsiteMap | None
        async with get_db_session() as session:
            sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session)
            sitemap = await sitemap_repo.exists_by_fields(
                {
                    "url": sitemap_url,
                    "website_id": website_uuid,
                }
            )
            if sitemap is not None:
                sitemap = await sitemap_repo.update(
                    sitemap, WebsiteMapUpdate(url=sitemap_url)
                )
            else:
                sitemap = await sitemap_repo.create(
                    WebsiteMapCreate(url=sitemap_url, website_id=website_uuid)
                )
    except Exception as e:  # pragma: no cover
        logger.warning("Error Creating or Updating Website Sitemap: %s" % e)
    finally:
        return None

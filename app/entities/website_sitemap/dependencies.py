from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.website_sitemap.crud import WebsiteMap, WebsiteMapRepository
from app.utilities import parse_id


async def get_website_map_or_404(
    db: AsyncDatabaseSession,
    sitemap_id: Any,
) -> WebsiteMap:
    """Parses uuid/int and fetches website map by id."""
    parsed_id: UUID = parse_id(sitemap_id)
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    sitemap: WebsiteMap | None = await sitemap_repo.read(entry_id=parsed_id)
    if sitemap is None:
        raise EntityNotFound(entity_info="WebsiteMap {}".format(parsed_id))
    return sitemap


FetchSitemapOr404 = Annotated[WebsiteMap, Depends(get_website_map_or_404)]

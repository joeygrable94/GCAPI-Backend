from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.website_page.crud import WebsitePage, WebsitePageRepository
from app.utilities import parse_id


async def get_website_page_or_404(
    db: AsyncDatabaseSession,
    page_id: Any,
) -> WebsitePage | None:
    """Parses uuid/int and fetches website page by id."""
    parsed_id: UUID = parse_id(page_id)
    website_page_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    website_page: WebsitePage | None = await website_page_repo.read(entry_id=parsed_id)
    if website_page is None:
        raise EntityNotFound(entity_info="WebsitePage {}".format(parsed_id))
    return website_page


FetchWebPageOr404 = Annotated[WebsitePage, Depends(get_website_page_or_404)]

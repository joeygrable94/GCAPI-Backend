from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.website.crud import Website, WebsiteRepository
from app.utilities import parse_id


async def get_website_or_404(
    db: AsyncDatabaseSession,
    website_id: Any,
) -> Website | None:
    """Parses uuid/int and fetches website by id."""
    parsed_id: UUID = parse_id(website_id)
    website_repo: WebsiteRepository = WebsiteRepository(session=db)
    website: Website | None = await website_repo.read(entry_id=parsed_id)
    if website is None:
        raise EntityNotFound(entity_info="Website {}".format(parsed_id))
    return website


FetchWebsiteOr404 = Annotated[Website, Depends(get_website_or_404)]

from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.tracking_link.crud import TrackingLink, TrackingLinkRepository
from app.utilities import parse_id


async def get_tracking_link_or_404(
    db: AsyncDatabaseSession,
    tracking_link_id: Any,
) -> TrackingLink | None:
    """Parses uuid/int and fetches tracking_link by id."""
    parsed_id: UUID = parse_id(tracking_link_id)
    link_repo: TrackingLinkRepository = TrackingLinkRepository(session=db)
    link: TrackingLink | None = await link_repo.read(entry_id=parsed_id)
    if link is None:
        raise EntityNotFound(entity_info="TrackingLink {}".format(parsed_id))
    return link


FetchTrackingLinkOr404 = Annotated[TrackingLink, Depends(get_tracking_link_or_404)]

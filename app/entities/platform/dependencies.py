from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.core_organization.crud import Organization
from app.entities.platform.crud import Platform, PlatformRepository
from app.utilities import parse_id


async def get_platform_404(
    db: AsyncDatabaseSession,
    platform_id: Any,
) -> Platform | None:
    """Parses uuid/int and fetches platform by id."""
    parsed_id: UUID = parse_id(platform_id)
    platform_repo: PlatformRepository = PlatformRepository(session=db)
    platform: Platform | None = await platform_repo.read(parsed_id)
    if platform is None:
        raise EntityNotFound(entity_info="Platform {}".format(parsed_id))
    return platform


FetchPlatformOr404 = Annotated[Organization, Depends(get_platform_404)]

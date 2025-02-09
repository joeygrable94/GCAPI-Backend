from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.core_organization.crud import Organization, OrganizationRepository
from app.entities.core_organization.errors import OrganizationNotFound
from app.utilities import parse_id


async def get_organization_or_404(
    db: AsyncDatabaseSession,
    organization_id: Any,
) -> Organization | None:
    """Parses uuid/int and fetches organization by id."""
    parsed_id: UUID = parse_id(organization_id)
    organization_repo: OrganizationRepository = OrganizationRepository(session=db)
    organization: Organization | None = await organization_repo.read(entry_id=parsed_id)
    if organization is None:
        raise OrganizationNotFound()
    return organization


FetchOrganizationOr404 = Annotated[Organization, Depends(get_organization_or_404)]

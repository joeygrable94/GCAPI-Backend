from app.core.crud import BaseRepository
from app.entities.organization_platform.model import OrganizationPlatform
from app.entities.organization_platform.schemas import (
    OrganizationPlatformCreate,
    OrganizationPlatformRead,
    OrganizationPlatformUpdate,
)


class OrganizationPlatformRepository(
    BaseRepository[
        OrganizationPlatformCreate,
        OrganizationPlatformRead,
        OrganizationPlatformUpdate,
        OrganizationPlatform,
    ]
):
    @property
    def _table(self) -> OrganizationPlatform:
        return OrganizationPlatform

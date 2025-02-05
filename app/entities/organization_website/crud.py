from app.core.crud import BaseRepository
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.organization_website.schemas import (
    OrganizationWebsiteCreate,
    OrganizationWebsiteRead,
    OrganizationWebsiteUpdate,
)


class OrganizationWebsiteRepository(
    BaseRepository[
        OrganizationWebsiteCreate,
        OrganizationWebsiteRead,
        OrganizationWebsiteUpdate,
        OrganizationWebsite,
    ]
):
    @property
    def _table(self) -> OrganizationWebsite:
        return OrganizationWebsite

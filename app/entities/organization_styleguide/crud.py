from app.core.crud import BaseRepository
from app.entities.organization_styleguide.model import OrganizationStyleguide
from app.entities.organization_styleguide.schemas import (
    OrganizationStyleguideCreate,
    OrganizationStyleguideRead,
    OrganizationStyleguideUpdate,
)


class OrganizationStyleguideRepository(
    BaseRepository[
        OrganizationStyleguideCreate,
        OrganizationStyleguideRead,
        OrganizationStyleguideUpdate,
        OrganizationStyleguide,
    ]
):
    @property
    def _table(self) -> OrganizationStyleguide:
        return OrganizationStyleguide

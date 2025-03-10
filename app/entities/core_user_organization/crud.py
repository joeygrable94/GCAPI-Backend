from app.core.crud import BaseRepository
from app.entities.core_user_organization.model import UserOrganization
from app.entities.core_user_organization.schemas import (
    UserOrganizationCreate,
    UserOrganizationRead,
    UserOrganizationUpdate,
)


class UserOrganizationRepository(
    BaseRepository[
        UserOrganizationCreate,
        UserOrganizationRead,
        UserOrganizationUpdate,
        UserOrganization,
    ]
):
    @property
    def _table(self) -> UserOrganization:
        return UserOrganization

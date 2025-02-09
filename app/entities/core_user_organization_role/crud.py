from app.core.crud import BaseRepository
from app.entities.core_user_organization_role.model import UserOrganizationRole
from app.entities.core_user_organization_role.schemas import (
    UserOrganizationRoleCreate,
    UserOrganizationRoleRead,
    UserOrganizationRoleUpdate,
)


class UserOrganizationRoleRepository(
    BaseRepository[
        UserOrganizationRoleCreate,
        UserOrganizationRoleRead,
        UserOrganizationRoleUpdate,
        UserOrganizationRole,
    ]
):
    @property
    def _table(self) -> UserOrganizationRole:
        return UserOrganizationRole

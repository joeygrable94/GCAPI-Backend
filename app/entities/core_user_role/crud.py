from app.core.crud import BaseRepository
from app.entities.core_user_role.model import UserRole
from app.entities.core_user_role.schemas import (
    UserRoleCreate,
    UserRoleRead,
    UserRoleUpdate,
)


class UserRoleRepository(
    BaseRepository[
        UserRoleCreate,
        UserRoleRead,
        UserRoleUpdate,
        UserRole,
    ]
):
    @property
    def _table(self) -> UserRole:
        return UserRole

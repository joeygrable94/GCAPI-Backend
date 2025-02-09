from app.core.crud import BaseRepository
from app.entities.core_user_permission.model import UserPermission
from app.entities.core_user_permission.schemas import (
    UserPermissionCreate,
    UserPermissionRead,
    UserPermissionUpdate,
)


class UserPermissionRepository(
    BaseRepository[
        UserPermissionCreate,
        UserPermissionRead,
        UserPermissionUpdate,
        UserPermission,
    ]
):
    @property
    def _table(self) -> UserPermission:
        return UserPermission

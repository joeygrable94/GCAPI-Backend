from app.core.crud import BaseRepository
from app.entities.core_role_permission.model import RolePermission
from app.entities.core_role_permission.schemas import (
    RolePermissionCreate,
    RolePermissionRead,
    RolePermissionUpdate,
)


class RolePermissionRepository(
    BaseRepository[
        RolePermissionCreate,
        RolePermissionRead,
        RolePermissionUpdate,
        RolePermission,
    ]
):
    @property
    def _table(self) -> RolePermission:
        return RolePermission

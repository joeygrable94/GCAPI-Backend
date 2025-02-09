from app.core.crud import BaseRepository
from app.entities.core_permission.model import Permission
from app.entities.core_permission.schemas import (
    PermissionCreate,
    PermissionRead,
    PermissionUpdate,
)


class PermissionRepository(
    BaseRepository[PermissionCreate, PermissionRead, PermissionUpdate, Permission]
):
    @property
    def _table(self) -> Permission:
        return Permission

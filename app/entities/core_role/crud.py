from app.core.crud import BaseRepository
from app.entities.core_role.model import Role
from app.entities.core_role.schemas import RoleCreate, RoleRead, RoleUpdate


class RoleRepository(BaseRepository[RoleCreate, RoleRead, RoleUpdate, Role]):
    @property
    def _table(self) -> Role:
        return Role

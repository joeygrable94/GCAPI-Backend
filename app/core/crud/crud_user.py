from app.core.crud.base import CRUDBase
from app.core.models.user import User
from app.core.schemas.user import UserCreate, UserUpdate

# Modular method
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass

user = CRUDUser(User)

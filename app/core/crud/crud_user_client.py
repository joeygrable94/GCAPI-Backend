from app.core.crud.base import CRUDBase
from app.core.models.user_client import UserClient
from app.core.schemas.user_client import UserClientCreate, UserClientUpdate

# Modular method
class CRUDUserClient(CRUDBase[UserClient, UserClientCreate, UserClientUpdate]):
    pass

user_client = CRUDUserClient(UserClient)

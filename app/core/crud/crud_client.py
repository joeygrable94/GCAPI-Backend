from app.core.crud.base import CRUDBase
from app.core.models.client import Client
from app.core.schemas.client import ClientCreate, ClientUpdate

# Modular method
class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    pass

client = CRUDClient(Client)

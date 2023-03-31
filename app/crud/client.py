from typing import Type

from app.crud.base import BaseRepository
from app.models import Client
from app.schemas import ClientCreate, ClientRead, ClientUpdate


class ClientRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _table(self) -> Type[Client]:  # type: ignore
        return Client

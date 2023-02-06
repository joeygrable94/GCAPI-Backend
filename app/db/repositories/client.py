from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate
from app.db.tables import Client


class ClientRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _table(self) -> Type[Client]:  # type: ignore
        return Client

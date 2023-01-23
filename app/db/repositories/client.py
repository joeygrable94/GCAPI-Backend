from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate
from app.db.tables import Client


class ClientsRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _schema_read(self) -> Type[ClientRead]:  # type: ignore
        return ClientRead

    @property
    def _table(self) -> Type[Client]:  # type: ignore
        return Client

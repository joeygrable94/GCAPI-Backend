from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate
from app.db.tables import Client


class ClientsRepository(BaseRepository[ClientCreate, ClientUpdate, ClientRead, Client]):
    @property
    def _table(self) -> Type[Client]:
        return Client

    @property
    def _schema_create(self) -> Type[ClientCreate]:
        return ClientCreate

    @property
    def _schema_update(self) -> Type[ClientUpdate]:
        return ClientUpdate

    @property
    def _schema_read(self) -> Type[ClientRead]:
        return ClientRead

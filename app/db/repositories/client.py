from typing import List, Type
from pydantic import UUID4

from sqlalchemy import select as sql_select

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate
from app.db.tables import Client
from .base import PER_PAGE_MAX_COUNT


class ClientsRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _schema_create(self) -> Type[ClientCreate]:
        return ClientCreate

    @property
    def _schema_read(self) -> Type[ClientRead]:
        return ClientRead

    @property
    def _schema_update(self) -> Type[ClientUpdate]:
        return ClientUpdate

    @property
    def _table(self) -> Type[Client]:
        return Client

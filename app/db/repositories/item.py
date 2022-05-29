from typing import Type

from pydantic import UUID4

from app.db.repositories.base import BaseRepository
from app.db.tables import Item
from app.db.schemas import ItemCreate, ItemRead, ItemUpdate


class ItemsRepository(BaseRepository[ItemCreate, ItemUpdate, ItemRead, Item]):

    @property
    def _table(self) -> Type[Item]:
        return Item

    @property
    def _schema_create(self) -> Type[ItemCreate]:
        return ItemCreate

    @property
    def _schema_update(self) -> Type[ItemUpdate]:
        return ItemUpdate

    @property
    def _schema_read(self) -> Type[ItemRead]:
        return ItemRead

from datetime import datetime
from typing import Optional

from pydantic import UUID4
from app.db.schemas.base import BaseSchema


class ItemBase(BaseSchema):
    title: str
    content: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: Optional[str]
    content: Optional[str]


class ItemRead(ItemBase):
    id: UUID4
    user_id: Optional[UUID4]

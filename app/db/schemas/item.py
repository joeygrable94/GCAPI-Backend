from typing import Optional

from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class ItemBase(BaseSchema):
    title: Optional[str] = ""
    content: Optional[str] = ""
    user_id: Optional[UUID4]


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: Optional[str]
    content: Optional[str]


class ItemRead(ItemBase):
    id: UUID4

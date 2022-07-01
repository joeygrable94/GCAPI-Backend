from typing import Optional

from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class ItemBase(BaseSchema):
    title: str = ""
    content: str = ""


class ItemCreate(ItemBase):
    user_id: Optional[UUID4]


class ItemUpdate(ItemBase):
    user_id: Optional[UUID4]


class ItemRead(ItemBase):
    id: UUID4
    user_id: Optional[UUID4]

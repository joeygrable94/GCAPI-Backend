from typing import Optional

from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class ClientBase(BaseSchema):
    title: Optional[str] = ""
    content: Optional[str] = ""


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    title: Optional[str]
    content: Optional[str]


class ClientRead(ClientBase):
    id: UUID4

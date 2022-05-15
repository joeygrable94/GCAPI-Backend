from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class ClientBase(BaseModel):
    title: str
    content: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientInDBBase(ClientBase):
    id: UUID4
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Client(ClientInDBBase):
    pass


class ClientInDB(ClientInDBBase):
    pass

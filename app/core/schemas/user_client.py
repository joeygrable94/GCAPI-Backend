from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class UserClientBase(BaseModel):
    scope: str
    user_id: UUID4
    client_id: UUID4


class UserClientCreate(UserClientBase):
    pass


class UserClientUpdate(UserClientBase):
    pass


class UserClientInDBBase(UserClientBase):
    id: UUID4
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class UserClient(UserClientInDBBase):
    pass


class UserClientInDB(UserClientInDBBase):
    pass

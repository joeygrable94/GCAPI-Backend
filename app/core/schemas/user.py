from datetime import date, datetime
from typing import Optional
import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    created_on: Optional[datetime]
    updated_on: Optional[datetime]


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

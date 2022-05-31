import uuid

from fastapi_users import schemas
from pydantic import UUID4


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: UUID4

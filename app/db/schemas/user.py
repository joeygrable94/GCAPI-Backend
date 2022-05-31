import uuid

from fastapi_users import schemas
from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class UserCreate(BaseSchema, schemas.BaseUserCreate):
    pass


class UserUpdate(BaseSchema, schemas.BaseUserUpdate):
    pass


class UserRead(BaseSchema, schemas.BaseUser[uuid.UUID]):
    id: UUID4

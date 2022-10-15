from typing import Optional

from pydantic import EmailStr

from app.db.schemas.base import BaseSchema, BaseSchemaRead


class UserInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(BaseSchema):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseSchema):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserRead(BaseSchemaRead):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool

from typing import Generic, Optional, TypeVar
import uuid

from pydantic import BaseModel, EmailStr
from app.core.user_manager.types import ID
from app.core.user_manager.generics import UUID_ID


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class BaseUser(Generic[ID], CreateUpdateDictModel):
    """Base User model."""

    id: ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(CreateUpdateDictModel):
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserRead(BaseUser[uuid.UUID]):
    id: UUID_ID


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=UserCreate)
UU = TypeVar("UU", bound=UserUpdate)
UR = TypeVar("UR", bound=UserRead)

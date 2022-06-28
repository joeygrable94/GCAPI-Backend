from typing import Optional, TypeVar

from pydantic import UUID4, EmailStr

from app.core.user_manager.schemas import BaseUser, CreateUpdateDictModel
from app.db.utilities import UUID_ID


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


class UserRead(BaseUser[UUID_ID]):
    id: UUID4


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=UserCreate)
UU = TypeVar("UU", bound=UserUpdate)
UR = TypeVar("UR", bound=UserRead)

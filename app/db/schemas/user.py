from typing import Any, Dict, Generic, Optional, Protocol, TypeVar

from pydantic import UUID4, EmailStr, BaseModel

from app.db.schemas.base import BaseSchema


ID = TypeVar("ID")


class UserProtocol(Protocol[ID]):
    """User protocol the ORM model should follow."""

    id: ID
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...  # pragma: no cover


UP = TypeVar("UP", bound=UserProtocol)


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self) -> Dict:
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
            },
        )

    def create_update_dict_superuser(self) -> Dict:
        return self.dict(exclude_unset=True, exclude={"id"})


class BaseUser(Generic[ID], CreateUpdateDictModel):
    """Base User model."""

    id: ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseSchema, CreateUpdateDictModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseSchema, CreateUpdateDictModel):
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserRead(BaseUser[UUID4], BaseSchema):
    id: UUID4


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=UserCreate)
UU = TypeVar("UU", bound=UserUpdate)
UR = TypeVar("UR", bound=UserRead)

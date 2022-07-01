from typing import Dict, Generic

from pydantic import BaseModel, EmailStr

from app.core.user_manager.types import ID


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

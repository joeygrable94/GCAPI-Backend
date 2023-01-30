from typing import Any, List, Optional, Tuple

from fastapi_permissions import Allow
from pydantic import UUID4, validator

from app.db.schemas.base import BaseSchema, BaseSchemaRead


# ACL
class ClientACL(BaseSchema):
    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        return [
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
            (Allow, "role:user", "list"),
            (Allow, "role:user", "create"),
            (Allow, "role:user", "read"),
        ]


# validators
class ValidateClientTitleRequired(BaseSchema):
    title: str

    @validator("title")
    def limits_title(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("title must contain 5 or more characters")
        if len(v) > 96:
            raise ValueError("title must contain less than 96 characters")
        return v


class ValidateClientTitleOptional(BaseSchema):
    title: Optional[str]

    @validator("title")
    def limits_title(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 5:
            raise ValueError("title must contain 5 or more characters")
        if v and len(v) > 96:
            raise ValueError("title must contain less than 96 characters")
        return v


class ValidateClientContentOptional(BaseSchema):
    content: Optional[str]

    @validator("content")
    def limits_content(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 255:
            raise ValueError("content must contain less than 255 characters")
        return v


class ClientBase(ValidateClientTitleRequired, ValidateClientContentOptional):
    title: str
    content: Optional[str]


class ClientCreate(ClientBase):
    title: str
    content: Optional[str]


class ClientUpdate(ValidateClientTitleOptional, ValidateClientContentOptional):
    title: Optional[str]
    content: Optional[str]


class ClientRead(ClientACL, ClientBase, BaseSchemaRead):
    id: UUID4

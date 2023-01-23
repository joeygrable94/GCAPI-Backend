from typing import Any, List, Optional, Tuple

from fastapi_permissions import Allow
from pydantic import UUID4, Field

from app.db.schemas.base import BaseSchema, BaseSchemaRead


class WebsiteBase(BaseSchema):
    domain: str = Field("", max_length=255)
    is_secure: bool = False


class WebsiteCreate(BaseSchema):
    domain: str = Field("", max_length=255)
    is_secure: Optional[bool] = False


class WebsiteUpdate(BaseSchema):
    domain: Optional[str] = Field(None, max_length=255)
    is_secure: Optional[bool] = False


class WebsiteRead(WebsiteBase, BaseSchemaRead):
    id: UUID4

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

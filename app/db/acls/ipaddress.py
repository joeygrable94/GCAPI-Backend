from typing import Any, List, Tuple

from fastapi_permissions import Allow
from pydantic import BaseModel

from app.core.config import settings


class IpAddressACL(BaseModel):
    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        return [
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
            (Allow, f"user:{settings.FIRST_SUPERUSER}", "super"),
        ]

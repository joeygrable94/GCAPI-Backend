from typing import Any, List, Tuple

from fastapi_permissions import Allow, Authenticated
from pydantic import BaseModel

from app.core.config import settings


class AccessTokenACL(BaseModel):
    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        return [
            (Allow, Authenticated, "use"),
            (Allow, f"user:{settings.FIRST_SUPERUSER}", "super"),
        ]

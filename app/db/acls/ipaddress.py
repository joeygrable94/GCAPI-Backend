from typing import Any, List, Tuple

from fastapi_permissions import Allow  # type: ignore
from pydantic import BaseModel


class IpaddressACL(BaseModel):
    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        return [  # pragma: no cover
            (Allow, "access:admin", "access"),
            (Allow, "access:client", "access"),
            (Allow, "access:user", "access"),
        ]

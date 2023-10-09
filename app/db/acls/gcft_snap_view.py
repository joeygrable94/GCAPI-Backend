from typing import Any, List, Tuple

from fastapi_permissions import Allow  # type: ignore
from pydantic import BaseModel


class GcftSnapViewACL(BaseModel):
    __acl__: List[Tuple[Any, Any, Any]] = [  # pragma: no cover
        (Allow, "access:admin", "access"),
        (Allow, "access:client", "access"),
        (Allow, "access:user", "access"),
    ]
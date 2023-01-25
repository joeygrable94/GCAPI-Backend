from typing import Any, List, Tuple

from fastapi_permissions import Allow
from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class UserClientBase(BaseSchema):
    user_id: UUID4
    client_id: UUID4


class UserClientCreate(UserClientBase):
    pass


class UserClientUpdate(UserClientBase):
    pass


class UserClientRead(UserClientBase):
    id: UUID4

    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        return [
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
        ]
from typing import Any, List, Tuple

from fastapi_permissions import Allow
from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class ClientWebsiteBase(BaseSchema):
    client_id: UUID4
    website_id: UUID4


class ClientWebsiteCreate(ClientWebsiteBase):
    pass


class ClientWebsiteUpdate(ClientWebsiteBase):
    pass


class ClientWebsiteRead(ClientWebsiteBase):
    id: UUID4

    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        return [
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
        ]

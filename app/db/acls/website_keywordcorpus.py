from typing import Any, List, Tuple

from fastapi_permissions import Allow
from pydantic import BaseModel


class WebsiteKeywordCorpusACL(BaseModel):
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
            (Allow, "role:user", "update"),
            (Allow, "role:user", "delete"),
        ]

from typing import Any, List, Tuple

from fastapi_permissions import Allow, Authenticated
from pydantic import BaseModel

from app.core.config import settings


class UserACL(BaseModel):
    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        """Defines who can do what.

        Returns a list of tuples (1, 2, 3):
            1. access level:
                Allow
                Deny
            2. principal identifier:
                Everyone
                Authenticated
                role:admin
                role:user
            3. permissions:
                super
                self
                list
                create
                read
                update
                delete

        If a role is not listed (like "role:user") the access will be
        automatically denied, as if (Deny, Everyone, All) is appended.
        """
        return [
            (Allow, Authenticated, "self"),
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
            (Allow, f"user:{settings.FIRST_SUPERUSER}", "super"),
            (Allow, f"user:{self.email}", "self"),  # type: ignore
        ]

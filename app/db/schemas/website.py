from typing import Any, List, Optional, Tuple

from fastapi_permissions import Allow
from pydantic import UUID4, validator

from app.core.utilities import domain_name_regex
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# ACL
class WebsiteACL(BaseSchema):
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
class ValidateWebsiteDomainRequired(BaseSchema):
    domain: str

    @validator("domain")
    def limits_domain(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("domain must contain 5 or more characters")
        if len(v) > 255:
            raise ValueError("domain must contain less than 255 characters")
        if not domain_name_regex.search(v):
            raise ValueError(
                "invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
            )
        return v


class ValidateWebsiteDomainOptional(BaseSchema):
    domain: Optional[str]

    @validator("domain")
    def limits_domain(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 5:
            raise ValueError("domain must contain 5 or more characters")
        if v and len(v) > 255:
            raise ValueError("domain must contain less than 255 characters")
        if v and not domain_name_regex.search(v):
            raise ValueError(
                "invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
            )
        return v


class WebsiteBase(ValidateWebsiteDomainRequired):
    domain: str
    is_secure: bool = False


class WebsiteCreate(ValidateWebsiteDomainRequired):
    domain: str
    is_secure: Optional[bool] = False


class WebsiteUpdate(ValidateWebsiteDomainOptional):
    domain: Optional[str]
    is_secure: Optional[bool] = False


class WebsiteRead(WebsiteACL, WebsiteBase, BaseSchemaRead):
    id: UUID4

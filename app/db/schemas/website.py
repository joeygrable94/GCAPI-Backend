from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, BaseModel, validator

from app.core.utilities import domain_name_regex
from app.db.acls.website import WebsiteACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


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


# schemas
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


# tasks
class WebsiteCreateProcessing(BaseModel):
    website: WebsiteRead
    sitemap_task_id: UUID4


# relationships
class WebsiteReadRelations(WebsiteRead):
    clients: Optional[List["ClientRead"]] = []
    sitemaps: Optional[List["WebsiteMapRead"]] = []
    pages: Optional[List["WebsitePageRead"]] = []


# import and update pydantic relationship refs
from app.db.schemas.client import ClientRead  # noqa: E402
from app.db.schemas.website_map import WebsiteMapRead  # noqa: E402
from app.db.schemas.website_page import WebsitePageRead  # noqa: E402

WebsiteReadRelations.update_forward_refs()

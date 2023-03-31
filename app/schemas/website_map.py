from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, validator

from app.db.acls import WebsiteMapACL
from app.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateWebsiteMapUrlRequired(BaseSchema):
    url: str

    @validator("url")
    def limits_url(cls, v: str) -> str:  # pragma: no cover
        if len(v) <= 0:
            raise ValueError("url text is required")
        if len(v) > 5000:
            raise ValueError("url must contain less than 5000 characters")
        return v


class ValidateWebsiteMapUrlOptional(BaseSchema):
    url: Optional[str]

    @validator("url")
    def limits_url(cls, v: Optional[str]) -> Optional[str]:  # pragma: no cover
        if v and len(v) <= 0:
            raise ValueError("url text is required")
        if v and len(v) > 5000:
            raise ValueError("url must contain less than 5000 characters")
        return v


# schemas
class WebsiteMapBase(BaseSchema):
    pass


class WebsiteMapCreate(
    ValidateWebsiteMapUrlRequired,
    WebsiteMapBase,
):
    url: str
    website_id: UUID4


class WebsiteMapUpdate(
    ValidateWebsiteMapUrlOptional,
    WebsiteMapBase,
):
    url: Optional[str]


class WebsiteMapRead(WebsiteMapACL, WebsiteMapCreate, WebsiteMapBase, BaseSchemaRead):
    id: UUID4


# relationships
class WebsiteMapReadRelations(WebsiteMapRead):
    pages: Optional[List["WebsitePageRead"]] = []


# import and update pydantic relationship refs
from app.schemas.website_page import WebsitePageRead  # noqa: E402

WebsiteMapReadRelations.update_forward_refs()

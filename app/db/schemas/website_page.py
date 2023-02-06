from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, validator

from app.db.acls.website_page import WebsitePageACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateWebsitePagePathRequired(BaseSchema):
    path: str

    @validator("path")
    def limits_path(cls, v: str) -> str:
        if len(v) <= 0:
            raise ValueError("path text is required")
        if len(v) > 4096:
            raise ValueError("path must contain less than 4096 characters")
        return v


class ValidateWebsitePagePathOptional(BaseSchema):
    path: Optional[str]

    @validator("path")
    def limits_path(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) <= 0:
            raise ValueError("path text is required")
        if v and len(v) > 4096:
            raise ValueError("path must contain less than 4096 characters")
        return v


# schemas
class WebsitePageBase(ValidateWebsitePagePathRequired, BaseSchema):
    path: str
    status: int
    website_id: UUID4
    sitemap_id: Optional[UUID4]


class WebsitePageCreate(WebsitePageBase):
    pass


class WebsitePageUpdate(ValidateWebsitePagePathOptional, BaseSchema):
    path: Optional[str]
    status: Optional[int]
    website_id: Optional[UUID4]
    sitemap_id: Optional[UUID4]


class WebsitePageRead(WebsitePageACL, WebsitePageBase, BaseSchemaRead):
    id: UUID4


# relationships
class WebsitePageReadRelations(WebsitePageRead):
    keywordcorpus: Optional[List["WebsiteKeywordCorpusRead"]] = []
    pagespeedinsights: Optional[List["WebsitePageSpeedInsightsRead"]] = []


# import and update pydantic relationship refs
from app.db.schemas.website_keywordcorpus import WebsiteKeywordCorpusRead  # noqa: E402
from app.db.schemas.website_pagespeedinsights import (  # noqa: E402
    WebsitePageSpeedInsightsRead,
)

WebsitePageReadRelations.update_forward_refs()

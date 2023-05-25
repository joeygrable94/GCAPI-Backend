from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import UUID4, BaseModel, validator
from usp.objects.page import SitemapPageChangeFrequency  # type: ignore

from app.db.acls import WebsitePageACL
from app.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateWebsitePageUrlRequired(BaseSchema):
    url: str

    @validator("url")
    def limits_url(cls, v: str) -> str:  # pragma: no cover
        if len(v) <= 0:
            raise ValueError("url text is required")
        if len(v) > 5000:
            raise ValueError("url must contain less than 5000 characters")
        return v


class ValidateWebsitePageUrlOptional(BaseSchema):
    url: Optional[str]

    @validator("url")
    def limits_url(cls, v: Optional[str]) -> Optional[str]:  # pragma: no cover
        if v and len(v) <= 0:
            raise ValueError("url text is required")
        if v and len(v) > 5000:
            raise ValueError("url must contain less than 5000 characters")
        return v


# schemas
class WebsitePageBase(ValidateWebsitePageUrlRequired, BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: Optional[datetime]
    change_frequency: Optional[SitemapPageChangeFrequency]
    website_id: UUID4
    sitemap_id: Optional[UUID4]


class WebsitePageCreate(WebsitePageBase):
    pass


class WebsitePageUpdate(ValidateWebsitePageUrlOptional, BaseSchema):
    url: Optional[str]
    status: Optional[int]
    priority: Optional[Union[float, Decimal]]
    last_modified: Optional[datetime]
    change_frequency: Optional[SitemapPageChangeFrequency]
    sitemap_id: Optional[UUID4]


class WebsitePageRead(WebsitePageACL, WebsitePageBase, BaseSchemaRead):
    id: UUID4


# task
class WebsitePageFetchPSIProcessing(BaseModel):
    page: WebsitePageRead
    mobile_task_id: UUID4
    desktop_task_id: UUID4


# relationships
class WebsitePageReadRelations(WebsitePageRead):
    keywordcorpus: Optional[List["WebsiteKeywordCorpusRead"]] = []
    pagespeedinsights: Optional[List["WebsitePageSpeedInsightsRead"]] = []


# import and update pydantic relationship refs
from app.schemas.website_keywordcorpus import WebsiteKeywordCorpusRead  # noqa: E402
from app.schemas.website_pagespeedinsights import (  # noqa: E402
    WebsitePageSpeedInsightsRead,
)

WebsitePageReadRelations.update_forward_refs()

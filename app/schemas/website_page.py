from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import UUID4, BaseModel
from usp.objects.page import SitemapPageChangeFrequency  # type: ignore

from app.db.acls import WebsitePageACL
from app.db.validators import ValidateSchemaUrlOptional, ValidateSchemaUrlRequired
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class WebsitePageBase(BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: Optional[datetime]
    change_frequency: Optional[SitemapPageChangeFrequency]
    website_id: UUID4
    sitemap_id: Optional[UUID4]


class WebsitePageCreate(ValidateSchemaUrlRequired, WebsitePageBase):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: Optional[datetime]
    change_frequency: Optional[SitemapPageChangeFrequency]
    website_id: UUID4
    sitemap_id: Optional[UUID4]


class WebsitePageUpdate(ValidateSchemaUrlOptional, BaseSchema):
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

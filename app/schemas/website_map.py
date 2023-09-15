from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel, validator
from usp.objects.page import SITEMAP_PAGE_DEFAULT_PRIORITY  # type: ignore
from usp.objects.page import SitemapPageChangeFrequency

from app.db.acls import WebsiteMapACL
from app.schemas.base import BaseSchema, BaseSchemaRead


# generics
class GoogleNewsStory(BaseModel):
    title: str
    publish_date: datetime
    publication_name: Optional[str] = None
    publication_language: Optional[str] = None
    access: Optional[str] = None
    genres: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    stock_tickers: Optional[List[str]] = None


class WebsiteMapPage(BaseModel):
    url: str
    priority: Decimal = SITEMAP_PAGE_DEFAULT_PRIORITY
    last_modified: Optional[datetime] = None
    change_frequency: Optional[SitemapPageChangeFrequency] = None
    news_story: Optional[GoogleNewsStory] = None


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


# tasks
class WebsiteMapProcessing(WebsiteMapCreate):
    task_id: str


# relationships
class WebsiteMapReadRelations(WebsiteMapRead):
    pages: Optional[List["WebsitePageRead"]] = []


# import and update pydantic relationship refs
from app.schemas.website_page import WebsitePageRead  # noqa: E402

WebsiteMapReadRelations.update_forward_refs()

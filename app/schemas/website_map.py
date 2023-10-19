from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel
from usp.objects.page import SITEMAP_PAGE_DEFAULT_PRIORITY  # type: ignore
from usp.objects.page import SitemapPageChangeFrequency

from app.db.validators import ValidateSchemaUrlOptional, ValidateSchemaUrlRequired
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


# schemas
class WebsiteMapBase(BaseSchema):
    url: str
    is_active: bool
    website_id: UUID4


class WebsiteMapCreate(
    ValidateSchemaUrlRequired,
    WebsiteMapBase,
):
    url: str
    is_active: bool = True
    website_id: UUID4


class WebsiteMapUpdate(
    ValidateSchemaUrlOptional,
    BaseSchema,
):
    url: Optional[str] = None
    is_active: Optional[bool] = None


class WebsiteMapRead(WebsiteMapBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsiteMapProcessing(BaseSchema):
    url: str
    website_id: UUID4
    task_id: str


class WebsiteMapProcessedResult(WebsiteMapCreate):
    website_map_pages: List[WebsiteMapPage]

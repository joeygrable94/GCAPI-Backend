from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import UUID4, BaseModel
from usp.objects.page import SITEMAP_PAGE_DEFAULT_PRIORITY  # type: ignore
from usp.objects.page import SitemapPageChangeFrequency

from app.db.acls import WebsiteMapACL
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
    pass


class WebsiteMapCreate(
    ValidateSchemaUrlRequired,
    WebsiteMapBase,
):
    url: str
    website_id: UUID4


class WebsiteMapUpdate(
    ValidateSchemaUrlOptional,
    WebsiteMapBase,
):
    url: Optional[str] = None


class WebsiteMapRead(WebsiteMapACL, WebsiteMapCreate, WebsiteMapBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsiteMapProcessing(WebsiteMapCreate):
    task_id: str


class WebsiteMapProcessedResult(WebsiteMapCreate):
    website_map_pages: List[WebsiteMapPage]


# relationships
class WebsiteMapReadRelations(WebsiteMapRead):
    pages: Optional[List["WebsitePageRead"]] = []


# import and update pydantic relationship refs
from app.schemas.website_page import WebsitePageRead  # noqa: E402

WebsiteMapReadRelations.model_rebuild()

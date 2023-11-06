from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import UUID4, BaseModel, field_validator
from usp.objects.page import SITEMAP_PAGE_DEFAULT_PRIORITY  # type: ignore
from usp.objects.page import SitemapPageChangeFrequency

from app.db.validators import validate_url_optional, validate_url_required
from app.schemas.base import BaseSchema, BaseSchemaRead


# generics
class GoogleNewsStory(BaseModel):
    title: str
    publish_date: datetime
    publication_name: str | None = None
    publication_language: str | None = None
    access: str | None = None
    genres: list[str] | None = None
    keywords: list[str] | None = None
    stock_tickers: list[str] | None = None


class WebsiteMapPage(BaseModel):
    url: str
    priority: Decimal = SITEMAP_PAGE_DEFAULT_PRIORITY
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    news_story: GoogleNewsStory | None = None


# schemas
class WebsiteMapBase(BaseSchema):
    url: str
    is_active: bool
    website_id: UUID4


class WebsiteMapCreate(WebsiteMapBase):
    url: str
    is_active: bool = True
    website_id: UUID4

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class WebsiteMapUpdate(BaseSchema):
    url: str | None = None
    is_active: bool | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class WebsiteMapRead(WebsiteMapBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsiteMapProcessing(BaseModel):
    url: str
    website_id: UUID4
    task_id: str

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class WebsiteMapProcessedResult(WebsiteMapCreate):
    website_map_pages: list[WebsiteMapPage]

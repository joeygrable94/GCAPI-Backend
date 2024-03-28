from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import Any

from pydantic import UUID4, BaseModel, field_validator

from app.db.validators import validate_url_optional, validate_url_required
from app.schemas.base import BaseSchema, BaseSchemaRead

# generics

SITEMAP_PAGE_DEFAULT_PRIORITY = Decimal("0.5")


@unique
class SitemapPageChangeFrequency(Enum):
    """Change frequency of a sitemap URL."""

    ALWAYS = "always"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NEVER = "never"

    @classmethod
    def has_value(cls, value: str) -> bool:  # pragma: no cover
        """Test if enum has specified value."""
        return any(value == item.value for item in cls)


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
    sitemap_id: UUID4
    task_id: UUID4 | str | Any | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class WebsiteMapProcessedResult(WebsiteMapCreate):
    sitemap_id: UUID4

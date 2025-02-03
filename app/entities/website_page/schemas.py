from datetime import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import Any, Union

from pydantic import UUID4, BaseModel, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import validate_url_optional, validate_url_required


@unique
class SitemapPageChangeFrequency(str, Enum):
    """Change frequency of a sitemap URL."""

    ALWAYS = "always"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NEVER = "never"

    @classmethod
    def has_value(cls, value: str) -> bool:
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


class WebsiteSitemapPage(BaseModel):
    url: str
    priority: Decimal = 0.5
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    news_story: GoogleNewsStory | None = None


class WebsitePageBase(BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    is_active: bool
    website_id: UUID4


class WebsitePageCreate(WebsitePageBase, BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    is_active: bool = True
    website_id: UUID4

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class WebsitePageUpdate(BaseSchema):
    url: str | None = None
    status: int | None = None
    priority: Union[float, Decimal] | None = None
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    is_active: bool | None = True
    website_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class WebsitePageRead(WebsitePageBase, BaseSchemaRead):
    id: UUID4


class WebsitePagePSIProcessing(BaseModel):
    page: WebsitePageRead
    psi_mobile_task_id: UUID4 | str | Any | None
    psi_desktop_task_id: UUID4 | str | Any | None


class WebsitePageKWCProcessing(BaseModel):
    page: WebsitePageRead
    kwc_task_id: UUID4 | str | Any | None

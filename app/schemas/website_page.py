from datetime import datetime
from decimal import Decimal
from typing import Any, Union

from pydantic import UUID4, BaseModel, field_validator

from app.db.validators import validate_url_optional, validate_url_required
from app.schemas import SitemapPageChangeFrequency
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class WebsitePageBase(BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    is_active: bool
    website_id: UUID4
    sitemap_id: UUID4 | None = None


class WebsitePageCreate(WebsitePageBase, BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    is_active: bool = True
    website_id: UUID4
    sitemap_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class WebsitePageUpdate(BaseSchema):
    url: str | None = None
    status: int | None = None
    priority: Union[float, Decimal] | None = None
    last_modified: datetime | None = None
    change_frequency: SitemapPageChangeFrequency | None = None
    is_active: bool | None = True
    website_id: UUID4 | None = None
    sitemap_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class WebsitePageRead(WebsitePageBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsitePagePSIProcessing(BaseModel):
    page: WebsitePageRead
    psi_mobile_task_id: UUID4 | str | Any | None
    psi_desktop_task_id: UUID4 | str | Any | None


class WebsitePageKWCProcessing(BaseModel):
    page: WebsitePageRead
    kwc_task_id: UUID4 | str | Any | None

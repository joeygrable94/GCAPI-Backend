from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Union

from pydantic import UUID4, BaseModel, field_validator

from app.db.validators import validate_url_optional, validate_url_required
from app.schemas.base import BaseSchema, BaseSchemaRead
from app.schemas.website_map import SitemapPageChangeFrequency


# schemas
class WebsitePageBase(BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: Optional[datetime] = None
    change_frequency: Optional[SitemapPageChangeFrequency] = None
    is_active: bool
    website_id: UUID4
    sitemap_id: Optional[UUID4] = None


class WebsitePageCreate(WebsitePageBase, BaseSchema):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: Optional[datetime] = None
    change_frequency: Optional[SitemapPageChangeFrequency] = None
    is_active: bool = True
    website_id: UUID4
    sitemap_id: Optional[UUID4] = None

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class WebsitePageUpdate(BaseSchema):
    url: Optional[str] = None
    status: Optional[int] = None
    priority: Optional[Union[float, Decimal]] = None
    last_modified: Optional[datetime] = None
    change_frequency: Optional[SitemapPageChangeFrequency] = None
    is_active: Optional[bool] = True
    website_id: Optional[UUID4] = None
    sitemap_id: Optional[UUID4] = None

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

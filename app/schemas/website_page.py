from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

from pydantic import UUID4, BaseModel
from usp.objects.page import SitemapPageChangeFrequency  # type: ignore

from app.db.validators import ValidateSchemaUrlOptional, ValidateSchemaUrlRequired
from app.schemas.base import BaseSchema, BaseSchemaRead


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


class WebsitePageCreate(ValidateSchemaUrlRequired, WebsitePageBase):
    url: str
    status: int
    priority: Union[float, Decimal]
    last_modified: Optional[datetime] = None
    change_frequency: Optional[SitemapPageChangeFrequency] = None
    is_active: bool = True
    website_id: UUID4
    sitemap_id: Optional[UUID4] = None


class WebsitePageUpdate(ValidateSchemaUrlOptional, BaseSchema):
    url: Optional[str] = None
    status: Optional[int] = None
    priority: Optional[Union[float, Decimal]] = None
    last_modified: Optional[datetime] = None
    change_frequency: Optional[SitemapPageChangeFrequency] = None
    is_active: Optional[bool] = True
    sitemap_id: Optional[UUID4] = None


class WebsitePageRead(WebsitePageBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsitePagePSIProcessing(BaseModel):
    page: WebsitePageRead
    psi_mobile_task_id: UUID4
    psi_desktop_task_id: UUID4


class WebsitePageKWCProcessing(BaseModel):
    page: WebsitePageRead
    kwc_task_id: UUID4

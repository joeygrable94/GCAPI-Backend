from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel

from app.db.acls import WebsitePageSpeedInsightsACL
from app.db.validators import (
    ValidateSchemaDeviceRequired,
    ValidateSchemaPerformanceValueRequired,
    ValidateSchemaStrategyRequired,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


class PSIDevice(str, Enum):
    desktop = "desktop"
    mobile = "mobile"


class PageSpeedInsightsDevice(ValidateSchemaDeviceRequired, BaseModel):
    device: PSIDevice


# schemas
class WebsitePageSpeedInsightsBase(
    ValidateSchemaStrategyRequired,
    ValidateSchemaPerformanceValueRequired,
    BaseSchema,
):
    strategy: str
    ps_weight: int
    ps_grade: float
    ps_value: str
    ps_unit: str
    fcp_weight: int
    fcp_grade: float
    fcp_value: float
    fcp_unit: str
    lcp_weight: int
    lcp_grade: float
    lcp_value: float
    lcp_unit: str
    cls_weight: int
    cls_grade: float
    cls_value: float
    cls_unit: str
    si_weight: int
    si_grade: float
    si_value: float
    si_unit: str
    tbt_weight: int
    tbt_grade: float
    tbt_value: float
    tbt_unit: str


class WebsitePageSpeedInsightsProcessing(BaseModel):
    website_id: UUID4
    page_id: UUID4
    insights: Optional[WebsitePageSpeedInsightsBase] = None


class WebsitePageSpeedInsightsCreate(WebsitePageSpeedInsightsBase):
    page_id: UUID4
    website_id: UUID4


class WebsitePageSpeedInsightsUpdate(BaseSchema):
    page_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class WebsitePageSpeedInsightsRead(
    WebsitePageSpeedInsightsACL,
    WebsitePageSpeedInsightsBase,
    BaseSchemaRead,
):
    page_id: UUID4
    website_id: UUID4

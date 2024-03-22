from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, field_validator

from app.db.validators import (
    validate_cls_unit_required,
    validate_device_required,
    validate_fcp_unit_required,
    validate_lcp_unit_required,
    validate_ps_unit_required,
    validate_ps_value_required,
    validate_si_unit_required,
    validate_strategy_required,
    validate_tbt_unit_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


class PSIDevice(str, Enum):
    desktop = "desktop"
    mobile = "mobile"


class PageSpeedInsightsDevice(BaseModel):
    device: PSIDevice

    _validate_device = field_validator("device", mode="before")(
        validate_device_required
    )


# schemas
class WebsitePageSpeedInsightsBase(BaseSchema):
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

    _validate_strategy = field_validator("strategy", mode="before")(
        validate_strategy_required
    )
    _validate_ps_value = field_validator("ps_value", mode="before")(
        validate_ps_value_required
    )
    _validate_ps_unit = field_validator("ps_unit", mode="before")(
        validate_ps_unit_required
    )
    _validate_fcp_unit = field_validator("fcp_unit", mode="before")(
        validate_fcp_unit_required
    )
    _validate_lcp_unit = field_validator("lcp_unit", mode="before")(
        validate_lcp_unit_required
    )
    _validate_cls_unit = field_validator("cls_unit", mode="before")(
        validate_cls_unit_required
    )
    _validate_si_unit = field_validator("si_unit", mode="before")(
        validate_si_unit_required
    )
    _validate_tbt_unit = field_validator("tbt_unit", mode="before")(
        validate_tbt_unit_required
    )


class WebsitePageSpeedInsightsProcessing(BaseModel):
    website_id: str
    page_id: str
    insights: Optional[WebsitePageSpeedInsightsBase] = None


class WebsitePageSpeedInsightsCreate(WebsitePageSpeedInsightsBase):
    page_id: UUID4
    website_id: UUID4


class WebsitePageSpeedInsightsUpdate(BaseSchema):
    page_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class WebsitePageSpeedInsightsRead(
    WebsitePageSpeedInsightsBase,
    BaseSchemaRead,
):
    page_id: UUID4
    website_id: UUID4

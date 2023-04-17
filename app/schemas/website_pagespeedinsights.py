from __future__ import annotations

from typing import Optional

from pydantic import UUID4, BaseModel, validator

from app.db.acls import WebsitePageSpeedInsightsACL
from app.schemas.base import BaseSchema, BaseSchemaRead


class PageSpeedInsightsDevice(BaseModel):
    device: str

    @validator("device")
    def limits_device(cls, v: str) -> str:
        if len(v) <= 0:
            raise ValueError("device value is required")
        if v.lower() not in ["mobile", "desktop"]:
            raise ValueError("device value must be mobile or desktop")
        return v.lower()  # pragma: no cover


# validators
class ValidateWebPSIStrategyRequired(BaseSchema):
    strategy: str

    @validator("strategy")
    def limits_strategy(cls, v: str) -> str:
        if len(v) <= 0:
            raise ValueError("strategy value is required")
        if v.lower() not in ["mobile", "desktop"]:
            raise ValueError("strategy value must be mobile or desktop")
        return v


class ValidateWebPSIValueRequired(BaseSchema):
    ps_value: str

    @validator("ps_value")
    def limits_ps_value(cls, v: str) -> str:
        if len(v) <= 0:
            raise ValueError("performance score value is required")
        if len(v) > 4:
            raise ValueError(
                "performance score value must contain less than 4 characters"
            )
        return v


class ValidateWebPSIValueOptional(BaseSchema):
    ps_value: Optional[str]

    @validator("ps_value")
    def limits_ps_value(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 4:
            raise ValueError(
                "performance score value must contain less than 4 characters"
            )
        return v


# schemas
class WebsitePageSpeedInsightsBase(
    ValidateWebPSIStrategyRequired,
    ValidateWebPSIValueRequired,
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
    insights: Optional[WebsitePageSpeedInsightsBase]


class WebsitePageSpeedInsightsCreate(WebsitePageSpeedInsightsBase):
    page_id: UUID4
    website_id: UUID4


class WebsitePageSpeedInsightsUpdate(BaseSchema):
    page_id: Optional[UUID4]
    website_id: Optional[UUID4]


class WebsitePageSpeedInsightsRead(
    WebsitePageSpeedInsightsACL,
    WebsitePageSpeedInsightsBase,
    BaseSchemaRead,
):
    page_id: UUID4
    website_id: UUID4

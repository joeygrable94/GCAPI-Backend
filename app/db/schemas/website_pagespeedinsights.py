from __future__ import annotations

from typing import Optional

from pydantic import UUID4, validator

from app.db.acls.website_pagespeedinsights import WebsitePageSpeedInsightsACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateWebPSIStrategyRequired(BaseSchema):
    strategy: str

    @validator("strategy")
    def limits_strategy(cls, v: str) -> str:
        if len(v) == 0:
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
        if v and len(v) <= 0:
            raise ValueError("performance score value is required")
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
    i_weight: int
    i_grade: float
    i_value: float
    i_unit: str


class WebsitePageSpeedInsightsCreate(WebsitePageSpeedInsightsBase):
    page_id: UUID4
    website_id: UUID4


class WebsitePageSpeedInsightsUpdate(
    ValidateWebPSIStrategyRequired,
    ValidateWebPSIValueOptional,
    BaseSchema,
):
    strategy: Optional[str]
    ps_weight: Optional[int]
    ps_grade: Optional[float]
    ps_value: Optional[str]
    ps_unit: Optional[str]
    fcp_weight: Optional[int]
    fcp_grade: Optional[float]
    fcp_value: Optional[float]
    fcp_unit: Optional[str]
    lcp_weight: Optional[int]
    lcp_grade: Optional[float]
    lcp_value: Optional[float]
    lcp_unit: Optional[str]
    cls_weight: Optional[int]
    cls_grade: Optional[float]
    cls_value: Optional[float]
    cls_unit: Optional[str]
    si_weight: Optional[int]
    si_grade: Optional[float]
    si_value: Optional[float]
    si_unit: Optional[str]
    tbt_weight: Optional[int]
    tbt_grade: Optional[float]
    tbt_value: Optional[float]
    tbt_unit: Optional[str]
    i_weight: Optional[int]
    i_grade: Optional[float]
    i_value: Optional[float]
    i_unit: Optional[str]
    page_id: Optional[UUID4]
    website_id: Optional[UUID4]


class WebsitePageSpeedInsightsRead(
    WebsitePageSpeedInsightsACL,
    WebsitePageSpeedInsightsBase,
    BaseSchemaRead,
):
    page_id: UUID4
    website_id: UUID4

from __future__ import annotations

from typing import Optional

from pydantic import UUID4, validator

from app.db.acls.website_pagespeedinsights import WebsitePageSpeedInsightsACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# validators
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
    ValidateWebPSIValueRequired,
    BaseSchema,
):
    ps_grade: float
    ps_value: str
    fcp_grade: float
    fcp_value: float
    lcp_grade: float
    lcp_value: float
    cls_grade: float
    cls_value: float
    si_grade: float
    si_value: float
    tbt_grade: float
    tbt_value: float
    i_grade: float
    i_value: float
    page_id: UUID4
    website_id: UUID4


class WebsitePageSpeedInsightsCreate(WebsitePageSpeedInsightsBase):
    pass


class WebsitePageSpeedInsightsUpdate(
    ValidateWebPSIValueOptional,
    BaseSchema,
):
    ps_grade: Optional[float]
    ps_value: Optional[str]
    fcp_grade: Optional[float]
    fcp_value: Optional[float]
    lcp_grade: Optional[float]
    lcp_value: Optional[float]
    cls_grade: Optional[float]
    cls_value: Optional[float]
    si_grade: Optional[float]
    si_value: Optional[float]
    tbt_grade: Optional[float]
    tbt_value: Optional[float]
    i_grade: Optional[float]
    i_value: Optional[float]
    page_id: Optional[UUID4]
    website_id: Optional[UUID4]


class WebsitePageSpeedInsightsRead(
    WebsitePageSpeedInsightsACL,
    WebsitePageSpeedInsightsBase,
    BaseSchemaRead,
):
    id: UUID4

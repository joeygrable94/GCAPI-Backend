from enum import Enum

from pydantic import UUID4, BaseModel, field_validator

from app.db.validators import (
    validate_device_required,
    validate_grade_data_required,
    validate_strategy_required,
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
    score_grade: float
    grade_data: str

    _validate_strategy = field_validator("strategy", mode="before")(
        validate_strategy_required
    )
    _validate_styleguide = field_validator("grade_data", mode="before")(
        validate_grade_data_required
    )


class WebsitePageSpeedInsightsProcessing(BaseModel):
    website_id: str
    page_id: str
    insights: WebsitePageSpeedInsightsBase | None = None
    is_created: bool = False


class WebsitePageSpeedInsightsCreate(WebsitePageSpeedInsightsBase):
    page_id: UUID4
    website_id: UUID4


class WebsitePageSpeedInsightsUpdate(BaseSchema):
    page_id: UUID4 | None = None
    website_id: UUID4 | None = None


class WebsitePageSpeedInsightsRead(WebsitePageSpeedInsightsBase, BaseSchemaRead):
    page_id: UUID4
    website_id: UUID4

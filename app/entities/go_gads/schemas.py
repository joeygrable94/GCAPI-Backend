from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_measurement_id_required,
    validate_title_optional,
    validate_title_required,
)


class GoAdsPropertyBase(BaseSchema):
    title: str
    measurement_id: str
    organization_id: UUID4
    platform_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_measurement_id = field_validator("measurement_id", mode="before")(
        validate_measurement_id_required
    )


class GoAdsPropertyCreate(GoAdsPropertyBase):
    pass


class RequestGoAdsPropertyCreate(BaseSchema):
    title: str
    measurement_id: str
    organization_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_measurement_id = field_validator("measurement_id", mode="before")(
        validate_measurement_id_required
    )


class GoAdsPropertyUpdate(BaseSchema):
    title: str | None = None
    organization_id: UUID4 | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoAdsPropertyRead(GoAdsPropertyBase, BaseSchemaRead):
    id: UUID4

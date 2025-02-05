from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import validate_title_optional, validate_title_required


class GoSearchConsolePropertyBase(BaseSchema):
    title: str
    organization_id: UUID4
    website_id: UUID4
    platform_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class GoSearchConsolePropertyCreate(GoSearchConsolePropertyBase):
    pass


class RequestGoSearchConsolePropertyCreate(BaseSchema):
    title: str
    organization_id: UUID4
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class GoSearchConsolePropertyUpdate(BaseSchema):
    title: str | None = None
    organization_id: UUID4 | None = None
    website_id: UUID4 | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoSearchConsolePropertyRead(GoSearchConsolePropertyBase, BaseSchemaRead):
    id: UUID4

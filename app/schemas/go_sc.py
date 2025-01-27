from pydantic import UUID4, field_validator

from app.db.validators import validate_title_optional, validate_title_required
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoSearchConsolePropertyBase(BaseSchema):
    title: str
    client_id: UUID4
    website_id: UUID4
    platform_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class GoSearchConsolePropertyCreate(GoSearchConsolePropertyBase):
    pass


class RequestGoSearchConsolePropertyCreate(GoSearchConsolePropertyBase):
    title: str
    client_id: UUID4
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class GoSearchConsolePropertyUpdate(BaseSchema):
    title: str | None = None
    client_id: UUID4 | None = None
    website_id: UUID4 | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoSearchConsolePropertyRead(GoSearchConsolePropertyBase, BaseSchemaRead):
    id: UUID4

from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import validate_title_optional, validate_title_required


class PermissionBase(BaseSchema):
    title: str
    spec: dict

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class PermissionCreate(PermissionBase):
    title: str
    spec: dict

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class PermissionUpdate(BaseSchema):
    title: str | None
    spec: dict | None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class PermissionRead(PermissionBase, BaseSchemaRead):
    id: UUID4

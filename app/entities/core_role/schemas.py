from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import validate_title_optional, validate_title_required


class RoleBase(BaseSchema):
    title: str

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class RoleCreate(RoleBase):
    title: str

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class RoleUpdate(BaseSchema):
    title: str | None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class RoleRead(RoleBase, BaseSchemaRead):
    id: UUID4

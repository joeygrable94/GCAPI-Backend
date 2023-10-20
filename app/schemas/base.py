from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )


class BaseSchemaRead(BaseSchema):
    id: UUID4
    created_on: datetime
    updated_on: datetime

from datetime import datetime

from pydantic import UUID4, BaseConfig, BaseModel


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name: bool = True
        orm_mode: bool = True


class BaseSchemaRead(BaseSchema):
    id: UUID4
    created_on: datetime
    updated_on: datetime

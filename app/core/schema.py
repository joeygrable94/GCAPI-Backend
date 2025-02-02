from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel, ConfigDict

from app.utilities.dates_and_time import get_datetime_gmt_str_from_datetime


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: get_datetime_gmt_str_from_datetime},
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )

    def serializable_dict(self, **kwargs) -> dict:  # pragma: no cover
        default_dict = self.model_dump()
        return jsonable_encoder(default_dict)


class BaseSchemaRead(BaseSchema):
    id: UUID4
    created: datetime
    updated: datetime

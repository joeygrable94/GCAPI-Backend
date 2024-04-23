from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """

    title: str = Field(..., description="encrypt")
    title: str | None = Field(default=None, description="encrypt")

    _encrypt_fields: Dict[str, bool] = {}

    @model_validator(mode="after")
    def mark_encrypted_fields(self) -> Any:
        for k, v in self.model_fields.items():
            if v.description == "encrypt":
                self._encrypt_fields[k] = True
            else:
                self._encrypt_fields[k] = False
        return self

    """

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )


class BaseSchemaRead(BaseSchema):
    id: UUID4
    created: datetime
    updated: datetime

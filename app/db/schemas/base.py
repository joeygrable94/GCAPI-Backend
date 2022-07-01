from pydantic import BaseConfig, BaseModel


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name: bool = True
        orm_mode: bool = True

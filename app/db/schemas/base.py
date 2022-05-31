from pydantic import BaseConfig, BaseModel


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        orm_mode = True

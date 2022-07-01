from typing import Any

from pydantic import Field
from sqlalchemy import Column, MetaData
from sqlalchemy.orm import declarative_base  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore

from app.db.utilities import _get_uuid

metadata: MetaData = MetaData()
Base: Any = declarative_base(metadata=metadata)


@declarative_mixin
class BaseMixin:
    __tablename__: str
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Column[Any] = Field(default_factory=_get_uuid)
    created_on: Column[Any]
    updated_on: Column[Any]

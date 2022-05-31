from typing import Any

from pydantic import Field
from sqlalchemy import Column, MetaData
from sqlalchemy.orm import declarative_base  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore

from app.db.utilities import _get_uuid

Base = declarative_base(metadata=MetaData())


@declarative_mixin
class BaseMixin:
    __tablename__: str
    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"always_refresh": True}
    id: Column[Any] = Field(default_factory=_get_uuid)
    created_on: Column[Any]
    updated_on: Column[Any]


@declarative_mixin
class UserBaseMixin:
    created_on: Column[Any]
    updated_on: Column[Any]

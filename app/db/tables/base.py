from datetime import datetime
from typing import Any

from sqlalchemy import CHAR, Column, DateTime

from app.db.base_class import Base, BaseMixin
from app.db.utilities import _get_date, _get_uuid


class TableBase(BaseMixin, Base):
    __abstract__: bool = True
    __mapper_args__: Any = {"always_refresh": True}
    id: Column[str] = Column(
        CHAR(36), primary_key=True, unique=True, nullable=False, default=_get_uuid
    )
    created_on: Column[datetime] = Column(DateTime(timezone=True), default=_get_date)
    updated_on: Column[datetime] = Column(
        DateTime(timezone=True), default=_get_date, onupdate=_get_date
    )

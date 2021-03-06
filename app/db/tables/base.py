from datetime import datetime
from typing import Any

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, DateTime, func

from app.db.base_class import Base, BaseMixin
from app.db.utilities import _get_uuid


class TableBase(BaseMixin, Base):
    __abstract__: bool = True
    __mapper_args__: Any = {"always_refresh": True}
    id: Column[Any] = Column(
        GUID, primary_key=True, unique=True, nullable=False, default=_get_uuid()
    )
    created_on: Column[datetime] = Column(
        DateTime(timezone=True), default=func.current_timestamp()
    )
    updated_on: Column[datetime] = Column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

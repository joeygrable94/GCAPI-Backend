from datetime import datetime
from sqlalchemy import Column, DateTime

from app.db.base_class import Base, BaseMixin
from app.db.utilities import UUID_ID, GUID, _get_date, _get_uuid


class TableBase(BaseMixin, Base):
    __abstract__ = True
    __mapper_args__ = {"always_refresh": True}
    # CHAR(36)
    id: UUID_ID = Column(GUID, primary_key=True, unique=True, nullable=False, default=_get_uuid)
    created_on: datetime = Column(DateTime(timezone=True), default=_get_date)
    updated_on: datetime = Column(DateTime(timezone=True), default=_get_date, onupdate=_get_date)

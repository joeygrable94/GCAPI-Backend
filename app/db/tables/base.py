from sqlalchemy import CHAR, Column, DateTime

from app.db.utilities import _get_date, _get_uuid
from app.db.base_class import Base


class TableBase(Base):
    __abstract__            = True
    __mapper_args__         = {'always_refresh': True}
    id                      = Column(CHAR(36), primary_key=True, unique=True, nullable=False, default=_get_uuid)
    created_on              = Column(DateTime(timezone=True), default=_get_date)
    updated_on              = Column(DateTime(timezone=True), default=_get_date, onupdate=_get_date)

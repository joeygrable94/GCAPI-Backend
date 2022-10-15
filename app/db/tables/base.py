from typing import Any

from sqlalchemy import Column, DateTime, func

from app.core.utilities import get_uuid
from app.db.base_class import Base
from app.db.types import GUID


class TableBase(Base):
    __abstract__: bool = True
    __tablename__: str
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Column = Column(
        GUID, primary_key=True, unique=True, nullable=False, default=get_uuid()
    )
    created_on: Column = Column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Column = Column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

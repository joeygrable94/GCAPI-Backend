from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped

from app.core.utilities import get_uuid
from app.db.base_class import Base
from app.db.types import GUID


class TableBase(Base):
    __abstract__: bool = True
    __tablename__: str
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID] = Column(
        GUID, primary_key=True, unique=True, nullable=False, default=get_uuid()
    )
    created_on: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

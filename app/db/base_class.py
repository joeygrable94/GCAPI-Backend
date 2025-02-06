from datetime import datetime

from pydantic import UUID4
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.utilities import get_uuid
from app.utilities.dates_and_time import get_date


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_date, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_date, nullable=False, onupdate=get_date
    )

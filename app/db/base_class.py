from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.utilities.dates_and_time import get_date


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_date, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_date, nullable=False, onupdate=get_date
    )

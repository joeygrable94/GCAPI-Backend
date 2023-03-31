from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    pass


class Note(Base):
    __tablename__: str = "note"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # relationships
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str

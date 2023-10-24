from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client_report import ClientReport  # noqa: F401
    from .user import User  # noqa: F401


class Note(Base):
    __tablename__: str = "note"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    title: Mapped[str] = mapped_column(
        String(96), nullable=False, unique=True, primary_key=True
    )
    description: Mapped[str] = mapped_column(Text(5000), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    # relationships
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("user.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="notes")
    client_reports: Mapped[List["ClientReport"]] = relationship(
        "ClientReport", secondary="client_report_note", back_populates="notes"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str

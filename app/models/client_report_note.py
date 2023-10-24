from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client_report import ClientReport  # noqa: F401
    from .note import Note  # noqa: F401


class ClientReportNote(Base):
    __tablename__: str = "client_report_note"
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
    client_report_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("client_report.id"),
        primary_key=True,
        nullable=False,
    )
    note_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("note.id"),
        primary_key=True,
        nullable=False,
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"ClientReportNote({self.id}, [R({self.client_report_id}), N({self.note_id})])"  # noqa: E501
        return repr_str

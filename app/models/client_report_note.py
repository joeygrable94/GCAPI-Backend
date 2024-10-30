from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.utilities import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client_report import ClientReport  # noqa: F401
    from .note import Note  # noqa: F401


class ClientReportNote(Base, Timestamp):
    __tablename__: str = "client_report_note"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
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
        repr_str: str = (
            f"ClientReportNote({self.id}, [R({self.client_report_id}), N({self.note_id})])"  # noqa: E501
        )
        return repr_str

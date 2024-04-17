from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import BLOB, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import StringEncryptedType  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine  # type: ignore

from app.core.config import settings
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .note import Note  # noqa: F401


class ClientReport(Base):
    __tablename__: str = "client_report"
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
        StringEncryptedType(
            String,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="pkcs5",
            length=96,
        ),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    url: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="pkcs5",
            length=2048,
        ),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        StringEncryptedType(
            Text,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="pkcs5",
            length=5000,
        ),
        nullable=True,
    )
    keys: Mapped[str] = mapped_column(BLOB, nullable=True)

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship("Client", back_populates="client_reports")
    notes: Mapped[List["Note"]] = relationship(
        "Note", secondary="client_report_note", back_populates="client_reports"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"ClientReport({self.title}, created {self.created_on})"
        return repr_str

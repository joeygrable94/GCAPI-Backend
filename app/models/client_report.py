from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import BLOB, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import (  # type: ignore  # noqa: E501
    AesEngine,
    StringEncryptedType,
)

from app.core.config import settings
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_DESC_MAXLEN_STORED,
    DB_STR_TINYTEXT_MAXLEN_STORED,
    DB_STR_URLPATH_MAXLEN_INPUT,
)

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .note import Note  # noqa: F401


class ClientReport(Base, Timestamp):
    __tablename__: str = "client_report"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid(),
    )
    title: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        unique=True,
        nullable=False,
    )
    url: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_URLPATH_MAXLEN_INPUT,
        ),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_DESC_MAXLEN_STORED,
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
        repr_str: str = f"ClientReport({self.title})"
        return repr_str

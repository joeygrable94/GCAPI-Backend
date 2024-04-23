from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import ForeignKey, String
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
from app.db.constants import DB_STR_16BIT_MAXLEN_STORED, DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .go_a4 import GoAnalytics4Property  # noqa: F401


class GoAnalytics4Stream(Base, Timestamp):
    __tablename__: str = "go_a4_stream"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
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
    stream_id: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        unique=True,
        nullable=False,
        primary_key=True,
    )

    # relationships
    ga4_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("go_a4.id"), nullable=False
    )
    ga4_account: Mapped["GoAnalytics4Property"] = relationship(
        "GoAnalytics4Property", back_populates="ga4_streams"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GoAnalytics4Stream({self.title} \
            Stream[{self.stream_id}] for GA4 Property[{self.ga4_id}])"
        )
        return repr_str

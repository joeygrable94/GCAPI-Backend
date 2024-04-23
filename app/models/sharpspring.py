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
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401


class Sharpspring(Base, Timestamp):
    __tablename__: str = "sharpspring"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    api_key: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=False,
    )
    secret_key: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=False,
    )

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship(back_populates="sharpspring_accounts")

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Sharpspring(Client[{self.client_id}] since {self.created})"
        return repr_str

from datetime import datetime
from typing import TYPE_CHECKING, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import StringEncryptedType  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine  # type: ignore

from app.core.config import settings
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .file_asset import FileAsset  # noqa: F401


class ClientBucket(Base):
    """
    Bucket Name: The name of the AWS S3 bucket where the image is stored. This allows
        you to identify the specific bucket for retrieval.
    Object Key: The unique key (path) within the S3 bucket that identifies the image.
        This should be unique for each image and can include subdirectories if needed.
    """

    __tablename__: str = "client_bucket"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
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
    bucket_name: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="pkcs5",
            length=100,
        ),
        nullable=False,
        primary_key=True,
    )
    object_key: Mapped[str] = mapped_column(
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

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("client.id"),
        nullable=False,
    )
    client: Mapped["Client"] = relationship(back_populates="buckets")
    file_assets: Mapped[List["FileAsset"]] = relationship(
        "FileAsset",
        back_populates="client_bucket",
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"ClientBucket({self.bucket_name}, [C({self.client_id})])"
        return repr_str

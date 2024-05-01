from typing import TYPE_CHECKING, Any, Optional

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import (  # type: ignore  # noqa: E501
    AesEngine,
    StringEncryptedType,
)

from app.core.config import settings
from app.core.utilities.uuids import get_uuid
from app.db.base_class import Base
from app.db.constants import DB_STR_32BIT_MAXLEN_STORED, DB_STR_TINYTEXT_MAXLEN_STORED
from app.db.custom_types import LongText

if TYPE_CHECKING:  # pragma: no cover
    from .bdx_feed import BdxFeed  # noqa: F401
    from .client import Client  # noqa: F401
    from .client_bucket import ClientBucket  # noqa: F401
    from .gcft_snap import GcftSnap  # noqa: F401
    from .geocoord import Geocoord  # noqa: F401
    from .user import User  # noqa: F401


class FileAsset(Base, Timestamp):
    """
    ID (Primary Key): A unique identifier for each image record. You can use an
        auto-incrementing integer or a UUID as the primary key.

    Name: The name of the file as saved. This can be a user-provided name or a
        generated one based on the file's properties.

    Extension: The file extension (e.g., .jpg, .png) of the file. This helps in
        determining the file type and handling it appropriately.

    Size KB: The size of the file file in kilobytes.

    Title: A human readable title or name for the file. This can be the same as
        the name or a more descriptive title.

    Description (Optional): A description or caption for the file, allowing you
        to store additional metadata or information about the file.

    Tags (Optional): A column to store tags or keywords associated with the file.
        This can help with search and categorization.

    Is Private: A flag indicating whether the file is public or private. This can
        be useful if you want to control access to images.

    User ID: The ID of the user who uploaded the file. This associates the file
        with a specific user if your application has user accounts.

    Bucket ID: The ID of the bucket where the file is stored. This associates the
        file with a specific bucket if your application has multiple buckets.

    Client ID: The ID of the client that the file belongs to. This associates the
        file with a specific client if your application has multiple clients.
    """

    __tablename__: str = "file_asset"
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
    filename: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=False,
        unique=True,
        default="default",
    )
    extension: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=False,
        default="jpg",
    )
    size_kb: Mapped[int] = mapped_column(
        StringEncryptedType(
            Integer,
            settings.api.encryption_key,
            AesEngine,
            "oneandzeroes",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=False,
        default=0,
    )
    title: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=False,
    )
    caption: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
    )
    keys: Mapped[str] = mapped_column(LongText, nullable=True)
    is_private: Mapped[bool] = mapped_column(
        StringEncryptedType(
            Boolean,
            settings.api.encryption_key,
            AesEngine,
            "zeroes",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=False,
        default=False,
    )

    # relationships
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("user.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="file_assets")
    bucket_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client_bucket.id"), nullable=False
    )
    client_bucket: Mapped["ClientBucket"] = relationship(
        "ClientBucket", back_populates="file_assets"
    )
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship("Client", back_populates="file_assets")
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )
    geotag: Mapped[Optional["Geocoord"]] = relationship(
        "Geocoord", back_populates="file_assets"
    )
    bdx_feed_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("bdx_feed.id"), nullable=True
    )
    bdx_feed: Mapped[Optional["BdxFeed"]] = relationship(
        "BdxFeed", back_populates="file_assets"
    )
    gcft_snap: Mapped[Optional["GcftSnap"]] = relationship(
        "GcftSnap", back_populates="file_asset"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"FileAsset({self.title} | {self.filename}.{self.extension} \
            [{self.size_kb} kb]: created {self.created}, updated {self.updated})"
        )
        return repr_str

from typing import TYPE_CHECKING, Any, Optional

from pydantic import UUID4
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.utilities.uuids import get_uuid
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_BUCKET_OBJECT_NAME_MAXLEN_INPUT,
    DB_STR_SHORTTEXT_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)

if TYPE_CHECKING:  # pragma: no cover
    from .bdx_feed import BdxFeed  # noqa: F401
    from .client import Client  # noqa: F401
    from .data_bucket import DataBucket  # noqa: F401
    from .gcft_snap import GcftSnap  # noqa: F401
    from .geocoord import Geocoord  # noqa: F401
    from .user import User  # noqa: F401


class FileAsset(Base, Timestamp):
    """
    ID (Primary Key): A unique identifier for each data record.

    Name: The name of the file as saved.

    mime_type: The files mimeType valid provided by Google Cloud.

    Size KB: The size of the file file in kilobytes (optional).

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
    file_name: Mapped[str] = mapped_column(
        String(length=DB_STR_BUCKET_OBJECT_NAME_MAXLEN_INPUT),
        index=True,
        nullable=False,
        unique=True,
        default="default",
    )
    mime_type: Mapped[str] = mapped_column(
        String(length=DB_STR_SHORTTEXT_MAXLEN_INPUT),
        nullable=False,
        default="image/jpeg",
    )
    size_kb: Mapped[int] = mapped_column(
        Integer(),
        nullable=True,
        default=None,
    )
    title: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        nullable=False,
    )
    caption: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        nullable=True,
    )

    # relationships
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("user.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="file_assets")
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
            f"FileAsset({self.title} | {self.file_name} [{self.size_kb} kb]: created {self.created}, updated {self.updated})"  # noqa: E501
        )
        return repr_str

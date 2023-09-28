from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import BLOB, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import Geocoord  # noqa: F401


class FileAsset(Base):
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
    name: Mapped[str] = mapped_column(
        String(96), nullable=False, unique=True, primary_key=True, default="default"
    )
    extension: Mapped[str] = mapped_column(String(255), nullable=False, default="jpg")
    size_kb: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    title: Mapped[str] = mapped_column(String(96), nullable=False)
    caption: Mapped[str] = mapped_column(String(150), nullable=True)
    keys: Mapped[str] = mapped_column(BLOB, nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)

    # relationships
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("user.id"), nullable=False
    )
    bucket_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client_bucket.id"), nullable=False
    )
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )
    bdx_feed_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("bdx_feed.id"), nullable=True
    )
    geotag: Mapped["Geocoord"] = relationship(
        "Geocoord", backref=backref("file_asset", lazy="subquery")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"FileAsset({self.title} | {self.name}.{self.extension} \
            [{self.size_kb} kb]: created {self.created_on}, updated {self.updated_on})"
        return repr_str

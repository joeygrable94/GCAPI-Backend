from typing import TYPE_CHECKING, Optional

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
from app.db.constants import (
    DB_STR_BUCKET_NAME_MAXLEN_INPUT,
    DB_STR_BUCKET_OBJECT_PREFIX_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_STORED,
)

if TYPE_CHECKING:  # pragma: no cover
    from .bdx_feed import BdxFeed  # noqa: F401
    from .client import Client  # noqa: F401
    from .file_asset import FileAsset  # noqa: F401
    from .gcft import Gcft  # noqa: F401


class DataBucket(Base, Timestamp):
    """
    Bucket Name: The name of the folder where the data is stored.

    Bucket Key: The unique key (id) provided by Google Cloud that identifies the folder.
        This should be unique for each folder.
    """

    __tablename__: str = "data_bucket"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid(),
    )
    bucket_name: Mapped[str] = mapped_column(
        String(length=DB_STR_BUCKET_NAME_MAXLEN_INPUT),
        index=True,
        nullable=False,
        default=settings.cloud.aws_s3_default_bucket,
    )
    bucket_prefix: Mapped[str] = mapped_column(
        String(length=DB_STR_BUCKET_OBJECT_PREFIX_MAXLEN_INPUT),
        index=True,
        unique=True,
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

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("client.id"),
        nullable=False,
    )
    client: Mapped["Client"] = relationship(
        back_populates="data_bucket", single_parent=True
    )
    bdx_feed_id: Mapped[UUID4 | None] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("bdx_feed.id"),
        nullable=True,
        default=None,
    )
    bdx_feed: Mapped[Optional["BdxFeed"]] = relationship(back_populates="data_bucket")
    gcft_id: Mapped[UUID4 | None] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("gcft.id"),
        nullable=True,
        default=None,
    )
    gcflytour: Mapped[Optional["Gcft"]] = relationship(back_populates="data_bucket")

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"DataBucket({self.bucket_name}, [C({self.client_id})])"
        return repr_str

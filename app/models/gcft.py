from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFT(Base):
    __tablename__: str = "gcft"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    group_slug: Mapped[str] = mapped_column(String(12), nullable=False)

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    gcft_snaps: Mapped[List["GCFTSnap"]] = relationship(
        "GCFTSnap", backref=backref("gcft", lazy="subquery")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GCFT({self.group_name}[{self.group_slug}], Client[{self.client_id}])"
        )
        return repr_str

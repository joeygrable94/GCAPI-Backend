from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_random_username  # type: ignore
from app.core.utilities.uuids import get_uuid
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .geocoord import GeoCoord  # noqa: F401
    from .note import Note  # noqa: F401


class User(Base):
    __tablename__: str = "user"
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
    auth_id: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        default=get_random_username(),
    )
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)

    # relationships
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=False
    )
    clients: Mapped[List["Client"]] = relationship(
        "User", secondary="user_client", back_populates="clients"
    )
    notes: Mapped[List["Note"]] = relationship(
        "Note", backref=backref("user", lazy="subquery")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"User({self.username})"
        return repr_str

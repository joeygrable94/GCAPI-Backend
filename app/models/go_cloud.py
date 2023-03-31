from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401


class GoogleCloudProperty(Base):
    __tablename__: str = "go_cloud"
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
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_api_key: Mapped[str] = mapped_column(String(64), nullable=False)
    hashed_project_id: Mapped[str] = mapped_column(String(64), nullable=False)
    hashed_project_number: Mapped[str] = mapped_column(String(64), nullable=False)
    hashed_service_account: Mapped[str] = mapped_column(String(64), nullable=False)

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleCloudProperty(Project[{self.project_name}] \
            for Client[{self.client_id}])"
        return repr_str
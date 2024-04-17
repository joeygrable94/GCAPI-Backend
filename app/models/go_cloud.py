from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAX_LEN

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401


class GoCloudProperty(Base):
    __tablename__: str = "go_cloud"
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
    project_name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, primary_key=True
    )
    api_key: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAX_LEN), nullable=False
    )
    project_id: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAX_LEN), nullable=False
    )
    project_number: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAX_LEN), nullable=False
    )
    service_account: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAX_LEN), nullable=False
    )

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship(back_populates="gcloud_accounts")

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GoCloudProperty(Project[{self.project_name}] \
            for Client[{self.client_id}])"
        )
        return repr_str

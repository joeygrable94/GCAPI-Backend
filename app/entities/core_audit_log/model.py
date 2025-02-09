from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import JSONType, UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.core_ipaddress.model import Ipaddress
    from app.entities.core_user.model import User


class AuditLog(Base):
    __tablename__: str = "audit_log"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
    )
    change_type: Mapped[str] = mapped_column(
        String(DB_STR_64BIT_MAXLEN_INPUT), nullable=False, default="create"
    )
    change_spec: Mapped[JSON] = mapped_column(
        JSONType(),
        nullable=False,
    )
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("user.id"),
        nullable=False,
    )
    ipaddress_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("ipaddress.id"),
        nullable=False,
    )

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")
    ipaddress: Mapped["Ipaddress"] = relationship(
        "Ipaddress", back_populates="audit_logs"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"AuditLog({self.change_type}, {self.created_at} by {self.user_id} from {self.ipaddress_id})"
        return repr_str

from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class UserIpaddress(Base):
    __tablename__: str = "user_ipaddress"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
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

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"UserIpaddress({self.id}, [U({self.user_id}), I({self.ipaddress_id})])"
        )
        return repr_str

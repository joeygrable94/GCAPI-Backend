from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Column, PickleType, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .token import AccessToken  # noqa: F401


class User(TableBase):
    __tablename__: str = "user"
    email: Column[str] = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Column[str] = Column(String(length=1024), nullable=False)
    is_active: Column[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Column[bool] = Column(Boolean, default=False, nullable=False)
    is_verified: Column[bool] = Column(Boolean, default=False, nullable=False)
    principals: Column[List[str]] = Column(
        MutableList.as_mutable(PickleType), default=[], nullable=False
    )

    # relationships
    tokens: Column[Optional[List["AccessToken"]]] = relationship(  # type: ignore
        "AccessToken", backref=backref("user", lazy="subquery")
    )
    clients: Column[Optional[List["Client"]]] = relationship(  # type: ignore
        "Client", secondary="user_client", back_populates="users"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"User({self.email} created {self.created_on}, UUID[{self.id}])"
        return repr_str

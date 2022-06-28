from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import backref, relationship, validates

from app.core.config import settings
from app.db.tables.base import TableBase
from app.db.utilities import email_pattern

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .item import Item  # noqa: F401
    from .user_client import UserClient  # noqa: F401


class User(TableBase):
    __tablename__: str = "user"
    email: Column[str] = Column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Column[str] = Column(String(length=1024), nullable=False)
    is_active: Column[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Column[bool] = Column(Boolean, default=False, nullable=False)
    is_verified: Column[bool] = Column(Boolean, default=False, nullable=False)

    # relationships
    clients: Any = relationship(
        "Client", secondary="user_client", back_populates="users"
    )
    items: Any = relationship("Item", backref=backref("user", lazy="noload"))

    @validates("email")
    def validate_email(self, k: Any, v: Any) -> Any:
        assert isinstance(v, str)
        if not email_pattern.fullmatch(v):
            raise ValueError("Invalid characters in the username/email")
        if settings.EMAIL_PROVIDER_RESTRICTION:
            if not any(
                provider in v for provider in settings.ALLOWED_EMAIL_PROVIDER_LIST
            ):
                raise ValueError("Invalid email provider")
        return v

    def __repr__(self) -> str:
        repr_str: str = f"User({self.email} created {self.created_on}, UUID[{self.id}])"
        return repr_str

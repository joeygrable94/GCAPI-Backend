from typing import TYPE_CHECKING, Any

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import backref, relationship, validates

from app.core.config import settings
from app.db.tables.base import UserTableBase
from app.db.utilities import email_pattern

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .item import Item  # noqa: F401
    from .user_client import UserClient  # noqa: F401


class User(UserTableBase, SQLAlchemyBaseUserTableUUID):

    # relationships
    clients = relationship("Client", secondary="user_client", back_populates="users")
    items = relationship("Item", backref=backref("user", lazy="noload"))

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
        repr_str = f"User({self.email} created {self.created_on}, UUID[{self.id}])"
        return repr_str

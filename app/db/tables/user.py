from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import backref, relationship, validates

from app.core.config import settings
from app.core.utilities import email_regex
from app.db.tables.base import TableBase

if TYPE_CHECKING:  # pragma: no cover
    from .token import AccessToken  # noqa: F401


class User(TableBase):
    __tablename__: str = "user"
    email: Column = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Column = Column(String(length=1024), nullable=False)
    is_active: Column = Column(Boolean, default=True, nullable=False)
    is_superuser: Column = Column(Boolean, default=False, nullable=False)
    is_verified: Column = Column(Boolean, default=False, nullable=False)

    # relationships
    tokens: Any = relationship("AccessToken", backref=backref("user", lazy="subquery"))

    @validates("email")
    def validate_email(self, k: Any, v: Any) -> Any:
        assert isinstance(v, str)
        if not email_regex.fullmatch(v):
            raise ValueError("Invalid characters in the username/email")
        if settings.EMAIL_PROVIDER_RESTRICTION:
            if not any(
                provider in v for provider in settings.ALLOWED_EMAIL_PROVIDER_LIST
            ):
                raise ValueError("Invalid email provider")
        return v

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"User({self.email} created {self.created_on}, UUID[{self.id}])"
        return repr_str

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Column, PickleType, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, backref, relationship, validates

from app.core.config import settings
from app.core.utilities import email_regex, scope_regex
from app.db.tables.base import TableBase

if TYPE_CHECKING:  # pragma: no cover
    from .token import AccessToken  # noqa: F401


class User(TableBase):
    __tablename__: str = "user"
    email: Mapped[str] = Column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = Column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    scopes: Mapped[Any] = Column(
        MutableList.as_mutable(PickleType), default=[], nullable=False
    )

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

    @validates("scopes")
    def validate_scopes(self, k: Any, v: Any) -> Any:
        assert isinstance(v, list)
        for s in v:
            if not scope_regex.fullmatch(s.lower()):
                raise ValueError("Invalid scope format")  # pragma: no cover
        return v

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"User({self.email} created {self.created_on}, UUID[{self.id}])"
        return repr_str

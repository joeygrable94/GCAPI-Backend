from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID


class AccessToken(TableBase):
    __tablename__: str = "accesstoken"
    token_jti: Mapped[str] = Column(String(64), primary_key=True)
    csrf: Mapped[str] = Column(String(64), default="", nullable=False)
    expires_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    is_revoked: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    # relationships
    user_id: Mapped[UUID] = Column(
        GUID, ForeignKey("user.id", ondelete="cascade"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"AccessToken({self.id}, [Issued({self.created_on}), U({self.user_id})])"
        )
        return repr_str

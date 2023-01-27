from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String

from app.db.tables.base import TableBase
from app.db.types import GUID


class AccessToken(TableBase):
    __tablename__: str = "accesstoken"
    token_jti: Column[str] = Column(String(64), primary_key=True)
    csrf: Column[str] = Column(String(64), nullable=False, default="")
    expires_at: Column[Optional[datetime]] = Column(
        DateTime(timezone=True), nullable=True
    )
    is_revoked: Column[bool] = Column(Boolean, default=False, nullable=False)

    # relationships
    user_id: Column[UUID] = Column(
        GUID, ForeignKey("user.id", ondelete="cascade"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"AccessToken({self.id}, [Issued({self.created_on}), U({self.user_id})])"
        )
        return repr_str

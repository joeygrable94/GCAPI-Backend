from typing import TYPE_CHECKING, Any

from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFT(TableBase):
    __tablename__: str = "gcft"
    group_name: Column[str] = Column(String(255), nullable=False)
    group_slug: Column[str] = Column(String(12), nullable=False)

    # relationships
    client_id: Column[str] = Column(CHAR(36), ForeignKey("client.id"), nullable=False)
    gcft_snaps: Any = relationship("GCFTSnap", backref=backref("gcft", lazy="subquery"))

    def __repr__(self) -> str:
        repr_str: str = (
            f"GCFT({self.group_name}[{self.group_slug}], Client[{self.client_id}])"
        )
        return repr_str

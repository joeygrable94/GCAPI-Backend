from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFT(TableBase):
    __tablename__ = "gcft"
    group_name = Column(String(255), nullable=False)
    group_slug = Column(String(12), nullable=False)

    # relationships
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)
    gcft_snaps = relationship("GCFTSnap", backref=backref("gcft", lazy="subquery"))

    def __repr__(self) -> str:
        repr_str = (
            f"GCFT({self.group_name}[{self.group_slug}], Client[{self.client_id}])"
        )
        return repr_str

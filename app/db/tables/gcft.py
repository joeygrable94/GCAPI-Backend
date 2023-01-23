from typing import TYPE_CHECKING, Any, List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFT(TableBase):
    __tablename__: str = "gcft"
    group_name: Mapped[str] = Column(String(255), nullable=False)
    group_slug: Mapped[str] = Column(String(12), nullable=False)

    # relationships
    client_id: Mapped[UUID] = Column(GUID, ForeignKey("client.id"), nullable=False)
    gcft_snaps: Mapped[Optional[List[Any]]] = relationship(
        "GCFTSnap", backref=backref("gcft", lazy="subquery")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GCFT({self.group_name}[{self.group_slug}], Client[{self.client_id}])"
        )
        return repr_str

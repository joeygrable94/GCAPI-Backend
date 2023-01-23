from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401


class GoogleCloudProperty(TableBase):
    __tablename__: str = "go_cloud"
    project_name: Mapped[str] = Column(String(255), nullable=False)
    hashed_api_key: Mapped[str] = Column(String(64), nullable=False)
    hashed_project_id: Mapped[str] = Column(String(64), nullable=False)
    hashed_project_number: Mapped[str] = Column(String(64), nullable=False)
    hashed_service_account: Mapped[str] = Column(String(64), nullable=False)

    # relationships
    client_id: Mapped[UUID] = Column(GUID, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleCloudProperty(Project[{self.project_name}] \
            for Client[{self.client_id}])"
        return repr_str

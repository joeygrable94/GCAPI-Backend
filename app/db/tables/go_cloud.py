from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401


class GoogleCloudProperty(TableBase):
    __tablename__: str = "go_cloud"
    project_name: Column[str] = Column(String(255), nullable=False)
    hashed_api_key: Column[str] = Column(String(64), nullable=False)
    hashed_project_id: Column[str] = Column(String(64), nullable=False)
    hashed_project_number: Column[str] = Column(String(64), nullable=False)
    hashed_service_account: Column[str] = Column(String(64), nullable=False)

    # relationships
    client_id: Column[str] = Column(GUID, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GoogleCloudProperty(Project[{self.project_name}] \
            for Client[{self.client_id}])"
        return repr_str

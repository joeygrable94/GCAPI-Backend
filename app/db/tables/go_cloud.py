from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401


class GoogleCloudProperty(TableBase):
    """
    SAMPLE DATA
    project_name: "GC Google Cloud API"
    project_id: "soy-antenna-123456"
    project_number: "1ab234567c8d"
    service_account: "service-account-name@soy-antenna-123456.iam.gserviceaccount.com"
    api_key: "neja389dd_CWN_ddihotkupWndASqkoSq9dpPK8"
    """

    __tablename__ = "go_cloud"
    project_name = Column(String(255), nullable=False)
    hashed_api_key = Column(String(64), nullable=False)
    hashed_project_id = Column(String(64), nullable=False)
    hashed_project_number = Column(String(64), nullable=False)
    hashed_service_account = Column(String(64), nullable=False)

    # relationships
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"GoogleCloudProperty(Project[{self.project_name}] for Client[{self.client_id}])"
        return repr_str

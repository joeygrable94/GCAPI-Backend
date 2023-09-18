from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import ClientACL
from app.db.validators import (
    ValidateSchemaDescriptionOptional,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class ClientBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaDescriptionOptional,
):
    title: str
    description: Optional[str]


class ClientCreate(ClientBase):
    title: str
    description: Optional[str]


class ClientUpdate(
    ValidateSchemaTitleOptional,
    ValidateSchemaDescriptionOptional,
):
    title: Optional[str]
    description: Optional[str]


class ClientRead(ClientACL, ClientBase, BaseSchemaRead):
    id: UUID4


# relationships
class ClientReadRelations(ClientRead):
    users: Optional[List["UserRead"]] = []
    websites: Optional[List["WebsiteRead"]] = []
    client_reports: Optional[List["ClientReportRead"]] = []
    sharpspring_accounts: Optional[List["SharpspringRead"]] = []
    bdx_feed_accounts: Optional[List["BdxFeedRead"]] = []
    # gcloud_accounts: Optional[List["GoCloudPropertyRead"]] = []
    # ga4_accounts: Optional[List["GoAnalytics4PropertyRead"]] = []
    # gua_accounts: Optional[List["GoUniversalAnalyticsPropertyRead"]] = []


from app.schemas.bdx_feed import BdxFeedRead  # noqa: E402
from app.schemas.client_report import ClientReportRead  # noqa: E402
from app.schemas.sharpspring import SharpspringRead  # noqa: E402
from app.schemas.user import UserRead  # noqa: E402
from app.schemas.website import WebsiteRead  # noqa: E402

ClientReadRelations.update_forward_refs()

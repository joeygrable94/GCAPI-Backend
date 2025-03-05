from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.core_organization.model import Organization
from app.entities.core_user.model import User
from app.entities.core_user_organization.model import UserOrganization
from app.entities.go_gads.model import GoAdsProperty
from app.entities.go_gads.schemas import (
    GoAdsPropertyCreate,
    GoAdsPropertyRead,
    GoAdsPropertyUpdate,
)
from app.entities.website_go_gads.model import WebsiteGoAdsProperty


class GoAdsPropertyRepository(
    BaseRepository[
        GoAdsPropertyCreate,
        GoAdsPropertyRead,
        GoAdsPropertyUpdate,
        GoAdsProperty,
    ]
):
    @property
    def _table(self) -> GoAdsProperty:
        return GoAdsProperty

    def query_list(
        self,
        user_id: UUID | None = None,
        organization_id: UUID | None = None,
        website_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(
                    Organization, GoAdsProperty.organization_id == Organization.id
                )
                .join(
                    UserOrganization,
                    Organization.id == UserOrganization.organization_id,
                )
                .join(User, UserOrganization.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if organization_id:
            stmt = stmt.join(
                Organization, GoAdsProperty.organization_id == Organization.id
            )
            conditions.append(Organization.id.like(organization_id))
        if website_id:
            stmt = stmt.join(
                WebsiteGoAdsProperty, GoAdsProperty.id == WebsiteGoAdsProperty.go_ads_id
            )
            conditions.append(WebsiteGoAdsProperty.website_id.like(website_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        # print(stmt)
        return stmt

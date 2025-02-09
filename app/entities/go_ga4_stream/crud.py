from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.core_organization.model import Organization
from app.entities.core_user.model import User
from app.entities.core_user_organization.model import UserOrganization
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4_stream.model import GoAnalytics4Stream
from app.entities.go_ga4_stream.schemas import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
    GoAnalytics4StreamUpdate,
)
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.website.model import Website


class GoAnalytics4StreamRepository(
    BaseRepository[
        GoAnalytics4StreamCreate,
        GoAnalytics4StreamRead,
        GoAnalytics4StreamUpdate,
        GoAnalytics4Stream,
    ]
):
    @property
    def _table(self) -> GoAnalytics4Stream:
        return GoAnalytics4Stream

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
        ga4_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(Website, GoAnalytics4Stream.website_id == Website.id)
                .join(OrganizationWebsite, Website.id == OrganizationWebsite.website_id)
                .join(
                    Organization, OrganizationWebsite.organization_id == Organization.id
                )
                .join(
                    UserOrganization,
                    Organization.id == UserOrganization.organization_id,
                )
                .join(User, UserOrganization.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if website_id:
            conditions.append(GoAnalytics4Stream.website_id.like(website_id))
        if ga4_id:
            stmt = stmt.join(
                GoAnalytics4Property,
                GoAnalytics4Stream.ga4_id == GoAnalytics4Property.id,
            )
            conditions.append(GoAnalytics4Stream.ga4_id.like(ga4_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

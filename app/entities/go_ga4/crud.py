from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4PropertyUpdate,
)
from app.entities.organization.model import Organization
from app.entities.user.model import User
from app.entities.user_organization.model import UserOrganization


class GoAnalytics4PropertyRepository(
    BaseRepository[
        GoAnalytics4PropertyCreate,
        GoAnalytics4PropertyRead,
        GoAnalytics4PropertyUpdate,
        GoAnalytics4Property,
    ]
):
    @property
    def _table(self) -> GoAnalytics4Property:
        return GoAnalytics4Property

    def query_list(
        self,
        user_id: UUID | None = None,
        organization_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(
                    Organization,
                    GoAnalytics4Property.organization_id == Organization.id,
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
                Organization, GoAnalytics4Property.organization_id == Organization.id
            )
            conditions.append(Organization.id.like(organization_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

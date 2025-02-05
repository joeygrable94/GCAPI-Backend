from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.go_gsc.model import GoSearchConsoleProperty
from app.entities.go_gsc.schemas import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
    GoSearchConsolePropertyUpdate,
)
from app.entities.organization.model import Organization
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.user.model import User
from app.entities.user_organization.model import UserOrganization
from app.entities.website.model import Website


class GoSearchConsolePropertyRepository(
    BaseRepository[
        GoSearchConsolePropertyCreate,
        GoSearchConsolePropertyRead,
        GoSearchConsolePropertyUpdate,
        GoSearchConsoleProperty,
    ]
):
    @property
    def _table(self) -> GoSearchConsoleProperty:
        return GoSearchConsoleProperty

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
                stmt.join(Website, self._table.website_id == Website.id)
                .join(OrganizationWebsite, Website.id == OrganizationWebsite.website_id)
                .join(Organization, OrganizationWebsite.organization_id == Organization.id)
                .join(UserOrganization, Organization.id == UserOrganization.organization_id)
                .join(User, UserOrganization.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if organization_id:  # TODO: test list gsc by organization_id
            stmt = stmt.join(Organization, GoSearchConsoleProperty.organization_id == Organization.id)
            conditions.append(Organization.id.like(organization_id))
        if website_id:  # TODO: test list gsc by website_id
            stmt.join(Website, GoSearchConsoleProperty.website_id == Website.id)
            conditions.append(GoSearchConsoleProperty.website_id.like(website_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

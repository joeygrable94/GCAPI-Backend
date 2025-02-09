from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.core_organization.model import Organization
from app.entities.core_user.model import User
from app.entities.core_user_organization.model import UserOrganization
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.website.model import Website
from app.entities.website_page.model import WebsitePage
from app.entities.website_page.schemas import (
    WebsitePageCreate,
    WebsitePageRead,
    WebsitePageUpdate,
)


class WebsitePageRepository(
    BaseRepository[WebsitePageCreate, WebsitePageRead, WebsitePageUpdate, WebsitePage]
):
    @property
    def _table(self) -> WebsitePage:
        return WebsitePage

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(Website, self._table.website_id == Website.id)
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
            stmt = stmt.join(Website, self._table.website_id == Website.id)
            conditions.append(self._table.website_id.like(website_id))
        if is_active is not None:
            conditions.append(self._table.is_active == is_active)
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

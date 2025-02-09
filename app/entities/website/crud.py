import socket
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.core.logger import logger
from app.entities.core_organization.model import Organization
from app.entities.core_user.model import User
from app.entities.core_user_organization.model import UserOrganization
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.website.model import Website
from app.entities.website.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate


class WebsiteRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _table(self) -> Website:
        return Website

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
                    OrganizationWebsite,
                    self._table.id == OrganizationWebsite.website_id,
                )
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
        if organization_id:
            stmt = stmt.join(
                OrganizationWebsite, self._table.id == OrganizationWebsite.website_id
            ).join(Organization, OrganizationWebsite.organization_id == Organization.id)
            conditions.append(Organization.id.like(organization_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

    async def validate(
        self,
        domain: str | None,
    ) -> bool:
        try:
            if not domain:
                raise Exception()
            addr = socket.gethostbyname(domain)
            logger.info(
                f"Validated website domain {domain} at IP address {addr}"
            )  # pragma: no cover
            return True
        except Exception:
            logger.info(
                f"Error validating the domain name: {domain}"
            )  # pragma: no cover
            return False

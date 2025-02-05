from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.organization.model import Organization
from app.entities.organization.schemas import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
)
from app.entities.user.model import User
from app.entities.user_organization.model import UserOrganization


class OrganizationRepository(
    BaseRepository[
        OrganizationCreate, OrganizationRead, OrganizationUpdate, Organization
    ]
):
    @property
    def _table(self) -> Organization:
        return Organization

    def query_list(
        self,
        user_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = stmt.join(
                UserOrganization, Organization.id == UserOrganization.organization_id
            ).join(User, UserOrganization.user_id == User.id)
            conditions.append(User.id.like(user_id))
        if is_active is not None:
            stmt = stmt.where(Organization.is_active == is_active)
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

from uuid import UUID

from sqlalchemy import Select
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.core_organization.model import Organization
from app.entities.core_user.model import User
from app.entities.core_user_organization.model import UserOrganization
from app.entities.organization_platform.model import OrganizationPlatform
from app.entities.platform.model import Platform
from app.entities.platform.schemas import (
    PlatformCreate,
    PlatformRead,
    PlatformUpdateAsAdmin,
)


class PlatformRepository(
    BaseRepository[PlatformCreate, PlatformRead, PlatformUpdateAsAdmin, Platform]
):
    @property
    def _table(self) -> Platform:
        return Platform

    def query_list(
        self,
        user_id: UUID | None = None,
        organization_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        if user_id:
            stmt = (
                stmt.join(
                    OrganizationPlatform,
                    Platform.id == OrganizationPlatform.platform_id,
                )
                .join(
                    Organization,
                    OrganizationPlatform.organization_id == Organization.id,
                )
                .join(
                    UserOrganization,
                    Organization.id == UserOrganization.organization_id,
                )
                .join(User, UserOrganization.user_id == User.id)
                .where(User.id == user_id)
            )
        if organization_id:
            stmt = (
                stmt.join(
                    OrganizationPlatform,
                    Platform.id == OrganizationPlatform.platform_id,
                )
                .join(
                    Organization,
                    OrganizationPlatform.organization_id == Organization.id,
                )
                .where(Organization.id == organization_id)
            )
        if is_active is not None:
            stmt = stmt.where(Platform.is_active == is_active)
        return stmt

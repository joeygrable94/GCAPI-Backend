from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Result, Select
from sqlalchemy import select as sql_select

from app.config import settings
from app.core.crud import BaseRepository
from app.entities.core_user.model import User
from app.entities.core_user.schemas import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserUpdatePrivileges,
)
from app.entities.core_user_organization.model import UserOrganization
from app.entities.organization_platform.model import OrganizationPlatform
from app.entities.organization_website.model import OrganizationWebsite
from app.utilities import paginate


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> User:
        return User

    async def get_list(
        self,
        page: int = 1,
    ) -> list[User] | list[None]:
        self._db.begin()
        skip, limit = paginate(
            page,
            default=settings.api.query_limit_rows_default,
            max=settings.api.query_limit_rows_max,
        )
        query: Select = sql_select(self._table).offset(skip).limit(limit)
        result: Result = await self._db.execute(query)
        data: Sequence[User] = result.scalars().all()
        data_list = list(data)
        return data_list

    async def verify_relationship(
        self,
        current_user_id: UUID,
        user_id: UUID | None = None,
        organization_id: UUID | None = None,
        platform_id: UUID | None = None,
        website_id: UUID | None = None,
    ) -> int:
        """
        Verify that the current user has access to the requested resource.

        Dynamically build a select query based on the parameters passed in:

        1. if a user_id is passed in get all the organizations of that user, then get
        all the organizations of the current user and see if there is an intersection.

        2. if a organization_id is passed in get all the organizations of the current user
        and see if the organization_id is in that list

        3. if a website_id is passed in get all the organizations of that website, then
        get all the organizations of the current user and see if there is an intersection

        """
        stmt: Select = sql_select(self._table)
        # 1
        if user_id:
            # get all the organizations of the user_id
            user_organizations = sql_select(UserOrganization.organization_id).where(
                UserOrganization.user_id == user_id
            )
            # get all organizations of the current user
            current_user_organizations = sql_select(
                UserOrganization.organization_id
            ).where(UserOrganization.user_id == current_user_id)
            # find the intersection
            stmt = (
                stmt.join(UserOrganization, User.id == UserOrganization.user_id)
                .where(UserOrganization.organization_id.in_(user_organizations))
                .where(UserOrganization.organization_id.in_(current_user_organizations))
            )
        # 2
        if organization_id:
            # get all organizations of the current user
            current_user_organizations = sql_select(
                UserOrganization.organization_id
            ).where(UserOrganization.user_id == current_user_id)
            # check if the organization_id is in the list
            stmt = (
                stmt.join(UserOrganization, User.id == UserOrganization.user_id)
                .where(UserOrganization.organization_id == organization_id)
                .where(UserOrganization.organization_id.in_(current_user_organizations))
            )
        # 3
        if platform_id:
            # get all organizations of the platform_id
            platform_organizations = sql_select(
                OrganizationPlatform.organization_id
            ).where(OrganizationPlatform.platform_id == platform_id)
            # get all organizations of the current user
            current_user_organizations = sql_select(
                UserOrganization.organization_id
            ).where(UserOrganization.user_id == current_user_id)
            # find the intersection
            stmt = (
                stmt.join(UserOrganization, User.id == UserOrganization.user_id)
                .where(UserOrganization.organization_id.in_(platform_organizations))
                .where(UserOrganization.organization_id.in_(current_user_organizations))
            )
        # 4
        if website_id:
            # get all organizations of the website_id
            website_organizations = sql_select(
                OrganizationWebsite.organization_id
            ).where(OrganizationWebsite.website_id == website_id)
            # get all organizations of the current user
            current_user_organizations = sql_select(
                UserOrganization.organization_id
            ).where(UserOrganization.user_id == current_user_id)
            # find the intersection
            stmt = (
                stmt.join(UserOrganization, User.id == UserOrganization.user_id)
                .where(UserOrganization.organization_id.in_(website_organizations))
                .where(UserOrganization.organization_id.in_(current_user_organizations))
            )
        result: Result = await self._db.execute(stmt)
        data: Sequence[User] = result.scalars().all()
        return len(data)

    async def add_privileges(
        self,
        entry: User,
        schema: UserUpdatePrivileges,
    ) -> User:
        updated_scopes = entry.scopes
        if schema.scopes:
            updated_scopes.extend(schema.scopes)
        entry.scopes = list(set(updated_scopes))
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def remove_privileges(
        self,
        entry: User,
        schema: UserUpdatePrivileges,
    ) -> User:
        user_scopes = entry.scopes
        if schema.scopes:
            updated_scopes = [
                scope for scope in user_scopes if scope not in schema.scopes
            ]
        entry.scopes = list(set(updated_scopes))
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Result, Select
from sqlalchemy import select as sql_select

from app.core.utilities import paginate
from app.crud.base import BaseRepository
from app.models import ClientPlatform, ClientWebsite, User, UserClient
from app.schemas import UserCreate, UserRead, UserUpdate, UserUpdatePrivileges


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> User:
        return User

    async def get_list(
        self,
        page: int = 1,
    ) -> list[User] | list[None]:
        self._db.begin()
        skip, limit = paginate(page)
        query: Select = sql_select(self._table).offset(skip).limit(limit)
        result: Result = await self._db.execute(query)
        data: Sequence[User] = result.scalars().all()
        data_list = list(data)
        return data_list

    async def verify_relationship(
        self,
        current_user_id: UUID,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        platform_id: UUID | None = None,
        website_id: UUID | None = None,
    ) -> int:
        """
        Verify that the current user has access to the requested resource.

        Dynamically build a select query based on the parameters passed in:

        1. if a user_id is passed in get all the clients of that user, then get
        all the clients of the current user and see if there is an intersection.

        2. if a client_id is passed in get all the clients of the current user
        and see if the client_id is in that list

        3. if a website_id is passed in get all the clients of that website, then
        get all the clients of the current user and see if there is an intersection

        """
        stmt: Select = sql_select(self._table)
        # 1
        if user_id:
            # get all the clients of the user_id
            user_clients = sql_select(UserClient.client_id).where(
                UserClient.user_id == user_id
            )
            # get all clients of the current user
            current_user_clients = sql_select(UserClient.client_id).where(
                UserClient.user_id == current_user_id
            )
            # find the intersection
            stmt = (
                stmt.join(UserClient, User.id == UserClient.user_id)
                .where(UserClient.client_id.in_(user_clients))
                .where(UserClient.client_id.in_(current_user_clients))
            )
        # 2
        if client_id:
            # get all clients of the current user
            current_user_clients = sql_select(UserClient.client_id).where(
                UserClient.user_id == current_user_id
            )
            # check if the client_id is in the list
            stmt = (
                stmt.join(UserClient, User.id == UserClient.user_id)
                .where(UserClient.client_id == client_id)
                .where(UserClient.client_id.in_(current_user_clients))
            )
        # 3
        if platform_id:
            # get all clients of the platform_id
            platform_clients = sql_select(ClientPlatform.client_id).where(
                ClientPlatform.platform_id == platform_id
            )
            # get all clients of the current user
            current_user_clients = sql_select(UserClient.client_id).where(
                UserClient.user_id == current_user_id
            )
            # find the intersection
            stmt = (
                stmt.join(UserClient, User.id == UserClient.user_id)
                .where(UserClient.client_id.in_(platform_clients))
                .where(UserClient.client_id.in_(current_user_clients))
            )
        # 4
        if website_id:
            # get all clients of the website_id
            website_clients = sql_select(ClientWebsite.client_id).where(
                ClientWebsite.website_id == website_id
            )
            # get all clients of the current user
            current_user_clients = sql_select(UserClient.client_id).where(
                UserClient.user_id == current_user_id
            )
            # find the intersection
            stmt = (
                stmt.join(UserClient, User.id == UserClient.user_id)
                .where(UserClient.client_id.in_(website_clients))
                .where(UserClient.client_id.in_(current_user_clients))
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

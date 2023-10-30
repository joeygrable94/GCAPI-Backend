from typing import Dict, Generic, List, Type, TypeVar

from fastapi import Depends, status
from pydantic import UUID4, BaseModel
from sqlalchemy import Select

from app.core.pagination import PageParams, Paginated, paginated_query
from app.core.security import configure_permissions
from app.core.security.permissions import (
    AclPrivilege,
    Authenticated,
    AuthPermissionException,
    Everyone,
    RoleAdmin,
    RoleManager,
)
from app.crud import ClientRepository, UserClientRepository, UserRepository
from app.db.base_class import Base
from app.models import User, UserClient
from app.schemas import UserUpdateAsAdmin, UserUpdateAsManager

from .get_auth import CurrentUser, get_current_user
from .get_db import AsyncDatabaseSession


def get_current_user_privileges(
    user: User = Depends(get_current_user),
) -> List[AclPrivilege]:
    principals: List[AclPrivilege]
    principals = [Everyone, Authenticated]
    principals.extend(user.privileges())
    return list(set(principals))


Permission = configure_permissions(get_current_user_privileges)


T = TypeVar("T", bound=BaseModel)
B = TypeVar("B", bound=Base)


class PermissionController(Generic[T]):
    db: AsyncDatabaseSession
    current_user: CurrentUser
    privileges: List[AclPrivilege]
    user_repo: UserRepository
    client_repo: ClientRepository
    user_client_repo: UserClientRepository

    def __init__(
        self,
        db: AsyncDatabaseSession,
        user: CurrentUser,
        privileges: List[AclPrivilege],
    ):
        self.db = db
        self.current_user = user
        self.privileges = privileges
        self.user_repo = UserRepository(db)
        self.client_repo = ClientRepository(db)
        self.user_client_repo = UserClientRepository(db)

    async def verify_user_can_access(
        self,
        user_id: UUID4 | None = None,
        client_id: UUID4 | None = None,
    ) -> bool:
        print(self.current_user)
        print(self.privileges)
        # admins and managers can access all users and clients
        if (
            self.current_user.is_superuser
            or RoleAdmin in self.privileges
            or RoleManager in self.privileges
        ):
            return True
        # check if the current user owns the user
        if user_id and user_id == self.current_user.id:
            return True
        # check if the current user owns the client
        if client_id:
            user_client: UserClient | None = await self.user_client_repo.exists_by_two(
                field_name_a="user_id",
                field_value_a=self.current_user.id,
                field_name_b="client_id",
                field_value_b=client_id,
            )
            if user_client:
                return True
        return False

    def verify_input_schema_by_role(
        self, input_object: T, schema_privileges: Dict[AclPrivilege, Type[T]]
    ) -> None:
        for privilege, schema in schema_privileges.items():
            if privilege in self.privileges and isinstance(input_object, schema):
                return
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="You do not have permission to access this resource",
        )

    def get_resource_response(
        self,
        resource: B,
        responses: Dict[AclPrivilege, Type[T]],
    ) -> T:
        for privilege, response_schema in responses.items():
            if privilege in self.privileges:
                return response_schema.model_validate(resource)
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="You do not have permission to access this resource",
        )

    async def get_paginated_resource_response(
        self,
        table_name: str,
        stmt: Select,
        page_params: PageParams,
        responses: Dict[AclPrivilege, Type[T]],
    ) -> Paginated[T]:
        for privilege, response_schema in responses.items():
            if privilege in self.privileges:
                return await paginated_query(
                    table_name=table_name,
                    db=self.db,
                    stmt=stmt,
                    page_params=page_params,
                    response_schema=response_schema,
                )
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="You do not have permission to access this resource",
        )

    async def add_privileges(
        self, to_user: User, schema: UserUpdateAsManager | UserUpdateAsAdmin
    ) -> User:
        user: User = await self.user_repo.add_privileges(to_user, schema)
        return user

    async def remove_privileges(
        self, to_user: User, schema: UserUpdateAsManager | UserUpdateAsAdmin
    ) -> User:
        user: User = await self.user_repo.remove_privileges(to_user, schema)
        return user

    def __repr__(self) -> str:
        repr_str: str = f"PermissionControl(User={self.current_user.auth_id})"
        return repr_str


def get_permission_controller(
    db: AsyncDatabaseSession,
    user: CurrentUser,
    privileges: List[AclPrivilege] = Depends(get_current_user_privileges),
) -> PermissionController:
    return PermissionController(db, user, privileges)

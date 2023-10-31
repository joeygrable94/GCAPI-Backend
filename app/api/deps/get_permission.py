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
from app.schemas.user import UserUpdatePrivileges

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
        print(self.current_user.id, user_id, client_id)
        user_client: UserClient | None
        # admins and managers can access all users and clients
        if (
            self.current_user.is_superuser
            or RoleAdmin in self.privileges
            or RoleManager in self.privileges
        ):
            return True
        # user_id and client_id was provided
        if user_id and client_id:
            # check if the requested user_id has a relationship with the client
            user_client = await self.user_client_repo.exists_by_two(
                field_name_a="user_id",
                field_value_a=user_id,
                field_name_b="client_id",
                field_value_b=client_id,
            )
            if user_client:
                return True
        # only client_id was provided
        elif client_id:
            # check if the current user has a relationship with the client
            user_client = await self.user_client_repo.exists_by_two(
                field_name_a="user_id",
                field_value_a=self.current_user.id,
                field_name_b="client_id",
                field_value_b=client_id,
            )
            if user_client:
                return True
        # only user_id was provided
        elif user_id:
            # check if the current user is the same as the user_id
            if user_id == self.current_user.id:
                return True
            # check if the current user is associated with
            # the same client as the user_id
            user_client = await self.user_client_repo.read_by(
                field_name="user_id", field_value=user_id
            )
            if user_client:
                current_user_client = await self.user_client_repo.exists_by_two(
                    field_name_a="user_id",
                    field_value_a=self.current_user.id,
                    field_name_b="client_id",
                    field_value_b=user_client.client_id,
                )
                if current_user_client:
                    return True
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="You do not have permission to access this resource",
        )

    def verify_input_schema_by_role(
        self, input_object: T, schema_privileges: Dict[AclPrivilege, Type[T]]
    ) -> None:
        input_dict = input_object.model_dump(exclude_unset=True, exclude_none=True)
        for privilege, schema in schema_privileges.items():
            if privilege in self.privileges:
                input_schema_keys = set(input_dict.keys())
                output_schema_keys = set(schema.__annotations__.keys())
                if input_schema_keys.issubset(output_schema_keys):
                    return
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="You do not have permission to take this action on this resource",
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
            message="You do not have permission to access the output of this resource",
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
            message="You do not have permission to access the paginated output of this resource",  # noqa: E501
        )

    async def add_privileges(self, to_user: User, schema: UserUpdatePrivileges) -> User:
        user: User = await self.user_repo.add_privileges(to_user, schema)
        return user

    async def remove_privileges(
        self, to_user: User, schema: UserUpdatePrivileges
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

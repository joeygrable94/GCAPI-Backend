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
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import ClientRepository, UserClientRepository, UserRepository
from app.db.base_class import Base
from app.models import User, UserClient
from app.schemas import UserUpdatePrivileges

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
    ):  # TODO: test
        self.db = db
        self.current_user = user
        self.privileges = privileges
        self.user_repo = UserRepository(db)
        self.client_repo = ClientRepository(db)
        self.user_client_repo = UserClientRepository(db)

    async def verify_user_can_access(
        self,
        privileges: List[AclPrivilege] = [],
        user_id: UUID4 | None = None,
        client_id: UUID4 | None = None,
    ) -> bool:
        user_client: UserClient | None
        # admins can access all users and clients
        if self.current_user.is_superuser or RoleAdmin in self.privileges:
            return True
        # current user with these privileges can access
        for perm in privileges:
            if perm in self.privileges:
                return True
        # user_id and client_id was provided
        if user_id and client_id:  # TODO: test
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
        elif client_id:  # TODO: test
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
            if user_client:  # TODO: test
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
                if set(input_dict.keys()).issubset(set(schema.__annotations__.keys())):
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
        raise AuthPermissionException(  # TODO: test
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

    def verify_user_add_scopes(
        self,
        schema: UserUpdatePrivileges,
    ) -> bool:
        # admin can add any scope
        if RoleAdmin in self.privileges:
            return True
        # only admin can add role based access
        if (
            (schema.scopes and RoleAdmin in schema.scopes)
            or (schema.scopes and RoleManager in schema.scopes)
            or (schema.scopes and RoleClient in schema.scopes)
            or (schema.scopes and RoleEmployee in schema.scopes)
            or (schema.scopes and RoleUser in schema.scopes)
        ):
            raise AuthPermissionException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                message="You do not have permission to add role based access to users",
            )
        # manager can only add user based access
        return True

    def verify_user_remove_scopes(
        self,
        schema: UserUpdatePrivileges,
    ) -> bool:
        # admin can remove any scope
        if RoleAdmin in self.privileges:
            return True
        # only admin can remove role based access
        if (
            (schema.scopes and RoleAdmin in schema.scopes)
            or (schema.scopes and RoleManager in schema.scopes)
            or (schema.scopes and RoleClient in schema.scopes)
            or (schema.scopes and RoleEmployee in schema.scopes)
            or (schema.scopes and RoleUser in schema.scopes)
        ):
            raise AuthPermissionException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                message="You do not have permission to remove role based access to users",  # noqa: E501
            )
        # manager can only remove user based access
        return True

    async def add_privileges(
        self, to_user: User, schema: UserUpdatePrivileges
    ) -> list[AclPrivilege]:
        # TODO: add validation to ensure that the scopes are valid
        self.verify_user_add_scopes(schema=schema)
        user_scopes: list[AclPrivilege] = await self.user_repo.add_privileges(
            entry=to_user, schema=schema
        )
        return user_scopes

    async def remove_privileges(
        self, to_user: User, schema: UserUpdatePrivileges
    ) -> list[AclPrivilege]:
        # TODO: add validation to ensure that the scopes are valid
        self.verify_user_remove_scopes(schema=schema)
        user_scopes: list[AclPrivilege] = await self.user_repo.remove_privileges(
            entry=to_user, schema=schema
        )
        return user_scopes

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"PermissionControl(User={self.current_user.auth_id})"
        return repr_str


def get_permission_controller(
    db: AsyncDatabaseSession,
    user: CurrentUser,
    privileges: List[AclPrivilege] = Depends(get_current_user_privileges),
) -> PermissionController:  # pragma: no cover
    return PermissionController(db, user, privileges)

from typing import Generic, TypeVar

from fastapi import status
from pydantic import UUID4, BaseModel
from sqlalchemy import Select

from app.core.pagination import PageParams, Paginated, paginated_query
from app.db.base_class import Base
from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.organization.crud import OrganizationRepository
from app.entities.user.crud import UserRepository
from app.entities.user.model import User
from app.entities.user.schemas import UserUpdatePrivileges
from app.entities.user_organization.crud import UserOrganizationRepository
from app.services.permission import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_RESPONSE,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_ADD,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_REMOVE,
    AclPrivilege,
    AuthPermissionException,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)

T = TypeVar("T", bound=BaseModel)
B = TypeVar("B", bound=Base)


class PermissionController(Generic[T]):
    db: AsyncDatabaseSession
    current_user: User
    privileges: list[AclPrivilege]
    user_repo: UserRepository
    organization_repo: OrganizationRepository
    user_organization_repo: UserOrganizationRepository

    def __init__(
        self,
        db: AsyncDatabaseSession,
        user: User,
        privileges: list[AclPrivilege],
    ):
        self.db = db
        self.current_user = user
        self.privileges = privileges
        self.user_repo = UserRepository(db)
        self.organization_repo = OrganizationRepository(db)
        self.user_organization_repo = UserOrganizationRepository(db)

    async def verify_user_can_access(
        self,
        privileges: list[AclPrivilege] = [],
        user_id: UUID4 | None = None,
        organization_id: UUID4 | None = None,
        platform_id: UUID4 | None = None,
        website_id: UUID4 | None = None,
    ) -> bool:
        # admins can access all resources
        if self.current_user.is_superuser or RoleAdmin in self.privileges:
            return True
        # current user with these privileges can access
        for perm in privileges:
            if perm in self.privileges:
                return True
        # current user can access their own resources
        if user_id and user_id == self.current_user.id:
            return True
        # count the current user relationships with resource
        users_access: int = await self.user_repo.verify_relationship(
            current_user_id=self.current_user.id,
            user_id=user_id,
            organization_id=organization_id,
            platform_id=platform_id,
            website_id=website_id,
        )
        if users_access:
            return True
        # deny access by default
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
        )

    def verify_input_schema_by_role(
        self, input_object: T, schema_privileges: dict[AclPrivilege, Generic[T]]
    ) -> None:
        input_dict = input_object.model_dump(exclude_unset=True, exclude_none=True)
        for privilege, schema in schema_privileges.items():
            if privilege in self.privileges:
                if set(input_dict.keys()).issubset(set(schema.__annotations__.keys())):
                    return
        raise AuthPermissionException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
        )

    def get_resource_response(
        self,
        resource: B,
        responses: dict[AclPrivilege, Generic[T]],
    ) -> T:
        for privilege, response_schema in responses.items():
            if privilege in self.privileges:
                return response_schema.model_validate(resource)
        raise AuthPermissionException(  # pragma: no cover - safety net
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            message=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_RESPONSE,
        )

    async def get_paginated_resource_response(
        self,
        table_name: str,
        stmt: Select,
        page_params: PageParams,
        responses: dict[AclPrivilege, Generic[T]],
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
            message=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION,
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
                message=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_ADD,
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
                message=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_REMOVE,
            )
        # manager can only remove user based access
        return True

    async def add_privileges(self, to_user: User, schema: UserUpdatePrivileges) -> User:
        self.verify_user_add_scopes(schema=schema)
        updated_user: User = await self.user_repo.add_privileges(
            entry=to_user, schema=schema
        )
        return updated_user

    async def remove_privileges(
        self, to_user: User, schema: UserUpdatePrivileges
    ) -> User:
        self.verify_user_remove_scopes(schema=schema)
        updated_user: User = await self.user_repo.remove_privileges(
            entry=to_user, schema=schema
        )
        return updated_user

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"PermissionControl(User={self.current_user.auth_id})"
        return repr_str

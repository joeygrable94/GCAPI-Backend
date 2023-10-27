from typing import Dict, Generic, List, Type, TypeVar

from fastapi import Depends, status
from pydantic import BaseModel
from sqlalchemy import Select

from app.core.pagination import PageParams, Paginated, paginate
from app.core.security import configure_permissions
from app.core.security.permissions import (
    AclPrivilege,
    Authenticated,
    AuthPermissionException,
    Everyone,
)
from app.crud import ClientRepository, UserClientRepository, UserRepository
from app.db.base_class import Base
from app.models import User

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
    user: CurrentUser
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
        self.user = user
        self.privileges = privileges
        self.user_repo = UserRepository(db)
        self.client_repo = ClientRepository(db)
        self.user_client_repo = UserClientRepository(db)

    def get_resource_response(
        self,
        resource: B,
        responses: Dict[AclPrivilege, T],
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
                return await paginate(
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

    def __repr__(self) -> str:
        repr_str: str = f"PermissionControl(User={self.user.auth_id})"
        return repr_str


def get_permission_controller(
    db: AsyncDatabaseSession,
    user: CurrentUser,
    privileges: List[AclPrivilege] = Depends(get_current_user_privileges),
) -> PermissionController:
    return PermissionController(db, user, privileges)

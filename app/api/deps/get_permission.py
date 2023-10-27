from typing import Dict, Generic, List, TypeVar

from fastapi import Depends, status

from app.core.security import configure_permissions
from app.core.security.permissions import (
    AclPrivilege,
    Authenticated,
    AuthPermissionException,
    Everyone,
)
from app.crud import ClientRepository, UserClientRepository, UserRepository
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

T = TypeVar("T")


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

    def get_resource_response(
        self,
        responses: Dict[AclPrivilege, T],
    ) -> T:
        for privilege, response in responses.items():
            if privilege in self.privileges:
                return response
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

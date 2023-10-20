from typing import Annotated, Any, List

from fastapi import Depends, HTTPException, Security, status

from app.api.exceptions import ErrorCode
from app.core.security import Auth0User, auth, configure_permissions, has_permission
from app.core.security.permissions import (
    AclPermission,
    AclScope,
    Authenticated,
    Everyone,
    RoleUser,
)
from app.crud import UserRepository
from app.models import User
from app.schemas import UserCreate

from .get_db import AsyncDatabaseSession


def get_acl_scope_list(roles: List[str], permissions: List[str]) -> List[AclScope]:
    user_scopes: List[AclScope] = [RoleUser]
    if roles:
        for auth0_role in roles:
            auth0_scope = AclScope(auth0_role)
            if auth0_scope not in user_scopes:
                user_scopes.append(auth0_scope)
    if permissions:
        for auth0_perm in permissions:
            auth0_scope = AclScope(auth0_perm)
            if auth0_scope not in user_scopes:
                user_scopes.append(auth0_scope)
    return user_scopes


def check_user_acl_scope_list(
    roles: List[str] | None,
    permissions: List[str] | None,
    user_privileges: List[AclScope],
) -> List[AclScope]:
    auth0_scopes: List[AclScope] = []
    if roles and permissions:
        auth0_scopes = get_acl_scope_list(roles, permissions)
    user_scopes: List[AclScope] = []
    for privilege in user_privileges:
        if privilege not in auth0_scopes:
            user_scopes.append(privilege)
    return user_scopes


async def get_current_user(
    db: AsyncDatabaseSession,
    auth0_user: Auth0User | None = Security(auth.get_user),
) -> User:
    if auth0_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.UNAUTHORIZED,
        )
    users_repo: UserRepository = UserRepository(session=db)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=auth0_user.auth_id
    )
    if not user:
        user_scopes = get_acl_scope_list(auth0_user.roles, auth0_user.permissions)
        user = await users_repo.create(
            UserCreate(
                auth_id=auth0_user.auth_id,
                email=auth0_user.email,
                username=auth0_user.email,
                scopes=user_scopes,
                is_superuser=False,
                is_verified=False,
                is_active=True,
            )
        )
    else:
        user_scopes = check_user_acl_scope_list(
            auth0_user.roles, auth0_user.permissions, user.privileges()
        )
        print("Auth0 Roles", auth0_user.roles)
        print("Auth0 Permissions", auth0_user.permissions)
        print("User Scopes", user.scopes)
        print("Update Scopes?", user_scopes)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_privileges(
    user: User = Depends(get_current_user),
) -> List[AclScope]:
    principals: List[AclScope]
    principals = [Everyone, Authenticated]
    principals.extend(user.privileges())
    return principals


Permission = configure_permissions(get_current_user_privileges)


def user_privilege_authorized(
    current_user: User,
    request_permission: AclPermission = AclPermission.read,
    request_data_model: Any = None,
) -> bool:
    if request_data_model is None:
        return False
    user_privileges: List[AclScope]
    user_privileges = get_current_user_privileges(current_user)
    return has_permission(user_privileges, request_permission, request_data_model)

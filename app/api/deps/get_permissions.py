from typing import Annotated, Any, List

from fastapi import Depends, HTTPException, Security, status

from app.api.exceptions import ErrorCode
from app.core.security import Auth0User, auth, configure_permissions, has_permission
from app.core.security.permissions import (
    AclPermission,
    AclScope,
    Authenticated,
    Everyone,
)
from app.crud import UserRepository
from app.models import User
from app.schemas import UserCreate

from .get_db import AsyncDatabaseSession


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
        user_roles: List[AclScope] = []
        if auth0_user.roles:
            for auth0_role in auth0_user.roles:
                user_roles.append(AclScope(scope=f"role:{auth0_role}"))
        else:
            user_roles.append(AclScope(scope="role:user"))
        user_scopes: List[AclScope] = []
        if auth0_user.permissions:
            for user_perm in auth0_user.permissions:
                user_scopes.append(AclScope(scope=user_perm))
        user = await users_repo.create(
            UserCreate(
                auth_id=auth0_user.auth_id,
                email=auth0_user.email,
                username=auth0_user.email,
                roles=user_roles,
                scopes=user_scopes,
                is_superuser=False,
                is_verified=False,
                is_active=True,
            )
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_privileges(
    user: User = Depends(get_current_user),
) -> List[AclScope]:
    principals: List[AclScope]
    principals = [Everyone, Authenticated]
    principals.extend(user.privileges())
    return principals


Permission = configure_permissions(
    get_current_user_privileges,
    HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorCode.INSUFFICIENT_PERMISSIONS,
    ),
)


# utilities


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

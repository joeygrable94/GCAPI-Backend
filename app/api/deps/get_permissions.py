from typing import Annotated, Any, List

from fastapi import Depends, HTTPException, Security, status

from app.api.exceptions import ErrorCode
from app.core.security import (
    Auth0User,
    UserRole,
    auth,
    configure_permissions,
    has_permission,
)
from app.core.security.permissions import (
    AclPermission,
    AclPrivilege,
    Authenticated,
    Everyone,
)
from app.crud import UserRepository
from app.models import User
from app.schemas import UserCreate
from app.schemas.user import UserRead

from .get_db import AsyncDatabaseSession


async def get_current_user(
    db: AsyncDatabaseSession,
    current_user: Auth0User | None = Security(auth.get_user),
) -> UserRead:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.UNAUTHORIZED,
        )
    users_repo: UserRepository = UserRepository(session=db)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=current_user.auth_id
    )
    if not user:
        user_roles: List[UserRole] = []
        if current_user.permissions:
            for user_perm in current_user.permissions:
                user_roles.append(UserRole[user_perm])
        user = await users_repo.create(
            UserCreate(
                auth_id=current_user.auth_id,
                email=current_user.email,
                username=current_user.email,
                is_superuser=False,
                is_verified=False,
                is_active=True,
                roles=user_roles,
            )
        )
    return UserRead.model_validate(user)


CurrentUser = Annotated[UserRead, Depends(get_current_user)]


def get_current_user_privileges(
    user: UserRead = Depends(get_current_user),
) -> List[AclPrivilege]:
    principals: List[AclPrivilege]
    principals = [Everyone, Authenticated]
    user_role: List[AclPrivilege] = getattr(user, "roles", [])
    user_privileges: List[AclPrivilege] = getattr(user, "privileges", [])
    user_permissions: List[AclPrivilege] = getattr(user, "permissions", [])
    principals.extend(user_role)
    principals.extend(user_privileges)
    principals.extend(user_permissions)
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
    current_user: UserRead,
    request_permission: AclPermission = AclPermission.read,
    request_data_model: Any = None,
) -> bool:
    if request_data_model is None:
        return False
    permissions: List[AclPrivilege] = get_current_user_privileges(current_user)
    return has_permission(permissions, request_permission, request_data_model)

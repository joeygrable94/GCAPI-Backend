from typing import Annotated

from fastapi import Depends, HTTPException, Security, status

from app.core.logger import logger
from app.db.constants import DB_STR_USER_PICTURE_DEFAULT
from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.auth.constants import (
    ERROR_MESSAGE_UNAUTHORIZED,
    ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
)
from app.entities.auth.controller import PermissionController
from app.entities.core_user.crud import UserRepository
from app.entities.core_user.model import User
from app.entities.core_user.schemas import UserCreate, UserUpdateAsManager
from app.services.clerk import ClerkUser, clerk_controller
from app.services.clerk.settings import clerk_settings
from app.services.permission import (
    AclPrivilege,
    Authenticated,
    Everyone,
    RoleUser,
    configure_permissions,
)
from app.utilities import get_uuid_str


def get_acl_scope_list(
    roles: list[str], permissions: list[str]
) -> list[AclPrivilege]:  # pragma: no cover
    user_scopes: list[AclPrivilege] = [RoleUser]
    if roles:
        for auth_role in roles:
            auth_scope = AclPrivilege(auth_role)
            if auth_scope not in user_scopes:
                user_scopes.append(auth_scope)
    if permissions:
        for auth_perm in permissions:
            auth_scope = AclPrivilege(auth_perm)
            if auth_scope not in user_scopes:
                user_scopes.append(auth_scope)
    return list(set(user_scopes))


async def get_current_user(
    db: AsyncDatabaseSession,
    auth_user: ClerkUser | None = Security(clerk_controller.get_user),
) -> User:
    if auth_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGE_UNAUTHORIZED,
        )
    if auth_user.is_verified is False:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
        )
    users_repo: UserRepository = UserRepository(session=db)
    current_user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=auth_user.auth_id
    )
    if auth_user.auth_id == clerk_settings.first_user_unverified_auth_id:
        auth_user.is_verified = False
    # auth_scopes = get_acl_scope_list(auth_user.roles, auth_user.permissions)
    if not current_user:
        new_username = auth_user.username or auth_user.email.split("@")[0]
        current_user = await users_repo.create(
            UserCreate(
                auth_id=auth_user.auth_id,
                email=auth_user.email,
                username=new_username + get_uuid_str()[:4],
                picture=auth_user.picture or DB_STR_USER_PICTURE_DEFAULT,
                scopes=[RoleUser],
                is_active=True,
                is_verified=auth_user.is_verified or False,
                is_superuser=False,
            )
        )
        logger.info(f"Created user: {current_user.id}")
    else:
        current_user = await users_repo.update(
            entry=current_user,
            schema=UserUpdateAsManager(is_verified=auth_user.is_verified or False),
        )
        if current_user:
            logger.info(f"Updated user: {current_user.id}")

    if current_user.is_verified is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
        )
    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_privileges(
    user: User = Depends(get_current_user),
) -> list[AclPrivilege]:
    principals: list[AclPrivilege]
    principals = [Everyone, Authenticated]
    principals.extend(user.privileges())
    scopes = list(set(principals))
    return scopes


Permission = configure_permissions(get_current_user_privileges)


def get_permission_controller(
    db: AsyncDatabaseSession,
    user: CurrentUser,
    privileges: list[AclPrivilege] = Depends(get_current_user_privileges),
) -> PermissionController:
    return PermissionController(db, user, privileges)

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
from app.entities.user.crud import UserRepository
from app.entities.user.model import User
from app.entities.user.schemas import UserCreate, UserUpdatePrivileges
from app.services.auth0 import AuthUser, auth_controller
from app.services.permission import (
    AclPrivilege,
    Authenticated,
    Everyone,
    RoleUser,
    configure_permissions,
)
from app.utilities import get_uuid_str


def get_acl_scope_list(roles: list[str], permissions: list[str]) -> list[AclPrivilege]:
    user_scopes: list[AclPrivilege] = [RoleUser]
    if roles:
        for auth0_role in roles:
            auth0_scope = AclPrivilege(auth0_role)
            if auth0_scope not in user_scopes:
                user_scopes.append(auth0_scope)
    if permissions:
        for auth0_perm in permissions:
            auth0_scope = AclPrivilege(auth0_perm)
            if auth0_scope not in user_scopes:
                user_scopes.append(auth0_scope)
    return list(set(user_scopes))


async def get_current_user(
    db: AsyncDatabaseSession,
    auth_user: AuthUser | None = Security(auth_controller.get_user),
) -> User:
    if auth_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGE_UNAUTHORIZED,
        )
    if auth_user.is_verified is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED,
        )
    users_repo: UserRepository = UserRepository(session=db)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=auth_user.auth_id
    )
    auth0_scopes = get_acl_scope_list(auth_user.roles, auth_user.permissions)
    if not user:
        new_username = auth_user.email.split("@")[0] + get_uuid_str()[:4]
        user = await users_repo.create(
            UserCreate(
                auth_id=auth_user.auth_id,
                email=auth_user.email,
                username=new_username,
                picture=auth_user.picture or DB_STR_USER_PICTURE_DEFAULT,
                scopes=auth0_scopes,
                is_active=True,
                is_verified=auth_user.is_verified or False,
                is_superuser=False,
            )
        )
        logger.info(f"Created user from Auth0: {user.id}")
    else:
        update_scopes = False
        new_scopes = user.scopes
        for scope in auth0_scopes:
            if scope not in user.scopes:
                update_scopes = True
                new_scopes.append(scope)
        if update_scopes:
            new_scopes = list(set(new_scopes))
            update_user = await users_repo.add_privileges(
                entry=user,
                schema=UserUpdatePrivileges(scopes=new_scopes),
            )
            if update_user:
                logger.info(f"Updated user scopes: {user.id}")
                return update_user
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_privileges(
    user: User = Depends(get_current_user),
) -> list[AclPrivilege]:
    principals: list[AclPrivilege]
    principals = [Everyone, Authenticated]
    principals.extend(user.privileges())
    return list(set(principals))


Permission = configure_permissions(get_current_user_privileges)


def get_permission_controller(
    db: AsyncDatabaseSession,
    user: CurrentUser,
    privileges: list[AclPrivilege] = Depends(get_current_user_privileges),
) -> PermissionController:
    return PermissionController(db, user, privileges)

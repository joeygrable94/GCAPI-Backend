from typing import Annotated, List

from fastapi import Depends, HTTPException, Security, status

from app.api.exceptions import ErrorCode
from app.core import logger
from app.core.security import Auth0User, auth
from app.core.security.permissions import AclPrivilege, RoleUser
from app.crud import UserRepository
from app.models import User
from app.schemas import UserCreate, UserUpdatePrivileges

from .get_db import AsyncDatabaseSession


def get_acl_scope_list(roles: List[str], permissions: List[str]) -> List[AclPrivilege]:
    user_scopes: List[AclPrivilege] = [RoleUser]
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
    auth0_user: Auth0User | None = Security(auth.get_user),
) -> User:
    if auth0_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.UNAUTHORIZED,
        )
    if auth0_user.is_verified is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorCode.UNVERIFIED_ACCESS_DENIED,
        )
    users_repo: UserRepository = UserRepository(session=db)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=auth0_user.auth_id
    )
    auth0_scopes = get_acl_scope_list(auth0_user.roles, auth0_user.permissions)
    if not user:
        user = await users_repo.create(
            UserCreate(
                auth_id=auth0_user.auth_id,
                email=auth0_user.email,
                username=auth0_user.email,
                picture=auth0_user.picture
                or "https://www.gravatar.com/avatar/?d=identicon",
                scopes=auth0_scopes,
                is_active=True,
                is_verified=auth0_user.is_verified or False,
                is_superuser=False,
            )
        )
        logger.info(f"Created user from Auth0: {user.id}")
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
        logger.info(f"Updated user scopes: {user.id}")
        if update_user:
            return update_user
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

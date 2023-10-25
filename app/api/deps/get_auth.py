from typing import Annotated, List

from fastapi import Depends, HTTPException, Security, status

from app.api.exceptions import ErrorCode
from app.core.logger import logger
from app.core.security import Auth0User, auth
from app.core.security.permissions import RoleUser, Scope
from app.crud import UserRepository
from app.models import User
from app.schemas import UserCreate
from app.schemas.user import UserUpdate

from .get_db import AsyncDatabaseSession


def get_acl_scope_list(roles: List[str], permissions: List[str]) -> List[Scope]:
    user_scopes: List[Scope] = [RoleUser]
    if roles:
        for auth0_role in roles:
            auth0_scope = Scope(auth0_role)
            if auth0_scope not in user_scopes:
                user_scopes.append(auth0_scope)
    if permissions:
        for auth0_perm in permissions:
            auth0_scope = Scope(auth0_perm)
            if auth0_scope not in user_scopes:
                user_scopes.append(auth0_scope)
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
    logger.info("Auth0 User:", auth0_user)
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
                scopes=auth0_scopes,
                is_superuser=False,
                is_verified=False,
                is_active=True,
            )
        )
    update_scopes = False
    new_scopes = user.scopes
    for scope in auth0_scopes:
        if scope not in user.scopes:
            update_scopes = True
            new_scopes.append(scope)
    if update_scopes:
        update_user = await users_repo.update(
            entry=user, schema=UserUpdate(scopes=new_scopes)
        )
        logger.info(f"Updated user scopes: {user.id} {new_scopes}")
        if update_user:
            return update_user
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

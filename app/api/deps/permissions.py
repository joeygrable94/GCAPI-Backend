from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi_auth0 import Auth0User
from fastapi_permissions import Authenticated  # type: ignore
from fastapi_permissions import Everyone, configure_permissions

from app.api.errors import ErrorCode
from app.core.auth import auth


def get_current_user(user: Auth0User | None = Security(auth.get_user)) -> Auth0User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.UNAUTHORIZED,
        )
    return user


CurrentUser = Annotated[Auth0User, Depends(get_current_user)]


def get_active_principals(user: CurrentUser | None) -> list:
    if user:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(getattr(user, "permissions", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals


Permission = configure_permissions(get_active_principals)

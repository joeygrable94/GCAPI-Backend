from typing import Annotated, Any, List

from fastapi import Depends, HTTPException, Security, status
from fastapi_permissions import Authenticated  # type: ignore  # noqa: E501
from fastapi_permissions import Everyone, configure_permissions, has_permission

from app.api.errors import ErrorCode
from app.core.auth import Auth0User, auth


def get_current_user(user: Auth0User | None = Security(auth.get_user)) -> Auth0User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.UNAUTHORIZED,
        )
    return user


CurrentUser = Annotated[Auth0User, Depends(get_current_user)]


def get_current_user_permissions(
    user: Auth0User = Depends(get_current_user),
) -> List[str]:
    if user:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(getattr(user, "permissions", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals


Permissions = configure_permissions(
    get_current_user_permissions,
    HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorCode.INSUFFICIENT_PERMISSIONS,
    ),
)


def get_current_user_authorization(
    current_user: Auth0User,
    request_permission: str = "access",
    request_data_model: Any = None,
) -> bool:
    if request_data_model is None:
        return False
    permissions: List[str] = get_current_user_permissions(current_user)
    return has_permission(permissions, request_permission, request_data_model)

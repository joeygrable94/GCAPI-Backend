from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.errors import ErrorCode
from app.api.exceptions import (
    InvalidPasswordException,
    UserAlreadyExists,
    UserNotExists,
)
from app.api.openapi import (
    delete_user_responses,
    get_all_users_responses,
    get_user_or_404_responses,
    get_user_reponses,
    update_user_me_responses,
    update_user_responses,
)
from app.db.schemas import UserRead, UserUpdate
from app.db.tables import User
from app.security import (
    AuthManager,
    get_current_active_superuser,
    get_current_active_user,
    get_user_auth,
    get_user_or_404,
)

router = APIRouter()


@router.get(
    "/me",
    name="users:current_user",
    dependencies=[Depends(get_current_active_user)],
    responses=get_user_or_404_responses,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: UserRead = Depends(get_current_active_user),
) -> UserRead:
    """
    Allows current-active-verified-users to fetch the details on their account.
    """
    return current_user


@router.patch(
    "/me",
    name="users:patch_current_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_auth),
    ],
    responses=update_user_me_responses,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def update_me(
    user_update: UserUpdate,
    current_user: UserRead = Depends(get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
) -> UserRead:
    """
    Allows current-active-verified-users to update their account.
    """
    try:  # pragma: no cover
        user: Optional[User] = await oauth.users.read_by_email(email=current_user.email)
        if not user:
            raise UserNotExists()
        updated_user: User = await oauth.users.update(entry=user, schema=user_update)
        return UserRead.from_orm(updated_user)
    except UserNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.USER_NOT_FOUND,
        )
    except UserAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USER_ALREADY_EXISTS,
        )
    except InvalidPasswordException as e:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.USER_PASSWORD_INVALID,
                "reason": e.reason,
            },
        )


@router.get(
    "/",
    name="users:list_users",
    dependencies=[
        Depends(get_current_active_superuser),
        Depends(get_user_auth),
    ],
    responses=get_all_users_responses,
    response_model=Union[List[UserRead], List[None]],
    status_code=status.HTTP_200_OK,
)
async def get_users_list(
    page: int = 1,
    current_super_user: UserRead = Depends(get_current_active_superuser),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[List[UserRead], List]:
    """
    Allows current-active-verified-superusers to fetch a list of users
    in a paginated output.

    The default number of users per page is configured in the settings.
    """
    page = 1 if page < 1 else page
    users: Optional[Union[List[User], List[None]]] = await oauth.users.list(page=page)
    if users and len(users):  # pragma: no cover
        return [UserRead.from_orm(u) for u in users]
    return list()  # pragma: no cover


@router.get(
    "/{id}",
    name="users:user",
    dependencies=[
        Depends(get_current_active_superuser),
        Depends(get_user_or_404),
    ],
    responses=get_user_reponses,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    current_super_user: UserRead = Depends(get_current_active_superuser),
    fetch_user: User = Depends(get_user_or_404),
) -> UserRead:
    """
    Allows current-active-verified-superusers may fetch a spectific user
    by their ID/UUID attribute.

    We do not want to be sending sending requests with user emails,
    leaving them potential at risk of being exposed to the public.
    """
    return UserRead.from_orm(fetch_user)


@router.patch(
    "/{id}",
    name="users:patch_user",
    dependencies=[
        Depends(get_current_active_superuser),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    responses=update_user_responses,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_update: UserUpdate,
    current_super_user: UserRead = Depends(get_current_active_superuser),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> UserRead:
    """
    Allows current-active-verified-superusers to request to update a user
    by their ID/UUID attribute.
    """
    try:
        user: User = await oauth.users.update(fetch_user, user_update)
        return UserRead.from_orm(user)  # pragma: no cover
    except UserAlreadyExists:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USER_ALREADY_EXISTS,
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.USER_PASSWORD_INVALID,
                "reason": e.reason,
            },
        )


@router.delete(
    "/{id}",
    name="users:delete_user",
    dependencies=[
        Depends(get_current_active_superuser),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    responses=delete_user_responses,
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    current_super_user: UserRead = Depends(get_current_active_superuser),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> Any:
    """
    Allows current-active-verified-superusers to delete a user
    by their ID/UUID attribute.
    """
    print(fetch_user)
    await oauth.users.delete(fetch_user)
    return None

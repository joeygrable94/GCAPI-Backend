from typing import List, Optional, Union

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
from app.core.config import Settings, get_settings
from app.core.logger import logger
from app.db.schemas import UserCreate, UserRead, UserReadAdmin, UserUpdate
from app.db.tables import User
from app.security import (
    AuthManager,
    Permission,
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
    response_model=Union[UserReadAdmin, UserRead],
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: UserReadAdmin = Permission("self", get_current_active_user),
) -> Union[UserReadAdmin, UserRead]:
    """
    Allows current-active-verified-users to fetch the details on their account.
    """
    if current_user.is_superuser:
        return current_user
    else:
        return UserRead.from_orm(current_user)


@router.patch(
    "/me",
    name="users:patch_current_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_auth),
    ],
    responses=update_user_me_responses,
    response_model=Union[UserReadAdmin, UserRead],
    status_code=status.HTTP_200_OK,
)
async def update_me(
    user_update: UserUpdate,
    current_user: UserReadAdmin = Permission("self", get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[UserReadAdmin, UserRead]:
    """
    Allows current-active-verified-users to update their account.
    """
    try:  # pragma: no cover
        user: Optional[User] = await oauth.users.read_by_email(email=current_user.email)
        if not user:
            raise UserNotExists()
        updated_user: User = await oauth.users.update(entry=user, schema=user_update)
        if updated_user.is_superuser:
            return UserReadAdmin.from_orm(updated_user)
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
        Depends(get_current_active_user),
        Depends(get_user_auth),
    ],
    responses=get_all_users_responses,
    response_model=Union[List[UserReadAdmin], List[UserRead], List],
    status_code=status.HTTP_200_OK,
)
async def get_users_list(
    page: int = 1,
    current_user: UserReadAdmin = Permission("list", get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[List[UserReadAdmin], List[UserRead], List]:
    """
    Allows current-active-verified-superusers to fetch a list of users
    in a paginated output.

    The default number of users per page is configured in the settings.
    """
    page = 1 if page < 1 else page
    users: Optional[Union[List[User], List[None]]] = await oauth.users.list(page=page)
    if users and len(users):  # pragma: no cover
        if current_user.is_superuser:
            return [UserReadAdmin.from_orm(u) for u in users]
        else:
            return [UserRead.from_orm(u) for u in users]
    else:
        return list()  # pragma: no cover


@router.post(
    "/",
    name="users:create_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_auth),
    ],
    # responses=create_user_responses,
    response_model=Union[UserReadAdmin, UserRead],
    status_code=status.HTTP_200_OK,
)
async def create_user(
    user_create: UserCreate,
    current_user: UserReadAdmin = Permission("create", get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Union[UserReadAdmin, UserRead]:
    """
    Creates a new user, un-verified by default.
    """
    try:
        created_user: User = await oauth.users.create(schema=user_create)
        new_user: UserReadAdmin = UserReadAdmin.from_orm(
            created_user
        )  # pragma: no cover
        if settings.DEBUG_MODE:  # pragma: no cover
            logger.info(f"User {new_user.id} was created.")
        if current_user.is_superuser:  # pragma: no cover
            return UserReadAdmin.from_orm(new_user)
        else:
            return UserRead.from_orm(new_user)  # pragma: no cover
    except UserAlreadyExists:  # pragma: no cover
        raise HTTPException(
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


@router.get(
    "/{id}",
    name="users:user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_or_404),
    ],
    responses=get_user_reponses,
    response_model=Union[UserReadAdmin, UserRead],
    status_code=status.HTTP_200_OK,
)
async def get_user(
    current_user: UserReadAdmin = Permission("read", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
) -> Union[UserReadAdmin, UserRead]:
    """
    Allows current-active-verified-superusers may fetch a spectific user
    by their ID/UUID attribute.

    We do not want to be sending sending requests with user emails,
    leaving them potential at risk of being exposed to the public.
    """
    if current_user.is_superuser:
        return UserReadAdmin.from_orm(fetch_user)  # pragma: no cover
    else:
        return UserRead.from_orm(fetch_user)  # pragma: no cover


@router.patch(
    "/{id}",
    name="users:patch_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    responses=update_user_responses,
    response_model=Union[UserReadAdmin, UserRead],
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_update: UserUpdate,
    current_user: UserReadAdmin = Permission("update", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[UserReadAdmin, UserRead]:
    """
    Allows current-active-verified-superusers to request to update a user
    by their ID/UUID attribute.
    """
    try:
        user: User = await oauth.users.update(fetch_user, user_update)
        if current_user.is_superuser:  # pragma: no cover
            return UserReadAdmin.from_orm(user)
        else:
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
        Depends(get_current_active_user),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    responses=delete_user_responses,
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    current_user: UserReadAdmin = Permission("delete", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> None:
    """
    Allows current-active-verified-superusers to delete a user
    by their ID/UUID attribute.
    """
    await oauth.users.delete(fetch_user)
    return None

from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.errors import ErrorCode
from app.api.exceptions import (
    ApiAuthException,
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
from app.db.schemas import (
    UserAdmin,
    UserCreate,
    UserRead,
    UserUpdate,
    UserUpdateAuthPermissions,
)
from app.db.schemas.user import UserAdminRelations, UserReadRelations
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
    response_model=Union[UserAdminRelations, UserReadRelations],
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: UserAdmin = Permission("self", get_current_active_user),
) -> Union[UserAdmin, UserRead]:
    """
    Allows current-active-verified-users to fetch the details on their account.
    """
    if current_user.is_superuser:
        return UserAdmin.from_orm(current_user)
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
    response_model=Union[UserAdminRelations, UserReadRelations],
    status_code=status.HTTP_200_OK,
)
async def update_me(
    user_update: UserUpdate,
    current_user: UserAdmin = Permission("self", get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[UserAdmin, UserRead]:
    """
    Allows current-active-verified-users to update their account.
    """
    try:  # pragma: no cover
        user: Optional[User] = await oauth.users.read_by_email(email=current_user.email)
        if not user:
            raise UserNotExists()
        updated_user: User = await oauth.users.update(entry=user, schema=user_update)
        if updated_user.is_superuser:
            return UserAdmin.from_orm(updated_user)
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
    response_model=Union[List[UserAdminRelations], List[UserReadRelations], List],
    status_code=status.HTTP_200_OK,
)
async def get_users_list(
    page: int = 1,
    current_user: UserAdmin = Permission("list", get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[List[UserAdmin], List[UserRead], List]:
    """
    Allows current-active-verified-superusers to fetch a list of users
    in a paginated output.

    The default number of users per page is configured in the settings.
    """
    page = 1 if page < 1 else page
    users: Optional[Union[List[User], List[None]]] = await oauth.users.list(page=page)
    if users and len(users):  # pragma: no cover
        if current_user.is_superuser:
            return [UserAdmin.from_orm(u) for u in users]
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
    response_model=Union[UserAdminRelations, UserReadRelations],
    status_code=status.HTTP_200_OK,
)
async def create_user(
    user_create: UserCreate,
    current_user: UserAdmin = Permission("create", get_current_active_user),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Union[UserAdmin, UserRead]:
    """
    Creates a new user, un-verified by default.
    """
    try:
        created_user: User = await oauth.users.create(schema=user_create)
        new_user: UserAdmin = UserAdmin.from_orm(created_user)  # pragma: no cover
        if settings.DEBUG_MODE:  # pragma: no cover
            logger.info(f"User {new_user.id} was created.")
        if current_user.is_superuser:  # pragma: no cover
            return UserAdmin.from_orm(new_user)
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
    response_model=Union[UserAdminRelations, UserReadRelations],
    status_code=status.HTTP_200_OK,
)
async def get_user(
    current_user: UserAdmin = Permission("read", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
) -> Union[UserAdmin, UserRead]:
    """
    Allows current-active-verified-superusers may fetch a spectific user
    by their ID/UUID attribute.

    We do not want to be sending sending requests with user emails,
    leaving them potential at risk of being exposed to the public.
    """
    if current_user.is_superuser:
        return UserAdmin.from_orm(fetch_user)  # pragma: no cover
    else:
        return UserRead.from_orm(fetch_user)  # pragma: no cover


@router.patch(
    "/{id}",
    name="users:update_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    responses=update_user_responses,
    response_model=Union[UserAdminRelations, UserReadRelations],
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_update: UserUpdate,
    current_user: UserAdmin = Permission("update", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> Union[UserAdmin, UserRead]:
    """
    Allows current-active-verified-superusers to request to update a user
    by their ID/UUID attribute.
    """
    try:
        user: User = await oauth.users.update(fetch_user, user_update)
        if current_user.is_superuser:  # pragma: no cover
            return UserAdmin.from_orm(user)
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
    current_user: UserAdmin = Permission("delete", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> None:
    """
    Allows current-active-verified-superusers to delete a user
    by their ID/UUID attribute.
    """
    await oauth.users.delete(fetch_user)
    return None


@router.patch(
    "/{id}/permissions/add",
    name="users:add_permissions_to_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    # responses=add_permissions_to_user_responses,
    response_model=UserAdminRelations,
    status_code=status.HTTP_200_OK,
)
async def add_user_permissions(
    user_update_permissions: UserUpdateAuthPermissions,
    current_user: UserAdmin = Permission("super", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> UserAdmin:
    try:
        if not current_user.is_superuser:
            raise ApiAuthException(reason="permission denied")  # pragma: no cover
        user: User = await oauth.users.updatePermissions(
            fetch_user, user_update_permissions, method="add"
        )
        return UserAdmin.from_orm(user)  # pragma: no cover
    except ApiAuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.reason,
        )


@router.patch(
    "/{id}/permissions/remove",
    name="users:remove_permissions_from_user",
    dependencies=[
        Depends(get_current_active_user),
        Depends(get_user_or_404),
        Depends(get_user_auth),
    ],
    # responses=remove_permissions_from_user_responses,
    response_model=UserAdminRelations,
    status_code=status.HTTP_200_OK,
)
async def remove_user_permissions(
    user_update_permissions: UserUpdateAuthPermissions,
    current_user: UserAdmin = Permission("super", get_current_active_user),
    fetch_user: User = Depends(get_user_or_404),
    oauth: AuthManager = Depends(get_user_auth),
) -> UserAdmin:
    try:
        if not current_user.is_superuser:
            raise ApiAuthException(reason="permission denied")  # pragma: no cover
        user: User = await oauth.users.updatePermissions(
            fetch_user, user_update_permissions, method="remove"
        )
        return UserAdmin.from_orm(user)  # pragma: no cover
    except ApiAuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.reason,
        )


# users_tokens_read
# users_clients_read

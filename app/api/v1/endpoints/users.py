from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchUserOr404,
    GetPageQueryParams,
    get_async_db,
    get_current_user,
    get_user_or_404,
)
from app.api.errors import ErrorCode
from app.api.exceptions import UserAlreadyExists

# from app.api.openapi import users_read_responses
from app.core.auth import auth
from app.crud.user import UserRepository
from app.models.user import User
from app.schemas import UserCreate, UserRead, UserReadRelations, UserRole, UserUpdate

router: APIRouter = APIRouter()


@router.get(
    "/me",
    name="users:current",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
    ],
    response_model=UserRead | None,
)
async def users_current(
    db: AsyncDatabaseSession,
    current_user: CurrentUser,
) -> UserRead | None:
    """Retrieve the profile information about the currently active, verified user.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `UserRead | None` : a dictionary containing the user profile information

    """
    users_repo: UserRepository = UserRepository(session=db)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=current_user.auth_id
    )
    if not user:
        user_roles: List[UserRole] = (
            current_user.roles if current_user.roles else [UserRole.USER]
        )
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


@router.get(
    "/",
    name="users:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[UserReadRelations],
)
async def users_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetPageQueryParams,
) -> List[UserRead] | List:
    """Retrieve a list of users.

    Permissions:
    ------------
    `role=admin|manager` : all users

    `role=client` : all users associated with the client through the `user_client` table

    `role=employee` : users associated with clients they are associated with in
        `user_client` table

    Returns:
    --------
    `List[UserRead] | List[None]` : a list of users, optionally filtered, or returns
        an empty list

    """
    # can_access = get_current_user_authorization(current_user, "access", UserRead)
    users_repo: UserRepository = UserRepository(session=db)
    users: List[User] | List[None] | None = await users_repo.list(page=query.page)
    return [UserRead.model_validate(c) for c in users] if users else []


@router.get(
    "/{user_id}",
    name="users:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    # responses=users_read_responses,
    response_model=UserReadRelations,
)
async def users_read(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user: FetchUserOr404,
) -> UserRead:
    """Retrieve a single user by id.

    Permissions:
    ------------
    `role=admin|manager` : all users

    `role=client` : all users associated with the client through the `user_client`
        table

    `role=employee` : all users associated with any clients they are associated with
        through the `user_client`

    `role=user` : only their own user profile id

    Returns:
    --------
    `UserRead` : a dictionary containing the user profile information

    - `role=admin|manager` : all fields
    - `role=client|employee|user` : all fields except `is_superuser`

    """
    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}",
    name="users:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    response_model=UserReadRelations,
)
async def users_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user: FetchUserOr404,
    user_in: UserUpdate,
) -> UserRead:
    """Update a user by id. Users may update limited fields of their own data,
    and maybe the fields of other users depending on their role.

    Permissions:
    ------------
    `role=admin|manager` : all users

    `role=user` : only their own user profile id

    Returns:
    --------
    `UserRead` : the updated user

    - `role=admin` : all fields
    - `role=manager` : all fields except `is_superuser`
    - `role=user` : can only update non-sensitive profile information like: `username`

    """
    try:
        users_repo: UserRepository = UserRepository(session=db)
        if user_in.username is not None:
            a_user: User | None = await users_repo.read_by(
                field_name="username", field_value=user_in.username
            )
            if a_user:
                raise UserAlreadyExists()
        updated_user: User | None = await users_repo.update(entry=user, schema=user_in)
        return (
            UserRead.model_validate(updated_user)
            if updated_user
            else UserRead.model_validate(user)
        )
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USERNAME_EXISTS,
        )


@router.delete(
    "/{user_id}",
    name="users:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    response_model=None,
)
async def users_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user: FetchUserOr404,
) -> None:
    """Delete a user by id.

    Permissions:
    ------------
    `role=admin` : all users

    `role=user` : may request to have their profile and all associated data deleted

    Returns:
    --------
    `None`

    """
    users_repo: UserRepository = UserRepository(session=db)
    await users_repo.delete(entry=user)
    return None

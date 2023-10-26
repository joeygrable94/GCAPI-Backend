from typing import Union

from fastapi import APIRouter, Depends, Request

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_request_client_ip,
    get_user_or_404,
)
from app.api.exceptions import UserAlreadyExists

# from app.api.openapi import users_read_responses
from app.core.pagination import PagedResponseSchema, PageParams, paginate
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessRead,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateSelf,
    RoleAdmin,
    RoleManager,
)
from app.core.security.permissions.access import Authenticated
from app.crud.user import UserRepository
from app.models import User
from app.schemas import UserRead, UserReadAsAdmin, UserReadAsManager, UserUpdate

router: APIRouter = APIRouter()


@router.get(
    "/me",
    name="users:current",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
    ],
    response_model=UserRead,
)
async def users_current(
    request: Request,
    db: AsyncDatabaseSession,
    current_user: User = Permission([AccessRead, AccessReadSelf], get_current_user),
    request_ip: str = Depends(get_request_client_ip),
) -> UserRead:
    """Retrieve the profile information about the currently active, verified user.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `UserRead` : a dictionary containing the user profile information

    """
    # set session vars
    request.session["user_id"] = str(current_user.id)
    req_sess_ip = request.session.get("ip_address", False)
    if not req_sess_ip:
        request.session["ip_address"] = str(request_ip)
    return UserRead.model_validate(current_user)


@router.get(
    "/",
    name="users:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=PagedResponseSchema[UserReadAsAdmin]
    | PagedResponseSchema[UserReadAsManager],
)
async def users_list(
    db: AsyncDatabaseSession,
    page_params: PageParams = Depends(PageParams),
    acl: PermissionController = Depends(get_permission_controller),
) -> PagedResponseSchema[UserReadAsAdmin] | PagedResponseSchema[UserReadAsManager]:
    """Retrieve a list of users.

    Permissions:
    ------------
    `role=admin|manager` : all users

    Returns:
    --------
    `List[UserRead] | List[None]` : a list of users, optionally filtered, or returns
        an empty list

    """
    users_repo: UserRepository = UserRepository(session=db)
    # users: List[User] | List[None] | None
    # users = await users_repo.list(page=query.page)
    # return [UserRead.model_validate(c) for c in users] if users else []
    response_out: PagedResponseSchema[UserReadAsAdmin] | PagedResponseSchema[
        UserReadAsManager
    ] = acl.get_resource_response(
        responses={
            RoleAdmin: await paginate(
                table_name=users_repo._table.__tablename__,
                db=db,
                stmt=users_repo.query_list(),
                page_params=page_params,
                response_schema=UserReadAsAdmin,
            ),
            RoleManager: await paginate(
                table_name=users_repo._table.__tablename__,
                db=db,
                stmt=users_repo.query_list(),
                page_params=page_params,
                response_schema=UserReadAsAdmin,
            ),
        },
    )
    return response_out


@router.get(
    "/{user_id}",
    name="users:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_user_or_404),
    ],
    # responses=users_read_responses,
    response_model=Union[UserReadAsAdmin, UserReadAsManager, UserRead],
)
async def users_read(
    db: AsyncDatabaseSession,
    current_user: CurrentUser,
    user: User = Permission([AccessRead, AccessReadSelf], get_user_or_404),
    acl: PermissionController = Depends(get_permission_controller),
) -> Union[UserReadAsAdmin, UserReadAsManager, UserRead]:
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
    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        acl.get_resource_response(
            responses={
                RoleAdmin: UserReadAsAdmin.model_validate(user),
                RoleManager: UserReadAsManager.model_validate(user),
                Authenticated: UserRead.model_validate(user),
            },
        )
    )
    return response_out


@router.patch(
    "/{user_id}",
    name="users:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    response_model=UserRead,
)
async def users_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user_in: UserUpdate,
    user: User = Permission([AccessUpdate, AccessUpdateSelf], get_user_or_404),
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
    user: User = Permission(AccessDelete, get_user_or_404),
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

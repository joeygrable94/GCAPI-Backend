from typing import Union

from fastapi import APIRouter, Depends, Request

from app.api.deps import (
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
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteSelf,
    AccessRead,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateSelf,
    RoleAdmin,
    RoleManager,
)
from app.core.security.permissions.access import Authenticated
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
        Depends(get_permission_controller),
        Depends(get_request_client_ip),
    ],
    response_model=Union[UserReadAsAdmin, UserReadAsManager, UserRead],
)
async def users_current(
    request: Request,
    acl: PermissionController = Depends(get_permission_controller),
    request_ip: str = Depends(get_request_client_ip),
) -> UserReadAsAdmin | UserReadAsManager | UserRead:
    """Retrieve the profile information about the currently active, verified user.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    a dictionary containing the user profile information

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role
    - `UserRead` : only publically accessible fields

    """
    # set session vars
    request.session["user_id"] = str(acl.user.id)
    req_sess_ip = request.session.get("ip_address", False)
    if not req_sess_ip:
        request.session["ip_address"] = str(request_ip)
    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        acl.get_resource_response(
            resource=acl.user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
                Authenticated: UserRead,
            },
        )
    )
    return response_out


@router.get(
    "/",
    name="users:list",
    dependencies=[
        Depends(PageParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Union[Paginated[UserReadAsAdmin], Paginated[UserReadAsManager]],
)
async def users_list(
    page_params: PageParams = Depends(PageParams),
    acl: PermissionController = Depends(get_permission_controller),
) -> Paginated[UserReadAsAdmin] | Paginated[UserReadAsManager]:
    """Retrieve a paginated list of users.

    Permissions:
    ------------
    `role=admin` : all users

    `role=manager` : all users

    Returns:
    --------
    a paginated response containing a list of users

    - `Paginated[UserReadAsAdmin]` : all fields
    - `Paginated[UserReadAsManager]` : only fields accessibile to the
        manager role

    """
    response_out: Paginated[UserReadAsAdmin] | Paginated[
        UserReadAsManager
    ] = await acl.get_paginated_resource_response(
        table_name=acl.user_repo._table.__tablename__,
        stmt=acl.user_repo.query_list(),
        page_params=page_params,
        responses={
            RoleAdmin: UserReadAsAdmin,
            RoleManager: UserReadAsManager,
        },
    )
    return response_out


@router.get(
    "/{user_id}",
    name="users:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    # responses=users_read_responses,
    response_model=Union[UserReadAsAdmin, UserReadAsManager, UserRead],
)
async def users_read(
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
    a dictionary containing the user profile information

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role
    - `UserRead` : only publically accessible fields

    """
    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        acl.get_resource_response(
            resource=user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
                Authenticated: UserRead,
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
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Union[UserReadAsAdmin, UserReadAsManager, UserRead],
)
async def users_update(
    user_in: UserUpdate,
    user: User = Permission([AccessUpdate, AccessUpdateSelf], get_user_or_404),
    acl: PermissionController = Depends(get_permission_controller),
) -> UserReadAsAdmin | UserReadAsManager | UserRead:
    """Update a user by id. Users may update limited fields of their own data,
    and maybe the fields of other users depending on their role.

    Permissions:
    ------------
    `role=admin|manager` : all users

    `role=user` : only their own user profile id

    Returns:
    --------
    the updated user object

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role
    - `UserRead` : only publically accessible fields

    """
    # users_repo: UserRepository = UserRepository(session=acl.db)
    if user_in.username is not None:
        a_user: User | None = await acl.user_repo.read_by(
            field_name="username", field_value=user_in.username
        )
        if a_user:
            raise UserAlreadyExists()
    updated_user: User | None = await acl.user_repo.update(entry=user, schema=user_in)
    user_out = updated_user or user
    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        acl.get_resource_response(
            resource=user_out,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
                Authenticated: UserRead,
            },
        )
    )
    return response_out


@router.delete(
    "/{user_id}",
    name="users:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
    ],
    response_model=None,
)
async def users_delete(
    user: User = Permission([AccessDelete, AccessDeleteSelf], get_user_or_404),
    acl: PermissionController = Depends(get_permission_controller),
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
    # TODO: add logic to request user deletion if AclPermission is AccessDeleteSelf
    await acl.user_repo.delete(entry=user)
    return None

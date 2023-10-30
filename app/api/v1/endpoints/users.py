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
    Authenticated,
    RoleAdmin,
    RoleManager,
)
from app.models import User
from app.schemas import (
    UserRead,
    UserReadAsAdmin,
    UserReadAsManager,
    UserUpdate,
    UserUpdateAsAdmin,
    UserUpdateAsManager,
)
from app.worker import task_request_to_delete_user

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
    response_model=UserRead | UserReadAsManager | UserReadAsAdmin,
)
async def users_current(
    request: Request,
    permissions: PermissionController = Depends(get_permission_controller),
    request_ip: str = Depends(get_request_client_ip),
) -> UserRead | UserReadAsManager | UserReadAsAdmin:
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
    request.session["user_id"] = str(permissions.current_user.id)
    req_sess_ip = request.session.get("ip_address", False)
    if not req_sess_ip:
        request.session["ip_address"] = str(request_ip)
    # return role based response
    response_out: UserRead | UserReadAsManager | UserReadAsAdmin = (
        permissions.get_resource_response(
            resource=permissions.current_user,
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
    response_model=Paginated[UserReadAsManager] | Paginated[UserReadAsAdmin],
)
async def users_list(
    page_params: PageParams = Depends(PageParams),
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[UserReadAsManager] | Paginated[UserReadAsAdmin]:
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
    response_out: Paginated[UserReadAsManager] | Paginated[
        UserReadAsAdmin
    ] = await permissions.get_paginated_resource_response(
        table_name=permissions.user_repo._table.__tablename__,
        stmt=permissions.user_repo.query_list(),
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
    response_model=UserRead | UserReadAsManager | UserReadAsAdmin,
)
async def users_read(
    user: User = Permission([AccessRead, AccessReadSelf], get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserRead | UserReadAsManager | UserReadAsAdmin:
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
    # verify current user has permission to update the user
    await permissions.verify_user_can_access(user_id=user.id)
    # return role based response
    response_out: UserRead | UserReadAsManager | UserReadAsAdmin = (
        permissions.get_resource_response(
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
    response_model=UserRead | UserReadAsManager | UserReadAsAdmin,
)
async def users_update(
    user_in: UserUpdate,
    user: User = Permission([AccessUpdate, AccessUpdateSelf], get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserRead | UserReadAsManager | UserReadAsAdmin:
    """Update a user by id. Users may update limited fields of their own data,
    and maybe the fields of other users depending on their role.

    Permissions:
    ------------
    `role=admin` : all users, all fields

    `role=manager` : all users, limited fields

    `role=user` : only their own public profile fields

    Returns:
    --------
    the updated user object

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role
    - `UserRead` : only publically accessible fields

    """
    # verify current user has permission to update the user
    await permissions.verify_user_can_access(user_id=user.id)
    # check user to be updated exists
    if user_in.username is not None:
        a_user: User | None = await permissions.user_repo.read_by(
            field_name="username", field_value=user_in.username
        )
        if a_user:
            raise UserAlreadyExists()
    # update the user data
    updated_user: User | None = await permissions.user_repo.update(
        entry=user, schema=user_in
    )
    user_out = updated_user or user
    # return role based response
    response_out: UserRead | UserReadAsManager | UserReadAsAdmin = (
        permissions.get_resource_response(
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
    permissions: PermissionController = Depends(get_permission_controller),
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
    # verify current user has permission to update the user
    await permissions.verify_user_can_access(user_id=user.id)
    if RoleAdmin in permissions.privileges:
        await permissions.user_repo.delete(entry=user)
    elif permissions.current_user.id == user.id:
        task_request_to_delete_user.delay(user_id=user.id)
    return None


@router.patch(
    "/{user_id}/privileges/add",
    name="users:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsManager | UserReadAsAdmin,
)
async def users_update_add_privileges(
    user_in: UserUpdateAsManager | UserUpdateAsAdmin,
    user: User = Permission(AccessUpdate, get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserReadAsManager | UserReadAsAdmin:
    # verify the input schema is valid for the current users role
    permissions.verify_input_schema_by_role(
        input_object=user_in,
        schema_privileges={
            RoleAdmin: UserUpdateAsAdmin,
            RoleManager: UserUpdateAsManager,
        },
    )
    # verify current user has permission to update the user
    await permissions.verify_user_can_access(user_id=user.id)
    # update the user data
    updated_user: User = await permissions.add_privileges(user, user_in)
    # return role based response
    response_out: UserReadAsAdmin | UserReadAsManager = (
        permissions.get_resource_response(
            resource=updated_user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
            },
        )
    )
    return response_out


@router.patch(
    "/{user_id}privileges/remove",
    name="users:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsManager | UserReadAsAdmin,
)
async def users_update_remove_privileges(
    user_in: UserUpdateAsManager | UserUpdateAsAdmin,
    user: User = Permission(AccessUpdate, get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserReadAsManager | UserReadAsAdmin:
    # verify the input schema is valid for the current users role
    permissions.verify_input_schema_by_role(
        input_object=user_in,
        schema_privileges={
            RoleAdmin: UserUpdateAsAdmin,
            RoleManager: UserUpdateAsManager,
        },
    )
    # verify current user has permission to update the user
    await permissions.verify_user_can_access(user_id=user.id)
    # update the user data
    updated_user: User = await permissions.remove_privileges(user, user_in)
    # return role based response
    response_out: UserReadAsAdmin | UserReadAsManager = (
        permissions.get_resource_response(
            resource=updated_user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
            },
        )
    )
    return response_out

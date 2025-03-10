from fastapi import APIRouter, BackgroundTasks, Depends, Request

from app.core.pagination import (
    GetPaginatedQueryParams,
    PageParams,
    PageParamsFromQuery,
    Paginated,
)
from app.entities.api.dependencies import get_async_db
from app.entities.auth.dependencies import (
    Permission,
    PermissionController,
    get_current_user,
    get_permission_controller,
)
from app.entities.core_ipaddress.dependencies import (
    RequestOrganizationIp,
    get_request_ip,
)
from app.entities.core_user.dependencies import get_user_or_404
from app.entities.core_user.errors import UserAlreadyExists
from app.entities.core_user.model import User
from app.entities.core_user.schemas import (
    UserDelete,
    UserRead,
    UserReadAsAdmin,
    UserReadAsManager,
    UserUpdate,
    UserUpdateAsAdmin,
    UserUpdateAsManager,
    UserUpdatePrivileges,
)
from app.services.permission import (
    AccessDelete,
    AccessDeleteSelf,
    AccessRead,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateSelf,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.tasks.background import (
    bg_task_request_to_delete_user,
    bg_task_track_user_ipinfo,
)

router: APIRouter = APIRouter()


@router.get(
    "/me",
    name="users:current",
    dependencies=[
        Depends(get_request_ip),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsAdmin | UserReadAsManager | UserRead,
)
async def users_current(
    bg_tasks: BackgroundTasks,
    request: Request,
    request_ip: RequestOrganizationIp,
    permissions: PermissionController = Depends(get_permission_controller),
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
    request.session["user_id"] = str(permissions.current_user.id)
    req_sess_ip = request.session.get("ip_address", False)
    if not req_sess_ip:
        request.session["ip_address"] = request_ip
        bg_tasks.add_task(
            bg_task_track_user_ipinfo,
            ip_address=str(request_ip),
            user_id=str(permissions.current_user.id),
        )

    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        permissions.get_resource_response(
            resource=permissions.current_user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
                RoleUser: UserRead,
            },
        )
    )
    return response_out


@router.get(
    "/",
    name="users:list",
    dependencies=[
        Depends(PageParamsFromQuery),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[UserReadAsAdmin | UserReadAsManager],
)
async def users_list(
    query: GetPaginatedQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[UserReadAsAdmin | UserReadAsManager]:
    """Retrieve a paginated list of users.

    Permissions:
    ------------
    `role=admin|manager` : all users

    Returns:
    --------
    a paginated response containing a list of users

    - `Paginated[UserReadAsAdmin]` : all fields
    - `Paginated[UserReadAsManager]` : only fields accessibile to the
        manager role

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])

    response_out: Paginated[
        UserReadAsAdmin | UserReadAsManager
    ] = await permissions.get_paginated_resource_response(
        table_name=permissions.user_repo._table.__tablename__,
        stmt=permissions.user_repo.query_list(),
        page_params=PageParams(page=query.page, size=query.size),
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
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    # responses=users_read_responses,
    response_model=UserReadAsAdmin | UserReadAsManager | UserRead,
)
async def users_read(
    user: User = Permission([AccessRead, AccessReadSelf], get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserReadAsAdmin | UserReadAsManager | UserRead:
    """Retrieve a single user by id.

    Permissions:
    ------------
    `role=admin|manager` : all users

    `role=organization` : all users associated with the organization through the `user_organization`
        table

    `role=employee` : all users associated with any organizations they are associated with
        through the `user_organization`

    `role=user` : only their own user profile id

    Returns:
    --------
    a dictionary containing the user profile information

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role
    - `UserRead` : only publically accessible fields

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], user_id=user.id
    )

    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        permissions.get_resource_response(
            resource=user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
                RoleUser: UserRead,
            },
        )
    )
    return response_out


@router.patch(
    "/{user_id}",
    name="users:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsAdmin | UserReadAsManager | UserRead,
)
async def users_update(
    user_in: UserUpdateAsAdmin | UserUpdateAsManager | UserUpdate,
    user: User = Permission([AccessUpdate, AccessUpdateSelf], get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserReadAsAdmin | UserReadAsManager | UserRead:
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
    permissions.verify_input_schema_by_role(
        input_object=user_in,
        schema_privileges={
            RoleAdmin: UserUpdateAsAdmin,
            RoleManager: UserUpdateAsManager,
            RoleUser: UserUpdate,
        },
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], user_id=user.id
    )
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
    if updated_user is None:  # pragma: no cover
        updated_user = user

    response_out: UserReadAsAdmin | UserReadAsManager | UserRead = (
        permissions.get_resource_response(
            resource=updated_user,
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
                RoleUser: UserRead,
            },
        )
    )
    return response_out


@router.delete(
    "/{user_id}",
    name="users:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def users_delete(
    bg_tasks: BackgroundTasks,
    user: User = Permission([AccessDelete, AccessDeleteSelf], get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserDelete:
    """Delete a user by id.

    Permissions:
    ------------
    `role=admin` : all users

    `role=user` : may request to have their profile and all associated data deleted

    Returns:
    --------
    `UserDelete` : a message indicating the user was deleted or requested to be
        deleted with the user id and corresponding task id

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin], user_id=user.id)
    output_message: str
    if permissions.current_user.id == user.id:
        bg_tasks.add_task(bg_task_request_to_delete_user, user_id=str(user.id))
        output_message = "User requested to be deleted"
    else:
        await permissions.user_repo.delete(entry=user)
        output_message = "User deleted"
    return UserDelete(
        message=output_message,
        user_id=user.id,
    )


@router.post(
    "/{user_id}/privileges/add",
    name="users:add_privileges",
    dependencies=[
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsAdmin | UserReadAsManager,
)
async def users_update_add_privileges(
    user_in: UserUpdatePrivileges,
    user: User = Permission(AccessUpdate, get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserReadAsAdmin | UserReadAsManager:
    """Add privileges to a user by id.

    Permissions:
    ------------
    `role=admin` : all users

    `role=manager` : cannot add the RoleAdmin privilege

    Returns:
    --------
    the updated user object

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    # update the user data
    updated_user: User = await permissions.add_privileges(to_user=user, schema=user_in)

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


@router.post(
    "/{user_id}/privileges/remove",
    name="users:remove_privileges",
    dependencies=[
        Depends(get_async_db),
        Depends(get_user_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsAdmin | UserReadAsManager,
)
async def users_update_remove_privileges(
    user_in: UserUpdatePrivileges,
    user: User = Permission(AccessUpdate, get_user_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserReadAsAdmin | UserReadAsManager:
    """Remove privileges from a user by id.

    Permissions:
    ------------
    `role=admin|manager` : all users

    Returns:
    --------
    the updated user object

    - `UserReadAsAdmin` : all fields
    - `UserReadAsManager` : only fields accessible to the manager role

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    # update the user data
    updated_user: User = await permissions.remove_privileges(
        to_user=user, schema=user_in
    )

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

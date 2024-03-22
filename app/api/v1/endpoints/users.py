from fastapi import APIRouter, Depends, Request
from taskiq import AsyncTaskiqTask

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
from app.core.pagination import (
    GetPaginatedQueryParams,
    PageParams,
    PageParamsFromQuery,
    Paginated,
)
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
    RoleUser,
)
from app.models import User
from app.schemas import (
    UserDelete,
    UserRead,
    UserReadAsAdmin,
    UserReadAsManager,
    UserUpdate,
    UserUpdateAsAdmin,
    UserUpdateAsManager,
    UserUpdatePrivileges,
)
from app.tasks import task_request_to_delete_user

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
    response_model=UserReadAsAdmin | UserReadAsManager | UserRead,
)
async def users_current(
    request: Request,
    permissions: PermissionController = Depends(get_permission_controller),
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
    request.session["user_id"] = str(permissions.current_user.id)
    req_sess_ip = request.session.get("ip_address", False)
    if not req_sess_ip:
        request.session["ip_address"] = str(request_ip)
    # return role based response
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
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[UserReadAsAdmin] | Paginated[UserReadAsManager],
)
async def users_list(
    query: GetPaginatedQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[UserReadAsAdmin] | Paginated[UserReadAsManager]:
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
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    # return role based response
    response_out: Paginated[UserReadAsAdmin] | Paginated[
        UserReadAsManager
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
        Depends(auth.implicit_scheme),
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
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], user_id=user.id
    )
    # return role based response
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
        Depends(auth.implicit_scheme),
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
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=user_in,
        schema_privileges={
            RoleAdmin: UserUpdateAsAdmin,
            RoleManager: UserUpdateAsManager,
            RoleUser: UserUpdate,
        },
    )
    # verify current user has permission to take this action
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
    # permissions.db.refresh(updated_user)
    # return role based response
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
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(privileges=[RoleAdmin], user_id=user.id)
    user_delete: UserDelete
    if permissions.current_user.id == user.id:
        delete_user_task: AsyncTaskiqTask = await task_request_to_delete_user.kiq(
            user_id=str(user.id)
        )
        user_delete = UserDelete(
            message="User requested to be deleted",
            user_id=user.id,
            task_id=delete_user_task.task_id,
        )
    else:
        await permissions.user_repo.delete(entry=user)
        user_delete = UserDelete(message="User deleted", user_id=user.id)
    return user_delete


@router.post(
    "/{user_id}/privileges/add",
    name="users:add_privileges",
    dependencies=[
        Depends(auth.implicit_scheme),
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
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    # update the user data
    updated_user: User = await permissions.add_privileges(to_user=user, schema=user_in)
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


@router.post(
    "/{user_id}/privileges/remove",
    name="users:remove_privileges",
    dependencies=[
        Depends(auth.implicit_scheme),
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
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    # update the user data
    updated_user: User = await permissions.remove_privileges(
        to_user=user, schema=user_in
    )
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

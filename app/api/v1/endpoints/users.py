from os import environ
from typing import Any, Dict

import requests
from fastapi import APIRouter, Depends, Request, Response
from taskiq import AsyncTaskiqTask

from app.api.deps import (
    Permission,
    PermissionController,
    RequestClientIp,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_request_client_ip,
    get_user_or_404,
)
from app.api.exceptions import (
    UserAlreadyExists,
    UserAuthRequestInvalidToken,
    UserAuthRequestPending,
    UserAuthRequestRequiresRefresh,
    UserPasswordsMismatch,
)
from app.core.config import Settings, get_settings

# from app.api.openapi import users_read_responses
from app.core.pagination import (
    GetPaginatedQueryParams,
    PageParams,
    PageParamsFromQuery,
    Paginated,
)
from app.core.redis import redis_conn
from app.core.security import CsrfProtect, RateLimiter, auth
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
    UserAuthRequestToken,
    UserDelete,
    UserLoginRequest,
    UserRead,
    UserReadAsAdmin,
    UserReadAsManager,
    UserSession,
    UserUpdate,
    UserUpdateAsAdmin,
    UserUpdateAsManager,
    UserUpdatePrivileges,
)
from app.tasks import task_request_to_delete_user

router: APIRouter = APIRouter()


@router.get(
    "/request-auth",
    name="users:authentication_request_csrf",
    dependencies=[
        Depends(CsrfProtect),
        Depends(get_settings),
        Depends(get_request_client_ip),
    ],
    response_model=UserAuthRequestToken,
)
async def get_auth_request_csrf(
    response: Response,
    request_ip: RequestClientIp,
    csrf_protect: CsrfProtect = Depends(),
    settings: Settings = Depends(get_settings),
) -> UserAuthRequestToken:
    """Generate an auth request token to be used in the /login route.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the CSRF token for the API

    """
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens(
        settings.api.csrf_secret_key
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    csrf_protect.set_csrf_header(csrf_token, response)

    auth_request_key = f"auth:request:{request_ip}"
    auth_request: str | None = await redis_conn.get(auth_request_key)
    if auth_request is None:
        # expires in 1 hour
        await redis_conn.set(auth_request_key, csrf_token, ex=3600)
    else:
        raise UserAuthRequestPending()

    return UserAuthRequestToken(auth_request_token=csrf_token)


@router.post(
    "/login",
    name="users:authentication",
    dependencies=[
        # 10 req/sec = 36,000 req/hr
        Depends(RateLimiter(times=10, seconds=1)),
        Depends(CsrfProtect),
        Depends(get_settings),
        Depends(get_request_client_ip),
    ],
    response_model=UserSession,
)
async def user_authentication(
    request: Request,
    response: Response,
    request_ip: RequestClientIp,
    user_login: UserLoginRequest,
    csrf_protect: CsrfProtect = Depends(),
    settings: Settings = Depends(get_settings),
) -> UserSession:
    auth_request_key = f"auth:request:{request_ip}"
    auth_request_token: str | None = await redis_conn.get(auth_request_key)
    if auth_request_token is None:
        raise UserAuthRequestRequiresRefresh()
    elif auth_request_token != user_login.auth_request_token:
        raise UserAuthRequestInvalidToken()
    else:
        # delete the auth request token
        await redis_conn.delete(auth_request_key)

    await csrf_protect.validate_csrf(
        request,
        secret_key=settings.api.csrf_secret_key,
        cookie_key=settings.api.csrf_name_key,
    )
    csrf_protect.unset_csrf_cookie(response)
    csrf_protect.unset_csrf_header(response)

    if user_login.password != user_login.confirm_password:
        raise UserPasswordsMismatch()
    clid: str | None = environ.get("AUTH0_M2M_CLIENT_ID", None)
    clsh: str | None = environ.get("AUTH0_M2M_CLIENT_SECRET", None)
    if clid is None:  # pragma: no cover
        raise ValueError("AUTH0_M2M_CLIENT_ID is not set")
    if clsh is None:  # pragma: no cover
        raise ValueError("AUTH0_M2M_CLIENT_SECRET is not set")
    auth_url = f"https://{settings.auth.domain}/oauth/token"
    auth_data = {
        "grant_type": "client_credentials",
        "username": user_login.email,
        "password": user_login.password,
        "audience": settings.auth.audience,
        "scope": user_login.auth_scope,
    }
    headers = {"content-type": "application/json"}
    auth_response = requests.post(
        auth_url, json=auth_data, headers=headers, auth=(clid, clsh)
    )
    data: Dict[str, Any] = auth_response.json()
    token_type = data.get("token_type", "Bearer")
    access_token = data.get("access_token", None)
    access_token_expires = data.get("expires_in", None)
    return UserSession(
        token_type=token_type,
        access_token=access_token,
        expires_in=access_token_expires,
    )


@router.get(
    "/me",
    name="users:current",
    dependencies=[
        Depends(get_request_client_ip),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserReadAsAdmin | UserReadAsManager | UserRead,
)
async def users_current(
    request: Request,
    request_ip: RequestClientIp,
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
    response_out: Paginated[UserReadAsAdmin] | Paginated[UserReadAsManager] = (
        await permissions.get_paginated_resource_response(
            table_name=permissions.user_repo._table.__tablename__,
            stmt=permissions.user_repo.query_list(),
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: UserReadAsAdmin,
                RoleManager: UserReadAsManager,
            },
        )
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

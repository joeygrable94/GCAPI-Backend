from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonClientTrackingLinkQueryParams,
    GetClientTrackingLinkQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_tracking_link_or_404,
)
from app.api.exceptions import ClientNotExists, TrackingLinkAlreadyExists
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteRelated,
    AccessUpdate,
    AccessUpdateRelated,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import TrackingLinkRepository
from app.db.utilities import hash_url, parse_url_utm_params
from app.models import TrackingLink
from app.schemas import (
    TrackingLinkBaseUtmParams,
    TrackingLinkCreate,
    TrackingLinkCreateRequest,
    TrackingLinkRead,
    TrackingLinkUpdate,
    TrackingLinkUpdateRequest,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="tracking_link:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(CommonClientTrackingLinkQueryParams),
    ],
    response_model=Paginated[TrackingLinkRead],
)
async def tracking_link_list(
    query: GetClientTrackingLinkQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[TrackingLinkRead]:
    """Retrieve a paginated list of tracking links associated with the client.

    Permissions:
    ------------
    `role=admin|manager` : all tracking links

    `role=user` : only tracking links associated with the user via `user_client`
        table

    Returns:
    --------
    `Paginated[TrackingLinkRead]` : a paginated list of client tracking links,
        optionally filtered

    """
    # formulate the select statement based on the current user's role
    links_repo = TrackingLinkRepository(permissions.db)
    query_params: Dict[str, Any] = {}
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        query_params = {
            "client_id": query.client_id,
            "url_path": query.url_path,
            "utm_campaign": query.utm_campaign,
            "utm_medium": query.utm_medium,
            "utm_source": query.utm_source,
            "utm_content": query.utm_content,
            "utm_term": query.utm_term,
            "is_active": query.is_active,
        }
    else:
        query_params = {
            "user_id": permissions.current_user.id,
            "client_id": query.client_id,
            "url_path": query.url_path,
            "utm_campaign": query.utm_campaign,
            "utm_medium": query.utm_medium,
            "utm_source": query.utm_source,
            "utm_content": query.utm_content,
            "utm_term": query.utm_term,
            "is_active": query.is_active,
        }
    select_stmt: Select = links_repo.query_list(**query_params)
    # return role based response
    response_out: Paginated[TrackingLinkRead] = (
        await permissions.get_paginated_resource_response(
            table_name=TrackingLink.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: TrackingLinkRead,
                RoleManager: TrackingLinkRead,
                RoleClient: TrackingLinkRead,
                RoleEmployee: TrackingLinkRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="tracking_link:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=TrackingLinkRead,
)
async def tracking_link_create(
    tracking_link_in: TrackingLinkCreateRequest,
    permissions: PermissionController = Depends(get_permission_controller),
) -> TrackingLinkRead:
    """Create a new tracking link and assign it to the client.

    Permissions:
    ------------
    `role=admin|manager` : create tracking links for all clients

    `role=user` : only create tracking links for clients associated with the
        user via `user_client` table

    Returns:
    --------
    `TrackingLinkRead` : the newly created client

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], client_id=tracking_link_in.client_id
    )
    if tracking_link_in.client_id is not None:
        client_exists = await permissions.client_repo.read(tracking_link_in.client_id)
        if client_exists is None:
            raise ClientNotExists()
    links_repo = TrackingLinkRepository(permissions.db)
    trk_url_hash = hash_url(tracking_link_in.url)
    tracking_link: TrackingLink | None = await links_repo.exists_by_fields(
        {"url_hash": trk_url_hash}
    )
    if tracking_link is not None:
        raise TrackingLinkAlreadyExists()
    url_params = parse_url_utm_params(tracking_link_in.url)
    tracking_link = await links_repo.create(
        schema=TrackingLinkCreate(
            url=tracking_link_in.url,
            url_hash=trk_url_hash,
            is_active=tracking_link_in.is_active or True,
            client_id=tracking_link_in.client_id,
            **url_params.model_dump(),
        )
    )
    # return role based response
    response_out: TrackingLinkRead = permissions.get_resource_response(
        resource=tracking_link,
        responses={
            RoleUser: TrackingLinkRead,
        },
    )
    return response_out


@router.get(
    "/{tracking_link_id}",
    name="tracking_link:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_tracking_link_or_404),
    ],
    response_model=TrackingLinkRead,
)
async def tracking_link_read(
    permissions: PermissionController = Depends(get_permission_controller),
    tracked_link: TrackingLink = Permission(
        [AccessUpdate, AccessUpdateRelated], get_tracking_link_or_404
    ),
) -> TrackingLinkRead:
    """Retrieve a client associated tracking link by id.

    Permissions:
    ------------
    `role=admin|manager` : all tracking links

    `role=user` : only tracking links for clients associated with the
        user via `user_client` table

    Returns:
    --------
    `TrackingLinkRead` : a tracking links matching the provided id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=tracked_link.client_id,
    )
    # return role based response
    response_out: TrackingLinkRead = permissions.get_resource_response(
        resource=tracked_link,
        responses={
            RoleUser: TrackingLinkRead,
        },
    )
    return response_out


@router.patch(
    "/{tracking_link_id}",
    name="tracking_link:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_tracking_link_or_404),
    ],
    response_model=TrackingLinkRead,
)
async def tracking_link_update(
    tracking_link_in: TrackingLinkUpdateRequest,
    permissions: PermissionController = Depends(get_permission_controller),
    tracked_link: TrackingLink = Permission(
        [AccessUpdate, AccessUpdateRelated], get_tracking_link_or_404
    ),
) -> TrackingLinkRead:
    """Update a tracking link by id, assign it to the client and user making the update.

    Permissions:
    ------------
    `role=admin|manager` : update any tracking link

    `role=user` : only update tracking links for clients associated with the
        user via `user_client` table

    Returns:
    --------
    `TrackingLinkRead` : the newly updated tracking link

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=tracking_link_in,
        schema_privileges={
            RoleUser: TrackingLinkUpdateRequest,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=tracked_link.client_id,
    )
    if tracking_link_in.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=tracking_link_in.client_id,
        )
        client_exists = await permissions.client_repo.read(tracking_link_in.client_id)
        if client_exists is None:
            raise ClientNotExists()
    links_repo = TrackingLinkRepository(permissions.db)
    url_params: TrackingLinkBaseUtmParams = TrackingLinkBaseUtmParams()
    trk_url_hash: None | str = None
    if tracking_link_in.url is not None:
        trk_url_hash = hash_url(tracking_link_in.url)
        a_tracking_link: TrackingLink | None = await links_repo.exists_by_fields(
            {"url_hash": trk_url_hash}
        )
        if a_tracking_link:
            raise TrackingLinkAlreadyExists()
        url_params = parse_url_utm_params(tracking_link_in.url)
    updated_tracking_link: TrackingLink = await links_repo.update(
        tracked_link,
        schema=TrackingLinkUpdate(
            url=tracking_link_in.url,
            is_active=tracking_link_in.is_active,
            url_hash=trk_url_hash,
            client_id=tracking_link_in.client_id,
            **url_params.model_dump(),
        ),
    )
    # return role based response
    response_out: TrackingLinkRead = permissions.get_resource_response(
        resource=updated_tracking_link if updated_tracking_link else tracked_link,
        responses={
            RoleUser: TrackingLinkRead,
        },
    )
    return response_out


@router.delete(
    "/{tracking_link_id}",
    name="tracking_link:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_tracking_link_or_404),
    ],
    response_model=None,
)
async def tracking_link_delete(
    permissions: PermissionController = Depends(get_permission_controller),
    tracked_link: TrackingLink = Permission(
        [AccessDelete, AccessDeleteRelated], get_tracking_link_or_404
    ),
) -> None:
    """Delete a client's tracking link by id.

    Permissions:
    ------------
    `role=admin` : all tracking links

    `role=user` : may delete tracking links associated with clients they are
        associated with via the `user_client` table

    Returns:
    --------
    `None` : the client tracking link has been deleted

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin], client_id=tracked_link.client_id
    )
    links_repo = TrackingLinkRepository(permissions.db)
    await links_repo.delete(entry=tracked_link)
    return None

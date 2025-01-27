from typing import Any

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
from app.api.exceptions import ClientNotFound, EntityAlreadyExists
from app.core.pagination import PageParams, Paginated
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
    TrackingLinkBaseParams,
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
    links_repo = TrackingLinkRepository(permissions.db)
    query_params: dict[str, Any] = dict()
    if query.client_id is not None:
        query_params["client_id"] = query.client_id
    if query.scheme is not None:
        query_params["scheme"] = query.scheme
    if query.domain is not None:
        query_params["domain"] = query.domain
    if query.destination is not None:
        query_params["destination"] = query.destination
    if query.url_path:
        query_params["url_path"] = query.url_path
    if query.utm_campaign is not None:
        query_params["utm_campaign"] = query.utm_campaign
    if query.utm_medium:
        query_params["utm_medium"] = query.utm_medium
    if query.utm_source is not None:
        query_params["utm_source"] = query.utm_source
    if query.utm_content is not None:
        query_params["utm_content"] = query.utm_content
    if query.utm_term is not None:
        query_params["utm_term"] = query.utm_term
    if query.is_active is not None:
        query_params["is_active"] = query.is_active

    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        pass
    else:
        query_params["user_id"] = permissions.current_user.id

    select_stmt: Select = links_repo.query_list(**query_params)
    response_out: Paginated[
        TrackingLinkRead
    ] = await permissions.get_paginated_resource_response(
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
    return response_out


@router.post(
    "/",
    name="tracking_link:create",
    dependencies=[
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

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], client_id=tracking_link_in.client_id
    )
    if tracking_link_in.client_id is not None:
        client_exists = await permissions.client_repo.read(tracking_link_in.client_id)
        if client_exists is None:
            raise ClientNotFound()
    links_repo = TrackingLinkRepository(permissions.db)
    trk_url_hash = hash_url(tracking_link_in.url)
    tracking_link: TrackingLink | None = await links_repo.exists_by_fields(
        {"url_hash": trk_url_hash}
    )
    if tracking_link is not None:
        raise EntityAlreadyExists(
            entity_info="TrackingLink url = {}".format(tracking_link_in.url)
        )
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

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=tracked_link.client_id,
    )

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
    permissions.verify_input_schema_by_role(
        input_object=tracking_link_in,
        schema_privileges={
            RoleUser: TrackingLinkUpdateRequest,
        },
    )
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
            raise ClientNotFound()
    links_repo = TrackingLinkRepository(permissions.db)
    url_params: TrackingLinkBaseParams | None
    trk_url_hash: None | str = None
    if tracking_link_in.url is not None:
        trk_url_hash = hash_url(tracking_link_in.url)
        a_tracking_link: TrackingLink | None = await links_repo.exists_by_fields(
            {"url_hash": trk_url_hash}
        )
        if a_tracking_link:
            raise EntityAlreadyExists(
                entity_info="TrackingLink url = {}".format(tracking_link_in.url)
            )
        url_params = parse_url_utm_params(tracking_link_in.url)
    update_schema = (
        TrackingLinkUpdate(
            url=tracking_link_in.url,
            url_hash=trk_url_hash,
            is_active=tracking_link_in.is_active,
            client_id=tracking_link_in.client_id,
        )
        if url_params is None
        else TrackingLinkUpdate(
            url=tracking_link_in.url,
            url_hash=trk_url_hash,
            is_active=tracking_link_in.is_active,
            client_id=tracking_link_in.client_id,
            **url_params.model_dump(),
        )
    )
    updated_tracking_link: TrackingLink = await links_repo.update(
        tracked_link,
        schema=update_schema,
    )
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
    if tracked_link.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin], client_id=tracked_link.client_id
        )
    links_repo = TrackingLinkRepository(permissions.db)
    await links_repo.delete(entry=tracked_link)
    return None

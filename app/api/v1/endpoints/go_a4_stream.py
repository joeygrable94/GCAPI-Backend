from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonWebsiteGa4QueryParams,
    GetWebsiteGa4QueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_ga4_stream_404,
    get_permission_controller,
)
from app.api.exceptions import (
    Ga4PropertyNotExists,
    Ga4StreamAlreadyExists,
    WebsiteNotExists,
)
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteRelated,
    AccessDeleteSelf,
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateRelated,
    AccessUpdateSelf,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import (
    GoAnalytics4PropertyRepository,
    GoAnalytics4StreamRepository,
    WebsiteRepository,
)
from app.models import GoAnalytics4Property, GoAnalytics4Stream, Website
from app.schemas import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
    GoAnalytics4StreamUpdate,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="ga4_stream:list",
    dependencies=[
        Depends(CommonWebsiteGa4QueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[GoAnalytics4StreamRead],
)
async def ga4_stream_list(
    query: GetWebsiteGa4QueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[GoAnalytics4StreamRead]:
    """Retrieve a paginated list of ga4 streams.

    Permissions:
    ------------
    `role=admin|manager` : all ga4 streams

    `role=user` : only ga4 streams that belong to the user

    Returns:
    --------
    `Paginated[GoAnalytics4StreamRead]` : a paginated list of ga4 streams,
        optionally filtered

    """
    # formulate the select statement based on the current user's role
    ga4_stream_repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=permissions.db
    )
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = ga4_stream_repo.query_list(
            website_id=query.website_id,
            ga4_id=query.ga4_id,
        )
    else:
        select_stmt = ga4_stream_repo.query_list(
            user_id=permissions.current_user.id,
            website_id=query.website_id,
            ga4_id=query.ga4_id,
        )
    response_out: Paginated[GoAnalytics4StreamRead] = (
        await permissions.get_paginated_resource_response(
            table_name=GoAnalytics4Stream.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoAnalytics4StreamRead,
                RoleManager: GoAnalytics4StreamRead,
                RoleClient: GoAnalytics4StreamRead,
                RoleEmployee: GoAnalytics4StreamRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="ga4_stream:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4StreamRead,
)
async def ga4_stream_create(
    ga4_stream_in: GoAnalytics4StreamCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoAnalytics4StreamRead:
    """Create a new ga4 streams.

    Permissions:
    ------------
    `role=admin|manager` : create new ga4 streams for all clients

    `role=user` : create only ga4 streams that belong to any clients associated
        with the current user

    Returns:
    --------
    `GoAnalytics4StreamRead` : the newly created ga4 stream

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=ga4_stream_in.website_id,
    )
    ga4_stream_repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=permissions.db
    )
    data: Dict = ga4_stream_in.model_dump()
    check_title: str = data.get("title", "")
    check_stream_id: str = data.get("stream_id", "")
    a_ga4_title: GoAnalytics4Stream | None = await ga4_stream_repo.read_by(
        field_name="title",
        field_value=check_title,
    )
    a_ga4_stream_id: GoAnalytics4Stream | None = await ga4_stream_repo.read_by(
        field_name="stream_id",
        field_value=check_stream_id,
    )
    if a_ga4_title is not None or a_ga4_stream_id is not None:
        raise Ga4StreamAlreadyExists()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_website: Website | None = await website_repo.read(
        entry_id=ga4_stream_in.website_id
    )
    if a_website is None:
        raise WebsiteNotExists()
    ga4_repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=permissions.db
    )
    a_ga4_property: GoAnalytics4Property | None = await ga4_repo.read(
        entry_id=ga4_stream_in.ga4_id
    )
    if a_ga4_property is None:
        raise Ga4PropertyNotExists()
    new_ga4_stream: GoAnalytics4Stream = await ga4_stream_repo.create(ga4_stream_in)
    # return role based response
    response_out: GoAnalytics4StreamRead = permissions.get_resource_response(
        resource=new_ga4_stream,
        responses={
            RoleUser: GoAnalytics4StreamRead,
        },
    )
    return response_out


@router.get(
    "/{ga4_stream_id}",
    name="ga4_stream:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_ga4_stream_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4StreamRead,
)
async def ga4_stream_read(
    ga4_stream: GoAnalytics4Stream = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_ga4_stream_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoAnalytics4StreamRead:
    """Retrieve a single ga4 stream by id.

    Permissions:
    ------------
    `role=admin|manager` : read all ga4 streams

    `role=user` : read only ga4 streams that belong to any clients
        associated with the current user

    Returns:
    --------
    `GoAnalytics4StreamRead` : the ga4 stream matching the ga4_stream_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=ga4_stream.website_id,
    )
    # return role based response
    response_out: GoAnalytics4StreamRead = permissions.get_resource_response(
        resource=ga4_stream,
        responses={
            RoleUser: GoAnalytics4StreamRead,
        },
    )
    return response_out


@router.patch(
    "/{ga4_stream_id}",
    name="ga4_stream:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_ga4_stream_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4StreamRead,
)
async def ga4_stream_update(
    ga4_stream_in: GoAnalytics4StreamUpdate,
    ga4_stream: GoAnalytics4Stream = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_ga4_stream_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoAnalytics4StreamRead:
    """Update a ga4 stream by id.

    Permissions:
    ------------
    `role=admin|manager` : update all ga4 streams

    `role=user` : update only ga4 streams that belong to any clients associated
        with the current user

    Returns:
    --------
    `GoAnalytics4StreamRead` : the updated ga4 stream

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=ga4_stream_in,
        schema_privileges={
            RoleUser: GoAnalytics4StreamUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=ga4_stream.website_id,
    )
    ga4_stream_repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=permissions.db
    )
    if ga4_stream_in.title is not None:
        a_ga4_stream: GoAnalytics4Stream | None = await ga4_stream_repo.read_by(
            field_name="title", field_value=ga4_stream_in.title
        )
        if a_ga4_stream:
            raise Ga4StreamAlreadyExists()
    if ga4_stream_in.website_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=ga4_stream_in.website_id,
        )
        website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
        a_website: Website | None = await website_repo.read(
            entry_id=ga4_stream_in.website_id
        )
        if a_website is None:
            raise WebsiteNotExists()
    updated_ga4: GoAnalytics4Stream | None = await ga4_stream_repo.update(
        entry=ga4_stream, schema=ga4_stream_in
    )
    # return role based response
    response_out: GoAnalytics4StreamRead = permissions.get_resource_response(
        resource=updated_ga4 if updated_ga4 else ga4_stream,
        responses={
            RoleUser: GoAnalytics4StreamRead,
        },
    )
    return response_out


@router.delete(
    "/{ga4_stream_id}",
    name="ga4_stream:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_ga4_stream_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def ga4_stream_delete(
    ga4_stream: GoAnalytics4Stream = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_ga4_stream_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a ga4 stream by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any ga4 streams

    `role=user` : delete only ga4 streams that belong to any clients associated
        with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=ga4_stream.website_id,
    )
    ga4_stream_repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=permissions.db
    )
    await ga4_stream_repo.delete(entry=ga4_stream)
    return None

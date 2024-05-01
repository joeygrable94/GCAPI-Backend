from fastapi import APIRouter, Depends, Path
from sqlalchemy import Select

from app.api.deps import (
    CommonWebsiteGoSearchConsoleQueryParams,
    GetWebsiteGoSearchConsoleQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_go_search_console_metric_404,
    get_go_search_console_property_404,
    get_permission_controller,
)
from app.api.exceptions import GoSearchConsoleMetricTypeInvalid
from app.core.pagination import PageParams, Paginated, paginated_query
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteRelated,
    AccessDeleteSelf,
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.crud import GoSearchConsoleMetricRepository
from app.models import (
    GoSearchConsoleCountry,
    GoSearchConsoleDevice,
    GoSearchConsolePage,
    GoSearchConsoleProperty,
    GoSearchConsoleQuery,
    GoSearchConsoleSearchappearance,
)
from app.schemas import (
    GoSearchConsoleMetricCreate,
    GoSearchConsoleMetricPages,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsoleMetricUpdate,
)

router: APIRouter = APIRouter()


@router.get(
    "/{gsc_id}",
    name="go_search_console_property_metric:list_all_metric_types",
    dependencies=[
        Depends(CommonWebsiteGoSearchConsoleQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
    ],
    response_model=GoSearchConsoleMetricPages,
)
async def go_search_console_metric_list_all(
    query: GetWebsiteGoSearchConsoleQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated],
        get_go_search_console_property_404,
    ),
) -> GoSearchConsoleMetricPages:
    """Retrieve a paginated list of all the google search console property metrics
    for the given google search console property id.

    Permissions:
    ------------
    `role=admin|manager` : all google search console property metrics

    `role=user` : only google search console property metrics that belong to the user

    Returns:
    --------
    `Paginated[GoSearchConsoleMetricRead]` : a paginated list of google search
        console property metrics, optionally filtered

    """
    gscm_sa_out: Paginated[GoSearchConsoleMetricRead] | None = None
    gscm_qu_out: Paginated[GoSearchConsoleMetricRead] | None = None
    gscm_pg_out: Paginated[GoSearchConsoleMetricRead] | None = None
    gscm_dv_out: Paginated[GoSearchConsoleMetricRead] | None = None
    gscm_co_out: Paginated[GoSearchConsoleMetricRead] | None = None
    query_metric_type_list: list[GoSearchConsoleMetricType]
    if query.metric_types is None:
        query_metric_type_list = [mt for mt in GoSearchConsoleMetricType]
    else:
        query_metric_type_list = query.metric_types
    for metric_type in query_metric_type_list:
        metric_repo = GoSearchConsoleMetricRepository(
            permissions.db, metric_type=GoSearchConsoleMetricType(metric_type)
        )
        metric_stmt = metric_repo.query_list(
            gsc_id=go_sc.id, date_start=query.date_start, date_end=query.date_end
        )
        if metric_type == GoSearchConsoleMetricType.searchappearance:
            gscm_sa_out = await paginated_query(
                table_name=GoSearchConsoleSearchappearance.__tablename__,
                db=permissions.db,
                stmt=metric_stmt,
                page_params=PageParams(page=query.page, size=query.size),
                response_schema=GoSearchConsoleMetricRead,
            )
        elif metric_type == GoSearchConsoleMetricType.query:
            gscm_qu_out = await paginated_query(
                table_name=GoSearchConsoleQuery.__tablename__,
                db=permissions.db,
                stmt=metric_stmt,
                page_params=PageParams(page=query.page, size=query.size),
                response_schema=GoSearchConsoleMetricRead,
            )
        elif metric_type == GoSearchConsoleMetricType.page:
            gscm_pg_out = await paginated_query(
                table_name=GoSearchConsolePage.__tablename__,
                db=permissions.db,
                stmt=metric_stmt,
                page_params=PageParams(page=query.page, size=query.size),
                response_schema=GoSearchConsoleMetricRead,
            )
        elif metric_type == GoSearchConsoleMetricType.device:
            gscm_dv_out = await paginated_query(
                table_name=GoSearchConsoleDevice.__tablename__,
                db=permissions.db,
                stmt=metric_stmt,
                page_params=PageParams(page=query.page, size=query.size),
                response_schema=GoSearchConsoleMetricRead,
            )
        elif metric_type == GoSearchConsoleMetricType.country:
            gscm_co_out = await paginated_query(
                table_name=GoSearchConsoleCountry.__tablename__,
                db=permissions.db,
                stmt=metric_stmt,
                page_params=PageParams(page=query.page, size=query.size),
                response_schema=GoSearchConsoleMetricRead,
            )
    return GoSearchConsoleMetricPages(
        searchappearance=gscm_sa_out.model_dump() if gscm_sa_out else None,
        query=gscm_qu_out.model_dump() if gscm_qu_out else None,
        page=gscm_pg_out.model_dump() if gscm_pg_out else None,
        device=gscm_dv_out.model_dump() if gscm_dv_out else None,
        country=gscm_co_out.model_dump() if gscm_co_out else None,
    )


@router.get(
    "/{gsc_id}/{metric_type}",
    name="go_search_console_property_metric:list_by_metric_type",
    dependencies=[
        Depends(CommonWebsiteGoSearchConsoleQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
    ],
    response_model=Paginated[GoSearchConsoleMetricRead],
)
async def go_search_console_metric_list_by_type(
    query: GetWebsiteGoSearchConsoleQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated],
        get_go_search_console_property_404,
    ),
    metric_type: GoSearchConsoleMetricType = Path(...),
) -> Paginated[GoSearchConsoleMetricRead]:
    """
    Retrieve a paginated list of google search console property metrics filtered
    by the metric_type parameter.

    Permissions:
    ------------
    `role=admin|manager` : all google search console property metrics

    `role=user` : only google search console property metrics that belong to the user

    Returns:
    --------
    `Paginated[GoSearchConsoleMetricRead]` : a paginated list of google search
        console property metrics, optionally filtered

    """
    gsc_metric_repo = GoSearchConsoleMetricRepository(
        permissions.db, metric_type=metric_type
    )
    select_stmt: Select
    select_stmt = gsc_metric_repo.query_list(
        gsc_id=go_sc.id, date_start=query.date_start, date_end=query.date_end
    )
    gsc_table_name: str
    if metric_type == GoSearchConsoleMetricType.searchappearance:
        gsc_table_name = GoSearchConsoleSearchappearance.__tablename__
    elif metric_type == GoSearchConsoleMetricType.query:
        gsc_table_name = GoSearchConsoleQuery.__tablename__
    elif metric_type == GoSearchConsoleMetricType.page:
        gsc_table_name = GoSearchConsolePage.__tablename__
    elif metric_type == GoSearchConsoleMetricType.device:
        gsc_table_name = GoSearchConsoleDevice.__tablename__
    elif metric_type == GoSearchConsoleMetricType.country:
        gsc_table_name = GoSearchConsoleCountry.__tablename__
    else:  # pragma: no cover
        raise GoSearchConsoleMetricTypeInvalid()
    gsc_metrics_out: Paginated[GoSearchConsoleMetricRead]
    gsc_metrics_out = await permissions.get_paginated_resource_response(
        table_name=gsc_table_name,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleUser: GoSearchConsoleMetricRead,
        },
    )
    return gsc_metrics_out


@router.post(
    "/{gsc_id}/{metric_type}",
    name="go_search_console_property_metric:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
    ],
    response_model=GoSearchConsoleMetricRead,
)
async def go_search_console_metric_create(
    gsc_metric_in: GoSearchConsoleMetricCreate,
    permissions: PermissionController = Depends(get_permission_controller),
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated],
        get_go_search_console_property_404,
    ),
    metric_type: GoSearchConsoleMetricType = Path(...),
) -> GoSearchConsoleMetricRead:
    """Create a new google search console property metrics.

    Permissions:
    ------------
    `role=admin|manager` : create new google search console property metrics
        for all clients

    `role=user` : create only google search console property metrics that
        belong to any clients associated with the current user

    Returns:
    --------
    `GoSearchConsoleMetricRead` : the newly created google search console
        property metric.

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    gsc_metric_repo = GoSearchConsoleMetricRepository(
        session=permissions.db, metric_type=metric_type
    )
    new_gsc_metric: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
    ) = await gsc_metric_repo.create(gsc_metric_in)
    response_out: GoSearchConsoleMetricRead = permissions.get_resource_response(
        resource=new_gsc_metric,
        responses={
            RoleUser: GoSearchConsoleMetricRead,
        },
    )
    return response_out


@router.get(
    "/{gsc_id}/{metric_type}/{metric_id}",
    name="go_search_console_property_metric:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
        Depends(get_go_search_console_metric_404),
    ],
    response_model=GoSearchConsoleMetricRead,
)
async def go_search_console_metric_read(
    permissions: PermissionController = Depends(get_permission_controller),
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated],
        get_go_search_console_property_404,
    ),
    go_sc_metric: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
    ) = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated],
        get_go_search_console_metric_404,
    ),
) -> GoSearchConsoleMetricRead:
    """Retrieve a single google search console property metric by id.

    Permissions:
    ------------
    `role=admin|manager` : read all google search console property metrics

    `role=user` : read only google search console property metrics that belong to
        any clients associated with the current user

    Returns:
    --------
    `GoSearchConsoleMetricRead` : the google search console property metric matching
        the metric_type and id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    # return role based response
    response_out: GoSearchConsoleMetricRead = permissions.get_resource_response(
        resource=go_sc_metric,
        responses={
            RoleUser: GoSearchConsoleMetricRead,
        },
    )
    return response_out


@router.patch(
    "/{gsc_id}/{metric_type}/{metric_id}",
    name="go_search_console_property_metric:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
        Depends(get_go_search_console_metric_404),
    ],
    response_model=GoSearchConsoleMetricRead,
)
async def go_search_console_metric_update(
    gsc_metric_in: GoSearchConsoleMetricUpdate,
    permissions: PermissionController = Depends(get_permission_controller),
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated],
        get_go_search_console_property_404,
    ),
    go_sc_metric: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
    ) = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated],
        get_go_search_console_metric_404,
    ),
    metric_type: GoSearchConsoleMetricType = Path(...),
) -> GoSearchConsoleMetricRead:
    """Update a google search console property metric by id.

    Permissions:
    ------------
    `role=admin|manager` : update all google search console property metrics

    `role=user` : update only google search console property metrics that
        belong to any clients associated with the current user

    Returns:
    --------
    `GoSearchConsoleMetricRead` : the updated google search console property metric

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    gsc_metric_repo = GoSearchConsoleMetricRepository(
        session=permissions.db, metric_type=metric_type
    )
    updated_gsc_metric: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
        | None
    ) = await gsc_metric_repo.update(entry=go_sc_metric, schema=gsc_metric_in)
    response_out: GoSearchConsoleMetricRead = permissions.get_resource_response(
        resource=updated_gsc_metric if updated_gsc_metric else go_sc_metric,
        responses={
            RoleUser: GoSearchConsoleMetricRead,
        },
    )
    return response_out


@router.delete(
    "/{gsc_id}/{metric_type}/{metric_id}",
    name="go_search_console_property_metric:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
        Depends(get_go_search_console_metric_404),
    ],
    response_model=None,
)
async def go_search_console_metric_delete(
    permissions: PermissionController = Depends(get_permission_controller),
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated],
        get_go_search_console_property_404,
    ),
    go_sc_metric: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
    ) = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated],
        get_go_search_console_metric_404,
    ),
    metric_type: GoSearchConsoleMetricType = Path(...),
) -> None:
    """Delete a google search console property metric by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any google search console property metrics

    `role=user` : delete only google search console property metrics that
        belong to any clients associated with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    gsc_metric_repo = GoSearchConsoleMetricRepository(
        session=permissions.db, metric_type=metric_type
    )
    await gsc_metric_repo.delete(entry=go_sc_metric)
    return None

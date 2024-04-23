from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonWebsitePageSpeedInsightsQueryParams,
    GetWebsitePageSpeedInsightsQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_website_page_psi_or_404,
)
from app.api.exceptions import WebsiteNotExists, WebsitePageNotExists
from app.core.logger import logger
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessRead,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import (
    WebsitePageRepository,
    WebsitePageSpeedInsightsRepository,
    WebsiteRepository,
)
from app.models import Website, WebsitePage, WebsitePageSpeedInsights
from app.schemas import (
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
    WebsitePageSpeedInsightsRead,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_page_speed_insights:list",
    dependencies=[
        Depends(CommonWebsitePageSpeedInsightsQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsitePageSpeedInsightsRead],
)
async def website_page_speed_insights_list(
    query: GetWebsitePageSpeedInsightsQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsitePageSpeedInsightsRead]:
    """Retrieve a paginated list of website page speed insights.

    Permissions:
    ------------
    `role=admin|manager` : all website page speed insights

    `role=client` : only website page speed insights with a website_id associated with
        the client via `client_website` table

    `role=employee` : only website page speed insights with a website_id associated
        with a client's website via `client_website` table, associated with the user
        via `user_client`

    Returns:
    --------
    `Paginated[WebsitePageSpeedInsightsRead]` : a paginated list of website page speed
        insights, optionally filtered
    """
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = web_psi_repo.query_list(
            website_id=query.website_id,
            page_id=query.page_id,
            devices=query.strategy,
        )
    else:
        select_stmt = web_psi_repo.query_list(
            user_id=permissions.current_user.id,
            website_id=query.website_id,
            page_id=query.page_id,
            devices=query.strategy,
        )
    response_out: Paginated[WebsitePageSpeedInsightsRead] = (
        await permissions.get_paginated_resource_response(
            table_name=WebsitePageSpeedInsights.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: WebsitePageSpeedInsightsRead,
                RoleManager: WebsitePageSpeedInsightsRead,
                RoleClient: WebsitePageSpeedInsightsRead,
                RoleEmployee: WebsitePageSpeedInsightsRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="website_page_speed_insights:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePageSpeedInsightsRead,
)
async def website_page_speed_insights_create(
    query: GetWebsitePageSpeedInsightsQueryParams,
    psi_in: WebsitePageSpeedInsightsBase,
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePageSpeedInsightsRead:
    """Create a new website page speed insights.

    Permissions:
    ------------
    `role=admin|manager` : create a new website page speed insights

    `role=client` : create a new website page speed insights that belongs to a website
        associated with the client via `client_website` table

    `role=employee` : create a new website page speed insights that belongs to a website
        associated with a client via `client_website` table, associated with the user
        via the `user_client` table

    Returns:
    --------
    `WebsitePageSpeedInsightsRead` : the newly created website page speed insights

    """
    # check if website_id provided
    if query.website_id is None:
        raise WebsiteNotExists()
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=query.website_id,
    )
    # check if website exists
    website_repo: WebsiteRepository = WebsiteRepository(permissions.db)
    a_website: Website | None = await website_repo.read(entry_id=query.website_id)
    if a_website is None:
        raise WebsiteNotExists()
    # check if page exists
    if query.page_id is None:
        raise WebsitePageNotExists()
    web_page_repo: WebsitePageRepository = WebsitePageRepository(permissions.db)
    a_web_page: WebsitePage | None = await web_page_repo.read(entry_id=query.page_id)
    if a_web_page is None:
        raise WebsitePageNotExists()
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(permissions.db)
    psi_create: WebsitePageSpeedInsightsCreate = WebsitePageSpeedInsightsCreate(
        **psi_in.model_dump(),
        page_id=query.page_id,
        website_id=query.website_id,
    )
    psi_in_db: WebsitePageSpeedInsights = await web_psi_repo.create(schema=psi_create)
    logger.info(
        "Created Website Page Speed Insights:",
        psi_in_db.id,
        psi_in_db.created,
    )
    return WebsitePageSpeedInsightsRead.model_validate(psi_in_db)


@router.get(
    "/{psi_id}",
    name="website_page_speed_insights:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_psi_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePageSpeedInsightsRead,
)
async def website_page_speed_insights_read(
    web_page_psi: WebsitePageSpeedInsights = Permission(
        AccessRead, get_website_page_psi_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePageSpeedInsightsRead:
    """Retrieve a single website page speed insights by id.

    Permissions:
    ------------
    `role=admin|manager` : read any website page speed insight

    `role=client` : read any website page speed insight that belongs to a website
        associated with the client via `client_website` table

    `role=employee` : read any website page speed insight that belongs to a website
        associated with a client via `client_website` table, associated with the user
        via the `user_client` table

    Returns:
    --------
    `WebsitePageSpeedInsightsRead` : the website page speed insights requested by psi_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=web_page_psi.website_id,
    )
    # return role based response
    response_out: WebsitePageSpeedInsightsRead = permissions.get_resource_response(
        resource=web_page_psi,
        responses={
            RoleUser: WebsitePageSpeedInsightsRead,
        },
    )
    return response_out


@router.delete(
    "/{psi_id}",
    name="website_page_speed_insights:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_psi_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def website_page_speed_insights_delete(
    web_page_psi: WebsitePageSpeedInsights = Permission(
        AccessDelete, get_website_page_psi_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a single website page speed insights by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any website page speed insight

    `role=client` : delete any website page speed insight that belongs to a website
        associated with the client via `client_website` table

    `role=employee` : delete any website page speed insight that belongs to a website
        associated with a client via `client_website` table, associated with the user
        via the `user_client` table

    Returns:
    --------
    `None`

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=web_page_psi.website_id,
    )
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=permissions.db)
    await web_psi_repo.delete(entry=web_page_psi)
    return None

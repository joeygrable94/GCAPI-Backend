from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.get_query import (
    CommonWebsitePageSpeedInsightsQueryParams,
    GetWebsitePageSpeedInsightsQueryParams,
)
from app.core.pagination import PageParams, Paginated
from app.entities.api.dependencies import get_async_db
from app.entities.api.errors import EntityNotFound, EntityRelationshipNotFound
from app.entities.auth.dependencies import (
    Permission,
    PermissionController,
    get_current_user,
    get_permission_controller,
)
from app.entities.website.crud import WebsiteRepository
from app.entities.website.model import Website
from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.model import WebsitePage
from app.entities.website_pagespeedinsight.crud import (
    WebsitePageSpeedInsightsRepository,
)
from app.entities.website_pagespeedinsight.dependencies import (
    get_website_page_psi_or_404,
)
from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights
from app.entities.website_pagespeedinsight.schemas import (
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
    WebsitePageSpeedInsightsRead,
)
from app.services.permission import (
    AccessDelete,
    AccessRead,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_page_speed_insights:list",
    dependencies=[
        Depends(CommonWebsitePageSpeedInsightsQueryParams),
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

    `role=organization` : only website page speed insights with a website_id associated with
        the organization via `organization_website` table

    `role=employee` : only website page speed insights with a website_id associated
        with a organization's website via `organization_website` table, associated with the user
        via `user_organization`

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
    response_out: Paginated[
        WebsitePageSpeedInsightsRead
    ] = await permissions.get_paginated_resource_response(
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
    return response_out


@router.post(
    "/",
    name="website_page_speed_insights:create",
    dependencies=[
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

    `role=organization` : create a new website page speed insights that belongs to a website
        associated with the organization via `organization_website` table

    `role=employee` : create a new website page speed insights that belongs to a website
        associated with a organization via `organization_website` table, associated with the user
        via the `user_organization` table

    Returns:
    --------
    `WebsitePageSpeedInsightsRead` : the newly created website page speed insights

    """
    # check if website_id provided
    if query.website_id is None:
        raise EntityNotFound(
            entity_info="Website id {}".format(query.website_id),
        )

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=query.website_id,
    )
    # check if website exists
    website_repo: WebsiteRepository = WebsiteRepository(permissions.db)
    a_website: Website | None = await website_repo.read(entry_id=query.website_id)
    if a_website is None:
        raise EntityNotFound(
            entity_info="Website id {}".format(query.website_id),
        )
    # check if page exists
    if query.page_id is None:
        raise EntityNotFound(
            entity_info="WebsitePage id {}".format(query.page_id),
        )
    web_page_repo: WebsitePageRepository = WebsitePageRepository(permissions.db)
    a_web_page: WebsitePage | None = await web_page_repo.read(entry_id=query.page_id)
    if a_web_page is None:
        raise EntityNotFound(
            entity_info="WebsitePage id {}".format(query.page_id),
        )
    a_web_page: WebsitePage | None = await web_page_repo.exists_by_fields(
        {
            "id": query.page_id,
            "website_id": query.website_id,
        }
    )
    if a_web_page is None:
        raise EntityRelationshipNotFound(
            entity_info="WebsitePage id = {}, website_id = {}".format(
                query.page_id,
                query.website_id,
            )
        )
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(permissions.db)
    psi_create: WebsitePageSpeedInsightsCreate = WebsitePageSpeedInsightsCreate(
        **psi_in.model_dump(),
        page_id=query.page_id,
        website_id=query.website_id,
    )
    psi_in_db: WebsitePageSpeedInsights = await web_psi_repo.create(schema=psi_create)
    return WebsitePageSpeedInsightsRead.model_validate(psi_in_db)


@router.get(
    "/{psi_id}",
    name="website_page_speed_insights:read",
    dependencies=[
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

    `role=organization` : read any website page speed insight that belongs to a website
        associated with the organization via `organization_website` table

    `role=employee` : read any website page speed insight that belongs to a website
        associated with a organization via `organization_website` table, associated with the user
        via the `user_organization` table

    Returns:
    --------
    `WebsitePageSpeedInsightsRead` : the website page speed insights requested by psi_id

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=web_page_psi.website_id,
    )

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

    `role=organization` : delete any website page speed insight that belongs to a website
        associated with the organization via `organization_website` table

    `role=employee` : delete any website page speed insight that belongs to a website
        associated with a organization via `organization_website` table, associated with the user
        via the `user_organization` table

    Returns:
    --------
    `None`

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=web_page_psi.website_id,
    )
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=permissions.db)
    await web_psi_repo.delete(entry=web_page_psi)
    return None

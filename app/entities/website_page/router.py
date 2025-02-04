from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import Select

from app.api.get_query import CommonWebsitePageQueryParams, GetWebsitePageQueryParams
from app.core.pagination import PageParams, Paginated
from app.entities.api.dependencies import get_async_db
from app.entities.api.errors import EntityAlreadyExists, EntityNotFound
from app.entities.auth.dependencies import (
    Permission,
    PermissionController,
    get_current_user,
    get_permission_controller,
)
from app.entities.website.crud import WebsiteRepository
from app.entities.website.model import Website
from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.dependencies import get_website_page_or_404
from app.entities.website_page.model import WebsitePage
from app.entities.website_page.schemas import (
    WebsitePageCreate,
    WebsitePageRead,
    WebsitePageUpdate,
)
from app.entities.website_pagespeedinsight.schemas import PSIDevice
from app.services.permission import (
    AccessDelete,
    AccessRead,
    AccessUpdate,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.tasks.background import bg_task_website_page_pagespeedinsights_fetch

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_pages:list",
    dependencies=[
        Depends(CommonWebsitePageQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsitePageRead],
)
async def website_page_list(
    query: GetWebsitePageQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsitePageRead]:
    """Retrieve a paginated list of website pages.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=organization` : only website pages with a website_id associated with the organization
        via `organization_website` table

    `role=employee` : only website pages with a website_id associated with a organization's
        website via `organization_website` table, associated with the user via `user_organization`

    Returns:
    --------
    `Paginated[WebsitePageRead]` : a paginated list of website pages,
        optionally filtered

    """
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(
        session=permissions.db
    )
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = web_pages_repo.query_list(
            website_id=query.website_id,
            is_active=query.is_active,
        )
    else:
        select_stmt = web_pages_repo.query_list(
            user_id=permissions.current_user.id,
            website_id=query.website_id,
            is_active=query.is_active,
        )
    response_out: Paginated[
        WebsitePageRead
    ] = await permissions.get_paginated_resource_response(
        table_name=WebsitePage.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleUser: WebsitePageRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="website_pages:create",
    dependencies=[
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePageRead,
)
async def website_page_create(
    website_page_in: WebsitePageCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePageRead:
    """Create a new website page.

    Permissions:
    ------------
    `role=admin|manager` : create a new website page

    `role=user` : create a new website page that belongs to a website associated
        with the organization via `organization_website` table, associated with the user via the
        `user_organization` table

    Returns:
    --------
    `WebsitePageRead` : the newly created website page

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page_in.website_id,
    )
    # check website page url is unique to website_id
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(
        session=permissions.db
    )
    a_page: WebsitePage | None = await web_pages_repo.exists_by_fields(
        {
            "url": website_page_in.url,
            "website_id": website_page_in.website_id,
        }
    )
    if a_page is not None:
        raise EntityAlreadyExists(
            entity_info="WebsitePage url = {}".format(website_page_in.url),
        )
    # check website page is assigned to a website
    a_website: Website | None = await website_repo.read(website_page_in.website_id)
    if a_website is None:
        raise EntityNotFound(
            entity_info="Website id = {}".format(website_page_in.website_id),
        )
    # create the website page
    website_page: WebsitePage = await web_pages_repo.create(website_page_in)
    response_out: WebsitePageRead = permissions.get_resource_response(
        resource=website_page,
        responses={
            RoleUser: WebsitePageRead,
        },
    )
    return response_out


@router.get(
    "/{page_id}",
    name="website_pages:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_page_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePageRead,
)
async def website_page_read(
    website_page: WebsitePage = Permission(AccessRead, get_website_page_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePageRead:
    """Retrieve a single website page by id.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=user` : only website pages with a website_id associated with a organization's
        website via `organization_website` table, associated with the user via `user_organization`

    Returns:
    --------
    `WebsitePageRead` : the website page requested by page_id

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )

    response_out: WebsitePageRead = permissions.get_resource_response(
        resource=website_page,
        responses={
            RoleUser: WebsitePageRead,
        },
    )
    return response_out


@router.patch(
    "/{page_id}",
    name="website_pages:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_page_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePageRead,
)
async def website_page_update(
    website_page_in: WebsitePageUpdate,
    website_page: WebsitePage = Permission(AccessUpdate, get_website_page_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePageRead:
    """Update a website page by id.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=user` : only website pages with a website_id associated with a organization's
        website via `organization_website` table, associated with the user via `user_organization`

    Returns:
    --------
    `WebsitePageRead` : the updated website page

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )

    web_pages_repo: WebsitePageRepository = WebsitePageRepository(
        session=permissions.db
    )

    query_page: dict | None = None
    if website_page_in.url is not None:
        query_page = {
            "url": website_page_in.url,
            "website_id": website_page.website_id,
        }

    # if website id provided
    if website_page_in.website_id is not None:
        # only update page if the user has access to the website
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=website_page_in.website_id,
        )
        # only update page if the website page exists
        website_repo = WebsiteRepository(session=permissions.db)
        a_website: Website | None = await website_repo.read(website_page_in.website_id)
        if a_website is None:
            raise EntityNotFound(
                entity_info="Website id = {}".format(website_page_in.website_id)
            )
        if website_page_in.url is not None:
            query_page["website_id"] = website_page_in.website_id

    if query_page is not None:
        a_page: WebsitePage | None = await web_pages_repo.exists_by_fields(query_page)
        if a_page is not None:
            raise EntityAlreadyExists(
                entity_info="WebsitePage url = {}, website_id = {}".format(
                    query_page["url"], query_page["website_id"]
                )
            )

    web_pages_repo = WebsitePageRepository(session=permissions.db)
    updated_website_page: WebsitePage | None = await web_pages_repo.update(
        entry=website_page, schema=website_page_in
    )

    response_out: WebsitePageRead = permissions.get_resource_response(
        resource=updated_website_page if updated_website_page else website_page,
        responses={
            RoleUser: WebsitePageRead,
        },
    )
    return response_out


@router.delete(
    "/{page_id}",
    name="website_pages:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_page_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def website_page_delete(
    website_page: WebsitePage = Permission(AccessDelete, get_website_page_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a website page by id.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=user` : only website pages with a website_id associated with a organization's
        website via `organization_website` table, associated with the user via `user_organization`

    Returns:
    --------
    `None`

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(
        session=permissions.db
    )
    await web_pages_repo.delete(entry=website_page)
    return None


@router.post(
    "/{page_id}/process-psi",
    name="website_pages:process_website_page_speed_insights",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_page_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePageRead,
)
async def website_page_process_website_page_speed_insights(
    bg_tasks: BackgroundTasks,
    website_page: WebsitePage = Permission(AccessUpdate, get_website_page_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePageRead:
    """A webhook to initiate processing a website page's page speed insights.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=user` : only website pages with a website_id associated with a organization's
        website via `organization_website` table, associated with the user via `user_organization`

    Returns:
    --------
    `WebsitePagePSIProcessing` : a website page PSI processing object containing the
        task_id's for the mobile and desktop page speed insights tasks

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )
    # check website page is assigned to a website
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_website: Website | None = await website_repo.read(website_page.website_id)
    if a_website is None:
        raise EntityNotFound(
            entity_info="Website id = {}".format(website_page.website_id),
        )
    fetch_page = a_website.get_link() + website_page.url
    # Send the task to the background.
    bg_tasks.add_task(
        bg_task_website_page_pagespeedinsights_fetch,
        website_id=str(a_website.id),
        page_id=str(website_page.id),
        fetch_url=fetch_page,
        device=PSIDevice.mobile,
    )
    bg_tasks.add_task(
        bg_task_website_page_pagespeedinsights_fetch,
        website_id=str(a_website.id),
        page_id=str(website_page.id),
        fetch_url=fetch_page,
        device=PSIDevice.desktop,
    )
    return WebsitePageRead.model_validate(website_page)

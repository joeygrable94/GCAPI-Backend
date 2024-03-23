from fastapi import APIRouter, Depends
from sqlalchemy import Select
from taskiq import AsyncTaskiqTask

from app.api.deps import (
    CommonWebsitePageQueryParams,
    GetWebsitePageQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_website_page_or_404,
)
from app.api.exceptions import WebsiteNotExists, WebsitePageAlreadyExists
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessRead,
    AccessUpdate,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.crud import WebsitePageRepository, WebsiteRepository
from app.models import Website, WebsitePage
from app.schemas import (
    PSIDevice,
    WebsitePageCreate,
    WebsitePagePSIProcessing,
    WebsitePageRead,
    WebsitePageUpdate,
)
from app.tasks import task_website_page_pagespeedinsights_fetch

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_pages:list",
    dependencies=[
        Depends(CommonWebsitePageQueryParams),
        Depends(auth.implicit_scheme),
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

    `role=client` : only website pages with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

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
            sitemap_id=query.sitemap_id,
        )
    else:  # TODO: test
        select_stmt = web_pages_repo.query_list(
            user_id=permissions.current_user.id,
            website_id=query.website_id,
            sitemap_id=query.sitemap_id,
        )
    response_out: Paginated[WebsitePageRead] = (
        await permissions.get_paginated_resource_response(
            table_name=WebsitePage.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleUser: WebsitePageRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="website_pages:create",
    dependencies=[
        Depends(auth.implicit_scheme),
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
        with the client via `client_website` table, associated with the user via the
        `user_client` table

    Returns:
    --------
    `WebsitePageRead` : the newly created website page

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page_in.website_id,
    )
    # check website page url is unique to website_id
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(
        session=permissions.db
    )
    a_page: WebsitePage | None = await web_pages_repo.exists_by_two(
        field_name_a="url",
        field_value_a=website_page_in.url,
        field_name_b="website_id",
        field_value_b=website_page_in.website_id,
    )
    if a_page is not None:
        raise WebsitePageAlreadyExists()
    # check website page is assigned to a website
    a_website: Website | None = await website_repo.read(website_page_in.website_id)
    if a_website is None:
        raise WebsiteNotExists()
    # create the website page
    website_page: WebsitePage = await web_pages_repo.create(website_page_in)
    # return role based response
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
        Depends(auth.implicit_scheme),
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

    `role=user` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `WebsitePageRead` : the website page requested by page_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )
    # return role based response
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
        Depends(auth.implicit_scheme),
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

    `role=user` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `WebsitePageRead` : the updated website page

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(
        session=permissions.db
    )
    updated_website_page: WebsitePage | None = await web_pages_repo.update(
        entry=website_page, schema=website_page_in
    )
    # return role based response
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
        Depends(auth.implicit_scheme),
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

    `role=user` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `None`

    """
    # verify current user has permission to take this action
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
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsitePagePSIProcessing,
)
async def website_page_process_website_page_speed_insights(
    website_page: WebsitePage = Permission(AccessUpdate, get_website_page_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsitePagePSIProcessing:
    """A webhook to initiate processing a website page's page speed insights.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=user` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `WebsitePagePSIProcessing` : a website page PSI processing object containing the
        task_id's for the mobile and desktop page speed insights tasks

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website_page.website_id,
    )
    # check website page is assigned to a website
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_website: Website | None = await website_repo.read(website_page.website_id)
    if a_website is None:
        raise WebsiteNotExists()
    fetch_page = a_website.get_link() + website_page.url
    # Send the task to the broker.
    website_page_psi_mobile: AsyncTaskiqTask = (
        await task_website_page_pagespeedinsights_fetch.kiq(
            website_id=str(a_website.id),
            page_id=str(website_page.id),
            fetch_url=fetch_page,
            device=PSIDevice.mobile,
        )
    )
    website_page_psi_desktop: AsyncTaskiqTask = (
        await task_website_page_pagespeedinsights_fetch.kiq(
            website_id=str(a_website.id),
            page_id=str(website_page.id),
            fetch_url=fetch_page,
            device=PSIDevice.desktop,
        )
    )
    return WebsitePagePSIProcessing(
        page=WebsitePageRead.model_validate(website_page),
        psi_mobile_task_id=website_page_psi_mobile.task_id,
        psi_desktop_task_id=website_page_psi_desktop.task_id,
    )

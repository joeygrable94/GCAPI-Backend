from typing import Any, List

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchWebPageOr404,
    GetWebsitePageQueryParams,
    get_async_db,
    get_website_page_or_404,
)
from app.api.exceptions import WebsiteNotExists, WebsitePageAlreadyExists
from app.core.security import auth
from app.crud import WebsitePageRepository, WebsiteRepository
from app.models import Website, WebsitePage
from app.schemas import (
    WebsitePageCreate,
    WebsitePagePSIProcessing,
    WebsitePageRead,
    WebsitePageUpdate,
)
from app.schemas.website_pagespeedinsights import PSIDevice
from app.worker import task_website_page_pagespeedinsights_fetch

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_pages:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsitePageRead],
)
async def website_page_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageQueryParams,
) -> List[WebsitePageRead] | List:
    """Retrieve a list of website pages.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=client` : only website pages with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `List[WebsitePageRead] | List[None]` : a list of website pages, optionally filtered,
        or returns an empty list

    """
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    website_list: List[WebsitePage] | List[None] | None = await web_pages_repo.list(
        page=query.page,
        website_id=query.website_id,
        sitemap_id=query.sitemap_id,
    )
    return (
        [WebsitePageRead.model_validate(w) for w in website_list]
        if website_list
        else []
    )


@router.post(
    "/",
    name="website_pages:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsitePageRead,
)
async def website_page_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page_in: WebsitePageCreate,
) -> WebsitePageRead:
    """Create a new website page.

    Permissions:
    ------------
    `role=admin|manager` : create a new website page

    `role=client` : create a new website page that belongs to a website associated with
        the client via `client_website` table

    `role=employee` : create a new website page that belongs to a website associated
        with the client via `client_website` table, associated with the user via the
        `user_client` table

    Returns:
    --------
    `WebsitePageRead` : the newly created website page

    """
    website_repo: WebsiteRepository = WebsiteRepository(session=db)
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    # check website page url is unique to website_id
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
    return WebsitePageRead.model_validate(website_page)


@router.get(
    "/{page_id}",
    name="website_pages:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=WebsitePageRead,
)
async def website_page_read(
    current_user: CurrentUser,
    website_page: FetchWebPageOr404,
) -> WebsitePageRead:
    """Retrieve a single website page by id.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=client` : only website pages with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `WebsitePageRead` : the website page requested by page_id

    """
    return WebsitePageRead.model_validate(website_page)


@router.patch(
    "/{page_id}",
    name="website_pages:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=WebsitePageRead,
)
async def website_page_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page: FetchWebPageOr404,
    website_page_in: WebsitePageUpdate,
) -> WebsitePageRead:
    """Update a website page by id.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=client` : only website pages with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `WebsitePageRead` : the updated website page

    """
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    updated_website_page: WebsitePage | None = await web_pages_repo.update(
        entry=website_page, schema=website_page_in
    )
    return (
        WebsitePageRead.model_validate(updated_website_page)
        if updated_website_page
        else WebsitePageRead.model_validate(website_page)
    )


@router.delete(
    "/{page_id}",
    name="website_pages:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=None,
)
async def website_page_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page: FetchWebPageOr404,
) -> None:
    """Delete a website page by id.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=client` : only website pages with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `None`

    """
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    await web_pages_repo.delete(entry=website_page)
    return None


@router.post(
    "/{page_id}/process-psi",
    name="website_pages:process_website_page_speed_insights",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=WebsitePagePSIProcessing,
)
async def website_page_process_website_page_speed_insights(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page: FetchWebPageOr404,
) -> WebsitePagePSIProcessing:
    """A webhook to initiate processing a website page's page speed insights.

    Permissions:
    ------------
    `role=admin|manager` : all website pages

    `role=client` : only website pages with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website pages with a website_id associated with a client's
        website via `client_website` table, associated with the user via `user_client`

    Returns:
    --------
    `WebsitePagePSIProcessing` : a website page PSI processing object containing the
        task_id's for the mobile and desktop page speed insights tasks

    """
    # check website page is assigned to a website
    website_repo: WebsiteRepository = WebsiteRepository(session=db)
    a_website: Website | None = await website_repo.read(website_page.website_id)
    if a_website is None:
        raise WebsiteNotExists()
    fetch_page = a_website.get_link() + website_page.url
    website_page_psi_mobile: Any = task_website_page_pagespeedinsights_fetch.delay(
        website_id=a_website.id,
        page_id=website_page.id,
        fetch_url=fetch_page,
        device=PSIDevice.mobile,
    )
    website_page_psi_desktop: Any = task_website_page_pagespeedinsights_fetch.delay(
        website_id=a_website.id,
        page_id=website_page.id,
        fetch_url=fetch_page,
        device=PSIDevice.desktop,
    )
    return WebsitePagePSIProcessing(
        page=WebsitePageRead.model_validate(website_page),
        psi_mobile_task_id=website_page_psi_mobile.task_id,
        psi_desktop_task_id=website_page_psi_desktop.task_id,
    )

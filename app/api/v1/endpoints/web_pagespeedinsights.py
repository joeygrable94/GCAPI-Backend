from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchWebPageSpeedInsightOr404,
    GetWebsitePageSpeedInsightsQueryParams,
    get_async_db,
    get_website_page_psi_or_404,
)
from app.api.exceptions import WebsiteNotExists, WebsitePageNotExists
from app.core.logger import logger
from app.core.security import auth
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
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsitePageSpeedInsightsRead],
)
async def website_page_speed_insights_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageSpeedInsightsQueryParams,
) -> List[WebsitePageSpeedInsightsRead] | List:
    """Retrieve a list of website page speed insights.

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
    `List[WebsitePageSpeedInsightsRead] | List[None]` : a list of website page speed
        insights, optionally filtered, or returns an empty list
    """
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=db)
    web_psi_list: List[WebsitePageSpeedInsights] | List[
        None
    ] | None = await web_psi_repo.list(
        page=query.page,
        website_id=query.website_id,
        page_id=query.page_id,
        devices=query.devices,
    )
    return (
        [WebsitePageSpeedInsightsRead.model_validate(wpsi) for wpsi in web_psi_list]
        if web_psi_list
        else []
    )


@router.post(
    "/",
    name="website_page_speed_insights:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsitePageSpeedInsightsRead,
)
async def website_page_speed_insights_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageSpeedInsightsQueryParams,
    psi_in: WebsitePageSpeedInsightsBase,
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
    # check if website exists
    if query.website_id is None:
        raise WebsiteNotExists()
    website_repo: WebsiteRepository = WebsiteRepository(db)
    a_website: Website | None = await website_repo.read(entry_id=query.website_id)
    if a_website is None:
        raise WebsiteNotExists()
    # check if page exists
    if query.page_id is None:
        raise WebsitePageNotExists()
    web_page_repo: WebsitePageRepository = WebsitePageRepository(db)
    a_web_page: WebsitePage | None = await web_page_repo.read(entry_id=query.page_id)
    if a_web_page is None:
        raise WebsitePageNotExists()
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(db)
    psi_create: WebsitePageSpeedInsightsCreate = WebsitePageSpeedInsightsCreate(
        **psi_in.model_dump(),
        page_id=query.page_id,
        website_id=query.website_id,
    )
    psi_in_db: WebsitePageSpeedInsights = await web_psi_repo.create(schema=psi_create)
    logger.info(
        "Created Website Page Speed Insights:",
        psi_in_db.id,
        psi_in_db.created_on,
    )
    return WebsitePageSpeedInsightsRead.model_validate(psi_in_db)


@router.get(
    "/{psi_id}",
    name="website_page_speed_insights:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_psi_or_404),
    ],
    response_model=WebsitePageSpeedInsightsRead,
)
async def website_page_speed_insights_read(
    current_user: CurrentUser,
    web_page_psi: FetchWebPageSpeedInsightOr404,
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
    return WebsitePageSpeedInsightsRead.model_validate(web_page_psi)


@router.delete(
    "/{psi_id}",
    name="website_page_speed_insights:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_psi_or_404),
    ],
    response_model=None,
)
async def website_page_speed_insights_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    web_page_psi: FetchWebPageSpeedInsightOr404,
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
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=db)
    await web_psi_repo.delete(entry=web_page_psi)
    return None

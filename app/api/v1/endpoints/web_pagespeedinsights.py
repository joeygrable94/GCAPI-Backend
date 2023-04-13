from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchWebPageSpeedInsightOr404,
    GetWebsitePageSpeedInsightsQueryParams,
    get_async_db,
    get_website_page_psi_or_404,
)
from app.api.errors import ErrorCode
from app.api.exceptions import WebsiteNotExists, WebsitePageNotExists
from app.core.auth import auth
from app.core.logger import logger
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
async def website_pagespeedinsights_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageSpeedInsightsQueryParams,
) -> List[WebsitePageSpeedInsightsRead] | List:
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
        [WebsitePageSpeedInsightsRead.from_orm(wpsi) for wpsi in web_psi_list]
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
async def website_pagespeedinsights_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageSpeedInsightsQueryParams,
    psi_in: WebsitePageSpeedInsightsBase,
) -> WebsitePageSpeedInsightsRead:
    try:
        # check if website exists
        if query.website_id is None:
            raise WebsiteNotExists()
        website_repo: WebsiteRepository = WebsiteRepository(db)
        # print(query.website_id)
        a_website: Website | None = await website_repo.read(entry_id=query.website_id)
        # print(a_website)
        if a_website is None:
            raise WebsiteNotExists()
        # check if page exists
        if query.page_id is None:
            raise WebsitePageNotExists()
        web_page_repo: WebsitePageRepository = WebsitePageRepository(db)
        a_web_page: WebsitePage | None = await web_page_repo.read(
            entry_id=query.page_id
        )
        if a_web_page is None:
            raise WebsitePageNotExists()
        # create website page speed insights
        web_psi_repo: WebsitePageSpeedInsightsRepository
        web_psi_repo = WebsitePageSpeedInsightsRepository(db)
        psi_create: WebsitePageSpeedInsightsCreate = WebsitePageSpeedInsightsCreate(
            **psi_in.dict(),
            page_id=query.page_id,
            website_id=query.website_id,
        )
        psi_in_db: WebsitePageSpeedInsights = await web_psi_repo.create(
            schema=psi_create
        )
        logger.info(
            "Created Website Page Speed Insights:",
            psi_in_db.id,
            psi_in_db.created_on,
        )
        return WebsitePageSpeedInsightsRead.from_orm(psi_in_db)
    except WebsiteNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_NOT_FOUND,
        )
    except WebsitePageNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_NOT_FOUND,
        )


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
async def website_pagespeedinsights_read(
    current_user: CurrentUser,
    web_page_psi: FetchWebPageSpeedInsightOr404,
) -> WebsitePageSpeedInsightsRead:
    return WebsitePageSpeedInsightsRead.from_orm(web_page_psi)


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
async def website_pagespeedinsights_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    web_page_psi: FetchWebPageSpeedInsightOr404,
) -> None:
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=db)
    await web_psi_repo.delete(entry=web_page_psi)
    return None

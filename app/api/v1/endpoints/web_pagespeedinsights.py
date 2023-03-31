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
from app.api.exceptions import WebsitePageSpeedInsightsNotExists
from app.core.auth import auth
from app.crud import WebsitePageSpeedInsightsRepository
from app.models import WebsitePageSpeedInsights
from app.schemas import WebsitePageSpeedInsightsRead

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_page_speed_insights:list_website_pages_insights",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsitePageSpeedInsightsRead],
)
async def website_page_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageSpeedInsightsQueryParams,
) -> List[WebsitePageSpeedInsightsRead] | List:
    web_psi_repo: WebsitePageSpeedInsightsRepository
    web_psi_repo = WebsitePageSpeedInsightsRepository(session=db)
    web_psi_list: List[WebsitePageSpeedInsights] | List[None] | None = await web_psi_repo.list(
        page=query.page,
        website_id=query.website_id,
        page_id=query.page_id,
        devices=query.devices,
    )
    if len(web_psi_list):
        return [WebsitePageSpeedInsightsRead.from_orm(wpsi) for wpsi in web_psi_list]
    return []


@router.get(
    "/{psi_id}",
    name="website_page_speed_insights:read_website_page_insights",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_psi_or_404),
    ],
    response_model=WebsitePageSpeedInsightsRead,
)
async def website_page_read(
    current_user: CurrentUser,
    web_page_psi: FetchWebPageSpeedInsightOr404,
) -> WebsitePageSpeedInsightsRead:
    try:
        if not web_page_psi:
            raise WebsitePageSpeedInsightsNotExists()
        return WebsitePageSpeedInsightsRead.from_orm(web_page_psi)
    except WebsitePageSpeedInsightsNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND,
        )


@router.delete(
    "/{psi_id}",
    name="website_page_speed_insights:delete_website_page_insights",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_psi_or_404),
    ],
    response_model=None,
)
async def website_page_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    web_page_psi: FetchWebPageSpeedInsightOr404,
) -> None:
    try:
        if not web_page_psi:
            raise WebsitePageSpeedInsightsNotExists()
        web_psi_repo: WebsitePageSpeedInsightsRepository
        web_psi_repo = WebsitePageSpeedInsightsRepository(session=db)
        await web_psi_repo.delete(entry=web_page_psi)
        return None
    except WebsitePageSpeedInsightsNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND,
        )

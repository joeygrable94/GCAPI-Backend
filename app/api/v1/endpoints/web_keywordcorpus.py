from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CommonWebsiteKeywordCorpusQueryParams,
    CurrentUser,
    FetchWebsiteKeywordCorpusOr404,
    GetWebsiteKeywordCorpusQueryParams,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_website_page_kwc_or_404,
)
from app.core.logger import logger
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
)
from app.crud import WebsiteKeywordCorpusRepository
from app.models import WebsiteKeywordCorpus
from app.schemas import WebsiteKeywordCorpusCreate, WebsiteKeywordCorpusRead

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_page_keyword_corpus:list",
    dependencies=[
        Depends(CommonWebsiteKeywordCorpusQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsiteKeywordCorpusRead],
)
async def website_page_keyword_corpus_list(
    query: GetWebsiteKeywordCorpusQueryParams,
    db: AsyncDatabaseSession,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteKeywordCorpusRead]:
    """Retrieve a paginated list of website keyword corpus.

    Permissions:
    ------------
    `role=admin|manager` : all website keyword corpus

    `role=client` : only website keyword corpus with a website_id associated with
        the client via `client_website` table

    `role=employee` : only website keyword corpus with a website_id associated
        with a client's website via `client_website` table, associated with the user
        via `user_client`

    Returns:
    --------
    `Paginated[WebsiteKeywordCorpusRead]` : a paginated list of website keyword corpus,
        optionally filtered

    """
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(session=db)
    response_out: Paginated[
        WebsiteKeywordCorpusRead
    ] = await permissions.get_paginated_resource_response(
        table_name=WebsiteKeywordCorpus.__tablename__,
        stmt=web_kwc_repo.query_list(
            website_id=query.website_id,
            page_id=query.page_id,
        ),
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: WebsiteKeywordCorpusRead,
            RoleManager: WebsiteKeywordCorpusRead,
            RoleClient: WebsiteKeywordCorpusRead,
            RoleEmployee: WebsiteKeywordCorpusRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="website_page_keyword_corpus:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsiteKeywordCorpusRead,
)
async def website_page_keyword_corpus_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsiteKeywordCorpusQueryParams,
    kwc_in: WebsiteKeywordCorpusCreate,
) -> WebsiteKeywordCorpusRead:
    """Create a new website keyword corpus.

    Permissions:
    ------------
    `role=admin|manager` : create a new website keyword corpus

    `role=client` : create a new website keyword corpus that belongs to a website
        associated with the client via `client_website` table

    `role=employee` : create a new website keyword corpus that belongs to a website
        associated with a client via `client_website` table, associated with the user
        via the `user_client` table

    Returns:
    --------
    `WebsiteKeywordCorpusRead` : the newly created website keyword corpus

    """
    # TODO: check if website exists?
    # TODO: check if page exists?
    # create website keyword corpus
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(db)
    kwc_in_db: WebsiteKeywordCorpus = await web_kwc_repo.create(schema=kwc_in)
    logger.info(
        "Created Website Keyword Corpus:",
        kwc_in_db.id,
        kwc_in_db.created_on,
    )
    return WebsiteKeywordCorpusRead.model_validate(kwc_in_db)


@router.get(
    "/{kwc_id}",
    name="website_page_keyword_corpus:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_kwc_or_404),
    ],
    response_model=WebsiteKeywordCorpusRead,
)
async def website_page_keyword_corpus_read(
    current_user: CurrentUser,
    web_page_kwc: FetchWebsiteKeywordCorpusOr404,
) -> WebsiteKeywordCorpusRead:
    """Retrieve a single website keyword corpus by id.

    Permissions:
    ------------
    `role=admin|manager` : read any website keyword corpus

    `role=client` : read any website keyword corpus that belongs to a website
        associated with the client via `client_website` table

    `role=employee` : read any website keyword corpus that belongs to a website
        associated with a client via `client_website` table, associated with the user
        via the `user_client` table

    Returns:
    --------
    `WebsiteKeywordCorpusRead` : the website keyword corpus requested by kwc_id

    """
    return WebsiteKeywordCorpusRead.model_validate(web_page_kwc)


@router.delete(
    "/{kwc_id}",
    name="website_page_keyword_corpus:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_kwc_or_404),
    ],
    response_model=None,
)
async def website_page_keyword_corpus_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    web_page_kwc: FetchWebsiteKeywordCorpusOr404,
) -> None:
    """Delete a single website keyword corpus by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any website keyword corpus

    `role=client` : delete any website keyword corpus that belongs to a website
        associated with the client via `client_website` table

    `role=employee` : delete any website keyword corpus that belongs to a website
        associated with a client via `client_website` table, associated with the user
        via the `user_client` table

    Returns:
    --------
    `None`

    """
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(session=db)
    await web_kwc_repo.delete(entry=web_page_kwc)
    return None

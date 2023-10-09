from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchWebsiteKeywordCorpusOr404,
    GetWebsiteKeywordCorpusQueryParams,
    get_async_db,
    get_website_page_kwc_or_404,
)
from app.api.exceptions import WebsiteNotExists, WebsitePageNotExists
from app.core.logger import logger
from app.core.security import auth
from app.crud import (
    WebsiteKeywordCorpusRepository,
    WebsitePageRepository,
    WebsiteRepository,
)
from app.models import Website, WebsiteKeywordCorpus, WebsitePage
from app.schemas import WebsiteKeywordCorpusCreate, WebsiteKeywordCorpusRead

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_page_keyword_corpus:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsiteKeywordCorpusRead],
)
async def website_page_keyword_corpus_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsiteKeywordCorpusQueryParams,
) -> List[WebsiteKeywordCorpusRead] | List:
    """Retrieve a list of website keyword corpus.

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
    `List[WebsiteKeywordCorpusRead] | List[None]` : a list of website keyword corpus,
        optionally filtered, or returns an empty list

    """
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(session=db)
    web_kwc_list: List[WebsiteKeywordCorpus] | List[
        None
    ] | None = await web_kwc_repo.list(
        page=query.page,
        website_id=query.website_id,
        page_id=query.page_id,
    )
    return (
        [WebsiteKeywordCorpusRead.model_validate(wkwc) for wkwc in web_kwc_list]
        if web_kwc_list
        else []
    )


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
    # create website keyword corpus
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(db)
    kwc_create: WebsiteKeywordCorpusCreate = WebsiteKeywordCorpusCreate(
        **kwc_in.model_dump(),
        page_id=query.page_id,
        website_id=query.website_id,
    )
    kwc_in_db: WebsiteKeywordCorpus = await web_kwc_repo.create(schema=kwc_create)
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

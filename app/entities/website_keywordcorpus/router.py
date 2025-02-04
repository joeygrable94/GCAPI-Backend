from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.get_query import (
    CommonWebsiteKeywordCorpusQueryParams,
    GetWebsiteKeywordCorpusQueryParams,
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
from app.entities.website_keywordcorpus.crud import WebsiteKeywordCorpusRepository
from app.entities.website_keywordcorpus.dependencies import get_website_page_kwc_or_404
from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus
from app.entities.website_keywordcorpus.schemas import (
    WebsiteKeywordCorpusCreate,
    WebsiteKeywordCorpusRead,
)
from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.model import WebsitePage
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
    name="website_page_keyword_corpus:list",
    dependencies=[
        Depends(CommonWebsiteKeywordCorpusQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsiteKeywordCorpusRead],
)
async def website_page_keyword_corpus_list(
    query: GetWebsiteKeywordCorpusQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteKeywordCorpusRead]:
    """Retrieve a paginated list of website keyword corpus.

    Permissions:
    ------------
    `role=admin|manager` : all website keyword corpus

    `role=organization` : only website keyword corpus with a website_id associated with
        the organization via `organization_website` table

    `role=employee` : only website keyword corpus with a website_id associated
        with a organization's website via `organization_website` table, associated with the user
        via `user_organization`

    Returns:
    --------
    `Paginated[WebsiteKeywordCorpusRead]` : a paginated list of website keyword corpus,
        optionally filtered

    """
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = web_kwc_repo.query_list(
            website_id=query.website_id,
            page_id=query.page_id,
        )
    else:
        select_stmt = web_kwc_repo.query_list(
            user_id=permissions.current_user.id,
            website_id=query.website_id,
            page_id=query.page_id,
        )
    response_out: Paginated[
        WebsiteKeywordCorpusRead
    ] = await permissions.get_paginated_resource_response(
        table_name=WebsiteKeywordCorpus.__tablename__,
        stmt=select_stmt,
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
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteKeywordCorpusRead,
)
async def website_page_keyword_corpus_create(
    kwc_in: WebsiteKeywordCorpusCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteKeywordCorpusRead:
    """Create a new website keyword corpus.

    Permissions:
    ------------
    `role=admin|manager` : create a new website keyword corpus

    `role=organization` : create a new website keyword corpus that belongs to a website
        associated with the organization via `organization_website` table

    `role=employee` : create a new website keyword corpus that belongs to a website
        associated with a organization via `organization_website` table, associated with the user
        via the `user_organization` table

    Returns:
    --------
    `WebsiteKeywordCorpusRead` : the newly created website keyword corpus

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=kwc_in.website_id,
    )
    # check if website exists
    website_repo: WebsiteRepository = WebsiteRepository(permissions.db)
    a_website: Website | None = await website_repo.read(entry_id=kwc_in.website_id)
    if a_website is None:
        raise EntityNotFound(entity_info="Website id = {}".format(kwc_in.website_id))
    web_page_repo: WebsitePageRepository = WebsitePageRepository(permissions.db)
    a_web_page: WebsitePage | None = await web_page_repo.read(entry_id=kwc_in.page_id)
    if a_web_page is None:
        raise EntityNotFound(entity_info="WebsitePage id = {}".format(kwc_in.page_id))
    a_web_page: WebsitePage | None = await web_page_repo.exists_by_fields(
        {
            "id": kwc_in.page_id,
            "website_id": kwc_in.website_id,
        }
    )
    if a_web_page is None:
        raise EntityRelationshipNotFound(
            entity_info="WebsitePage id = {}, website_id = {}".format(
                kwc_in.page_id,
                kwc_in.website_id,
            )
        )
    # create website keyword corpus
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(permissions.db)
    kwc_in_db: WebsiteKeywordCorpus = await web_kwc_repo.create(schema=kwc_in)
    return WebsiteKeywordCorpusRead.model_validate(kwc_in_db)


@router.get(
    "/{kwc_id}",
    name="website_page_keyword_corpus:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_page_kwc_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteKeywordCorpusRead,
)
async def website_page_keyword_corpus_read(
    web_page_kwc: WebsiteKeywordCorpus = Permission(
        AccessRead, get_website_page_kwc_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteKeywordCorpusRead:
    """Retrieve a single website keyword corpus by id.

    Permissions:
    ------------
    `role=admin|manager` : read any website keyword corpus

    `role=organization` : read any website keyword corpus that belongs to a website
        associated with the organization via `organization_website` table

    `role=employee` : read any website keyword corpus that belongs to a website
        associated with a organization via `organization_website` table, associated with the user
        via the `user_organization` table

    Returns:
    --------
    `WebsiteKeywordCorpusRead` : the website keyword corpus requested by kwc_id

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=web_page_kwc.website_id,
    )

    response_out: WebsiteKeywordCorpusRead = permissions.get_resource_response(
        resource=web_page_kwc,
        responses={
            RoleUser: WebsiteKeywordCorpusRead,
        },
    )
    return response_out


@router.delete(
    "/{kwc_id}",
    name="website_page_keyword_corpus:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_page_kwc_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def website_page_keyword_corpus_delete(
    web_page_kwc: WebsiteKeywordCorpus = Permission(
        AccessDelete, get_website_page_kwc_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a single website keyword corpus by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any website keyword corpus

    `role=organization` : delete any website keyword corpus that belongs to a website
        associated with the organization via `organization_website` table

    `role=employee` : delete any website keyword corpus that belongs to a website
        associated with a organization via `organization_website` table, associated with the user
        via the `user_organization` table

    Returns:
    --------
    `None`

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=web_page_kwc.website_id,
    )
    web_kwc_repo: WebsiteKeywordCorpusRepository
    web_kwc_repo = WebsiteKeywordCorpusRepository(session=permissions.db)
    await web_kwc_repo.delete(entry=web_page_kwc)
    return None

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonWebsiteMapQueryParams,
    GetWebsiteMapQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_website_map_or_404,
)
from app.api.exceptions import EntityAlreadyExists, EntityNotFound, XmlInvalid
from app.core.pagination import PageParams, Paginated
from app.core.security.permissions import (
    AccessDelete,
    AccessRead,
    AccessUpdate,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.crud import WebsiteMapRepository, WebsiteRepository
from app.models import Website, WebsiteMap
from app.schemas import (
    WebsiteMapCreate,
    WebsiteMapProcessing,
    WebsiteMapRead,
    WebsiteMapUpdate,
)
from app.tasks import bg_task_website_sitemap_process_xml

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_sitemaps:list",
    dependencies=[
        Depends(CommonWebsiteMapQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsiteMapRead],
)
async def sitemap_list(
    query: GetWebsiteMapQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteMapRead]:
    """Retrieve a paginated list of website maps.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=user` : only website maps with a website_id associated with the clients
        via `client_website` table, associated with the user via `user_client` table

    Returns:
    --------
    `Paginated[WebsiteMapRead]` : a paginated list of website maps,
        optionally filtered

    """
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = sitemap_repo.query_list(
            website_id=query.website_id,
        )
    else:
        select_stmt = sitemap_repo.query_list(
            user_id=permissions.current_user.id,
            website_id=query.website_id,
        )
    response_out: Paginated[
        WebsiteMapRead
    ] = await permissions.get_paginated_resource_response(
        table_name=WebsiteMap.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleUser: WebsiteMapRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="website_sitemaps:create",
    dependencies=[
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteMapRead,
)
async def sitemap_create(
    sitemap_in: WebsiteMapCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteMapRead:
    """Create a new website map.

    Permissions:
    ------------
    `role=admin|manager` : create a new website map

    `role=user` : create a new website map associated with a website that belongs to
        a client the user belongs to via `user_client` table

    Returns:
    --------
    `WebsiteMapRead` : the newly created website map

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=sitemap_in.website_id,
    )
    # check website being assigned a sitemap exists
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_website: Website | None = await website_repo.read(sitemap_in.website_id)
    if a_website is None:
        raise EntityNotFound(
            entity_info="Website id = {}".format(sitemap_in.website_id)
        )
    # check website map url is a valid XML document
    fetch_website_map_url: str = "{}/{}".format(
        a_website.get_link(),
        sitemap_in.url.lstrip("/"),
    )
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=permissions.db)
    sitemap_url_valid: bool = sitemap_repo.is_sitemap_url_xml_valid(
        fetch_website_map_url
    )
    if not sitemap_url_valid:
        raise XmlInvalid()
    # check website map url is unique to website_id
    a_sitemap: WebsiteMap | None = await sitemap_repo.exists_by_fields(
        {
            "url": sitemap_in.url,
            "website_id": sitemap_in.website_id,
        }
    )
    if a_sitemap is not None:
        raise EntityAlreadyExists(
            entity_info="WebsiteMap url = {}".format(sitemap_in.url)
        )
    # create website map
    sitemap: WebsiteMap = await sitemap_repo.create(sitemap_in)

    response_out: WebsiteMapRead = permissions.get_resource_response(
        resource=sitemap,
        responses={
            RoleUser: WebsiteMapRead,
        },
    )
    return response_out


@router.get(
    "/{sitemap_id}",
    name="website_sitemaps:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_map_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteMapRead,
)
async def sitemap_read(
    sitemap: WebsiteMap = Permission(AccessRead, get_website_map_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteMapRead:
    """Retrieve a single website map by id.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=user` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `WebsiteMapRead` : the website map

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=sitemap.website_id,
    )

    response_out: WebsiteMapRead = permissions.get_resource_response(
        resource=sitemap,
        responses={
            RoleUser: WebsiteMapRead,
        },
    )
    return response_out


@router.patch(
    "/{sitemap_id}",
    name="website_sitemaps:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_map_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteMapRead,
)
async def sitemap_update(
    sitemap_in: WebsiteMapUpdate,
    sitemap: WebsiteMap = Permission(AccessUpdate, get_website_map_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteMapRead:
    """Update a website map by id.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=user` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `WebsiteMapRead` : the updated website map

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=sitemap.website_id,
    )
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=permissions.db)
    if sitemap_in.url is not None:
        website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
        a_website: Website | None = await website_repo.read(sitemap.website_id)
        if a_website is None:
            raise EntityNotFound(
                entity_info="Website id = {}".format(sitemap_in.website_id)
            )
        fetch_website_map_url: str = "{}/{}".format(
            a_website.get_link(),
            sitemap_in.url.lstrip("/"),
        )
        sitemap_url_valid: bool = sitemap_repo.is_sitemap_url_xml_valid(
            fetch_website_map_url
        )
        if not sitemap_url_valid:
            raise XmlInvalid()
        # website assigned sitemap URL must be unique
        a_sitemap: WebsiteMap | None = await sitemap_repo.exists_by_fields(
            {
                "url": sitemap_in.url,
                "website_id": sitemap.website_id,
            }
        )
        if a_sitemap is not None:
            raise EntityAlreadyExists(
                entity_info="WebsiteMap url = {}".format(sitemap_in.url)
            )
    updated_sitemap: WebsiteMap | None = await sitemap_repo.update(
        entry=sitemap, schema=sitemap_in
    )
    response_out: WebsiteMapRead = permissions.get_resource_response(
        resource=updated_sitemap if updated_sitemap else sitemap,
        responses={
            RoleUser: WebsiteMapRead,
        },
    )
    return response_out


@router.delete(
    "/{sitemap_id}",
    name="website_sitemaps:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_map_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def sitemap_delete(
    sitemap: WebsiteMap = Permission(AccessDelete, get_website_map_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a website map by id.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=user` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `None`

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=sitemap.website_id,
    )
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=permissions.db)
    await sitemap_repo.delete(entry=sitemap)
    return None


@router.get(
    "/{sitemap_id}/process-pages",
    name="website_sitemaps:process_sitemap_pages",
    dependencies=[
        Depends(get_async_db),
        Depends(get_website_map_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteMapProcessing,
)
async def sitemap_process_sitemap_pages(
    bg_tasks: BackgroundTasks,
    sitemap: WebsiteMap = Permission(AccessUpdate, get_website_map_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteMapProcessing:
    """A webhook to initiate processing a sitemap's pages.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=user` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `WebsiteMapProcessing` : the task_id of the worker task

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=sitemap.website_id,
    )
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_website: Website | None = await website_repo.read(sitemap.website_id)
    if a_website is None:
        raise EntityNotFound(entity_info="Website id = {}".format(sitemap.website_id))
    fetch_website_map_url: str = "{}/{}".format(
        a_website.get_link(),
        sitemap.url.lstrip("/"),
    )
    # check website map url is a valid XML document
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=permissions.db)
    sitemap_url_valid = sitemap_repo.is_sitemap_url_xml_valid(fetch_website_map_url)
    if not sitemap_url_valid:
        raise XmlInvalid()
    # Send the task to the broker.
    bg_tasks.add_task(
        bg_task_website_sitemap_process_xml,
        website_id=str(sitemap.website_id),
        sitemap_id=str(sitemap.id),
        sitemap_url=str(sitemap.url),
    )
    return WebsiteMapProcessing(
        url=sitemap.url,
        website_id=sitemap.website_id,
        sitemap_id=sitemap.id,
    )

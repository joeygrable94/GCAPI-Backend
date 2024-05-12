from fastapi import APIRouter, Depends
from sqlalchemy import Select
from taskiq import AsyncTaskiqTask

from app.api.deps import (
    CommonClientQueryParams,
    GetClientQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_bdx_feed_404,
    get_current_user,
    get_permission_controller,
)
from app.api.exceptions import BdxFeedAlreadyExists, ClientNotExists
from app.api.utilities import create_or_read_data_bucket
from app.core.logger import logger
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteRelated,
    AccessDeleteSelf,
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateRelated,
    AccessUpdateSelf,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import BdxFeedRepository, ClientRepository
from app.models import BdxFeed, Client
from app.schemas import BdxFeedCreate, BdxFeedRead, BdxFeedUpdate
from app.tasks import task_create_client_data_bucket

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="bdx_feed:list",
    dependencies=[
        Depends(CommonClientQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[BdxFeedRead],
)
async def bdx_feed_list(
    query: GetClientQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[BdxFeedRead]:
    """Retrieve a paginated list of bdx_feeds.

    Permissions:
    ------------
    `role=admin|manager` : all bdx_feeds

    `role=user` : only bdx_feeds that belong to the user

    Returns:
    --------
    `Paginated[BdxFeedRead]` : a paginated list of bdx_feeds,
        optionally filtered

    """
    # formulate the select statement based on the current user's role
    bdx_repo: BdxFeedRepository = BdxFeedRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = bdx_repo.query_list(client_id=query.client_id)
    else:
        select_stmt = bdx_repo.query_list(
            user_id=permissions.current_user.id,
            client_id=query.client_id,
        )
    response_out: Paginated[BdxFeedRead] = (
        await permissions.get_paginated_resource_response(
            table_name=BdxFeed.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: BdxFeedRead,
                RoleManager: BdxFeedRead,
                RoleClient: BdxFeedRead,
                RoleEmployee: BdxFeedRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="bdx_feed:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=BdxFeedRead,
)
async def bdx_feed_create(
    bdx_in: BdxFeedCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> BdxFeedRead:
    """Create a new bdx_feeds.

    Permissions:
    ------------
    `role=admin|manager` : create new bdx_feeds for all clients

    `role=user` : create only bdx_feeds that belong to any clients associated
        with the current user

    Returns:
    --------
    `BdxFeedRead` : the newly created bdx_feed

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=bdx_in.client_id,
    )
    bdx_repo: BdxFeedRepository = BdxFeedRepository(session=permissions.db)
    a_bdx: BdxFeed | None = await bdx_repo.exists_by_fields(
        {
            "username": bdx_in.username,
            "serverhost": bdx_in.serverhost,
            "xml_file_key": bdx_in.xml_file_key,
        }
    )
    if a_bdx:
        raise BdxFeedAlreadyExists()
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    a_client: Client | None = await client_repo.read(entry_id=bdx_in.client_id)
    if a_client is None:
        raise ClientNotExists()
    new_bdx_feed: BdxFeed = await bdx_repo.create(bdx_in)
    data_bucket = await create_or_read_data_bucket(
        bucket_prefix=f"client/{a_client.slug}/bdxfeed/{new_bdx_feed.xml_file_key}",
        client_id=str(a_client.id),
        bdx_feed_id=str(new_bdx_feed.id),
        gcft_id=None,
    )
    if data_bucket is None:  # pragma: no cover
        logger.info(
            "Error creating data bucket for client bdx feed, running in worker..."
        )
        create_data_bucket_task: AsyncTaskiqTask = (  # noqa: E501, F841
            await task_create_client_data_bucket.kiq(
                bucket_prefix=f"client/{a_client.slug}/bdxfeed/{new_bdx_feed.xml_file_key}",  # noqa: E501
                client_id=str(a_client.id),
                bdx_feed_id=str(new_bdx_feed.id),
                gcft_id=None,
            )
        )
    # return role based response
    response_out: BdxFeedRead = permissions.get_resource_response(
        resource=new_bdx_feed,
        responses={
            RoleUser: BdxFeedRead,
        },
    )
    return response_out


@router.get(
    "/{bdx_id}",
    name="bdx_feed:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_bdx_feed_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=BdxFeedRead,
)
async def bdx_feed_read(
    bdx_feed: BdxFeed = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_bdx_feed_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> BdxFeedRead:
    """Retrieve a single bdx_feed by id.

    Permissions:
    ------------
    `role=admin|manager` : read all bdx_feeds

    `role=user` : read only bdx_feeds that belong to any clients
        associated with the current user

    Returns:
    --------
    `BdxFeedRead` : the bdx_feed matching the bdx_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=bdx_feed.client_id,
    )
    # return role based response
    response_out: BdxFeedRead = permissions.get_resource_response(
        resource=bdx_feed,
        responses={
            RoleUser: BdxFeedRead,
        },
    )
    return response_out


@router.patch(
    "/{bdx_id}",
    name="bdx_feed:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_bdx_feed_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=BdxFeedRead,
)
async def bdx_feed_update(
    bdx_in: BdxFeedUpdate,
    bdx_feed: BdxFeed = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_bdx_feed_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> BdxFeedRead:
    """Update a bdx_feed by id.

    Permissions:
    ------------
    `role=admin|manager` : update all bdx_feeds

    `role=user` : update only bdx_feeds that belong to any clients associated
        with the current user

    Returns:
    --------
    `BdxFeedRead` : the updated bdx_feed

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=bdx_in,
        schema_privileges={
            RoleUser: BdxFeedUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=bdx_feed.client_id,
    )
    bdx_repo: BdxFeedRepository = BdxFeedRepository(session=permissions.db)
    a_bdx_feed: BdxFeed | None = None
    b_bdx_feed: BdxFeed | None = None
    if bdx_in.username is not None:
        a_bdx_feed = await bdx_repo.read_by(
            field_name="username", field_value=bdx_in.username
        )
    if bdx_in.serverhost is not None:
        b_bdx_feed = await bdx_repo.read_by(
            field_name="serverhost", field_value=bdx_in.serverhost
        )
    # only update if the username and server name are different
    if b_bdx_feed is not None and a_bdx_feed is not None:
        raise BdxFeedAlreadyExists()
    if bdx_in.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=bdx_in.client_id,
        )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(entry_id=bdx_in.client_id)
        if a_client is None:
            raise ClientNotExists()
    updated_bdx_feed: BdxFeed | None = await bdx_repo.update(
        entry=bdx_feed, schema=bdx_in
    )
    # return role based response
    response_out: BdxFeedRead = permissions.get_resource_response(
        resource=updated_bdx_feed if updated_bdx_feed else bdx_feed,
        responses={
            RoleUser: BdxFeedRead,
        },
    )
    return response_out


@router.delete(
    "/{bdx_id}",
    name="bdx_feed:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_bdx_feed_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def bdx_feed_delete(
    bdx_feed: BdxFeed = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_bdx_feed_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a bdx_feed by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any bdx_feeds

    `role=user` : delete only bdx_feeds that belong to any clients associated
        with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=bdx_feed.client_id,
    )
    bdx_repo: BdxFeedRepository = BdxFeedRepository(session=permissions.db)
    await bdx_repo.delete(entry=bdx_feed)
    return None

from fastapi import APIRouter, Depends
from httpx import Client
from pydantic import UUID4
from pydantic_core import ValidationError
from sqlalchemy import Select

from app.api.get_query import CommonGoPropertyQueryParams, GetGoPropertyQueryParams
from app.core.pagination import PageParams, Paginated
from app.entities.api.dependencies import get_async_db
from app.entities.api.errors import EntityAlreadyExists, EntityNotFound
from app.entities.auth.dependencies import (
    Permission,
    PermissionController,
    get_current_user,
    get_permission_controller,
)
from app.entities.client.crud import ClientRepository
from app.entities.client.errors import ClientNotFound
from app.entities.go_ga4.crud import GoAnalytics4PropertyRepository
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4PropertyUpdate,
    RequestGoAnalytics4PropertyCreate,
)
from app.entities.go_ga4_stream.crud import GoAnalytics4StreamRepository
from app.entities.go_ga4_stream.model import GoAnalytics4Stream
from app.entities.go_ga4_stream.schemas import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
    GoAnalytics4StreamUpdate,
    RequestGoAnalytics4StreamCreate,
)
from app.entities.go_gads.crud import GoAdsPropertyRepository
from app.entities.go_gads.model import GoAdsProperty
from app.entities.go_gads.schemas import (
    GoAdsPropertyCreate,
    GoAdsPropertyRead,
    GoAdsPropertyUpdate,
    RequestGoAdsPropertyCreate,
)
from app.entities.go_gsc.crud import GoSearchConsolePropertyRepository
from app.entities.go_gsc.model import GoSearchConsoleProperty
from app.entities.go_gsc.schemas import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
    GoSearchConsolePropertyUpdate,
    RequestGoSearchConsolePropertyCreate,
)
from app.entities.go_property.dependencies import get_go_property_or_404
from app.entities.go_property.schemas import GooglePlatformType
from app.entities.platform.crud import PlatformRepository
from app.entities.website.crud import WebsiteRepository
from app.entities.website.model import Website
from app.services.permission import (
    AccessDelete,
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
)

router: APIRouter = APIRouter()


@router.get(
    "/{platform_type}",
    name="go_property:list",
    dependencies=[
        Depends(CommonGoPropertyQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[
        GoAnalytics4PropertyRead
        | GoAnalytics4StreamRead
        | GoSearchConsolePropertyRead
        | GoAdsPropertyRead
    ],
)
async def go_property_list(
    query: GetGoPropertyQueryParams,
    platform_type: GooglePlatformType,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[
    GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead
]:
    """Retrieve a paginated list of google properties: analytics, analytics stream, search concole, ads, etc.

    Permissions:
    ------------
    `role=admin|manager` : list all google properties

    `role=employee` : list only google properties that belong to any clients
        associated with the current user

    Returns:
    --------
    `Paginated[GoAnalytics4PropertyRead | GoAnalytics4StreamRead | GoSearchConsolePropertyRead | GoAdsPropertyRead]` : a paginated list of clients, optionally filtered

    """
    select_stmt: Select
    if platform_type == GooglePlatformType.ga4:
        ga4_repo = GoAnalytics4PropertyRepository(session=permissions.db)
        if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
            select_stmt = ga4_repo.query_list(
                user_id=query.user_id, client_id=query.client_id
            )
        else:
            select_stmt = ga4_repo.query_list(
                user_id=permissions.current_user.id, client_id=query.client_id
            )
        response_out: Paginated[
            GoAnalytics4PropertyRead
        ] = await permissions.get_paginated_resource_response(
            table_name=GoAnalytics4Property.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoAnalytics4PropertyRead,
                RoleManager: GoAnalytics4PropertyRead,
                RoleEmployee: GoAnalytics4PropertyRead,
                RoleClient: GoAnalytics4PropertyRead,
            },
        )
        return response_out
    elif platform_type == GooglePlatformType.ga4_stream:
        ga4_stream_repo = GoAnalytics4StreamRepository(session=permissions.db)
        if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
            select_stmt = ga4_stream_repo.query_list(
                user_id=query.user_id,
                website_id=query.website_id,
                ga4_id=query.ga4_id,
            )
        else:
            select_stmt = ga4_stream_repo.query_list(
                user_id=permissions.current_user.id,
                website_id=query.website_id,
                ga4_id=query.ga4_id,
            )
        response_out: Paginated[
            GoAnalytics4StreamRead
        ] = await permissions.get_paginated_resource_response(
            table_name=GoAnalytics4Stream.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoAnalytics4StreamRead,
                RoleManager: GoAnalytics4StreamRead,
                RoleEmployee: GoAnalytics4StreamRead,
                RoleClient: GoAnalytics4StreamRead,
            },
        )
        return response_out
    elif platform_type == GooglePlatformType.gads:
        gads_repo = GoAdsPropertyRepository(session=permissions.db)
        if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
            select_stmt = gads_repo.query_list(
                user_id=query.user_id,
                client_id=query.client_id,
                website_id=query.website_id,
            )
        else:
            select_stmt = gads_repo.query_list(
                user_id=permissions.current_user.id,
                client_id=query.client_id,
                website_id=query.website_id,
            )
        response_out: Paginated[
            GoAdsPropertyRead
        ] = await permissions.get_paginated_resource_response(
            table_name=GoAdsProperty.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoAdsPropertyRead,
                RoleManager: GoAdsPropertyRead,
                RoleEmployee: GoAdsPropertyRead,
                RoleClient: GoAdsPropertyRead,
            },
        )
        return response_out
    elif platform_type == GooglePlatformType.gsc:
        gsc_repo = GoSearchConsolePropertyRepository(session=permissions.db)
        if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
            select_stmt = gsc_repo.query_list(
                user_id=query.user_id,
                client_id=query.client_id,
                website_id=query.website_id,
            )
        else:
            select_stmt = gsc_repo.query_list(
                user_id=permissions.current_user.id,
                client_id=query.client_id,
                website_id=query.website_id,
            )
        response_out: Paginated[
            GoSearchConsolePropertyRead
        ] = await permissions.get_paginated_resource_response(
            table_name=GoSearchConsoleProperty.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoSearchConsolePropertyRead,
                RoleManager: GoSearchConsolePropertyRead,
                RoleEmployee: GoSearchConsolePropertyRead,
                RoleClient: GoSearchConsolePropertyRead,
            },
        )
        return response_out
    raise EntityNotFound(  # pragma: no cover - safety check
        entity_info=f"Google Property {platform_type} not found",
    )


@router.post(
    "/{platform_type}",
    name="go_property:create",
    dependencies=[
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead,
)
async def go_property_create(
    platform_type: GooglePlatformType,
    go_property_in: RequestGoAnalytics4PropertyCreate
    | RequestGoAnalytics4StreamCreate
    | RequestGoSearchConsolePropertyCreate
    | RequestGoAdsPropertyCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> (
    GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead
):
    """Create a new google property: analytics, analytics stream, search concole, ads, etc.

    Permissions:
    ------------
    `role=admin|manager` : create new google properties for all clients

    `role=user` : create only google properties that belong to any clients
        associated with the current user

    Returns:
    --------
    `GoAnalytics4PropertyRead | GoAnalytics4StreamRead | GoSearchConsolePropertyRead | GoAdsPropertyRead` : the newly created google property

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_property_in.client_id,
    )
    new_go_property: (
        GoAnalytics4PropertyRead
        | GoAnalytics4StreamRead
        | GoSearchConsolePropertyRead
        | GoAdsPropertyRead
    ) = None
    if platform_type == GooglePlatformType.ga4:
        go_property_in = RequestGoAnalytics4PropertyCreate.model_validate(
            go_property_in
        )
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="ga4")
        if a_platform is None:  # pragma: no cover
            raise EntityNotFound(entity_info="Platform slug = ga4")
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        check_property_id: str = data.get("property_id", "")
        ga4_repo = GoAnalytics4PropertyRepository(session=permissions.db)
        a_ga4_title = await ga4_repo.read_by(
            field_name="title", field_value=check_title
        )
        a_ga4_property_id = await ga4_repo.read_by(
            field_name="property_id", field_value=check_property_id
        )
        if a_ga4_title is not None or a_ga4_property_id is not None:
            raise EntityAlreadyExists(
                entity_info=f"GoAnalytics4Property {go_property_in.title}"
            )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(
            entry_id=go_property_in.client_id
        )
        if a_client is None:
            raise ClientNotFound()
        new_ga4 = await ga4_repo.create(
            GoAnalytics4PropertyCreate(
                **go_property_in.model_dump(), platform_id=a_platform.id
            )
        )
        new_go_property = GoAnalytics4PropertyRead.model_validate(new_ga4)
    elif platform_type == GooglePlatformType.ga4_stream:
        go_property_in = RequestGoAnalytics4StreamCreate.model_validate(go_property_in)
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_property_in.website_id,
        )
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="ga4")
        if a_platform is None:  # pragma: no cover
            raise EntityNotFound(entity_info="Platform slug = ga4")
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        check_stream_id: str = data.get("stream_id", "")
        check_measurement_id: str = data.get("measurement_id", "")
        ga4_stream_repo = GoAnalytics4StreamRepository(session=permissions.db)
        a_ga4_stream_title = await ga4_stream_repo.read_by(
            field_name="title", field_value=check_title
        )
        a_ga4_stream_property_id = await ga4_stream_repo.read_by(
            field_name="stream_id", field_value=check_stream_id
        )
        a_ga4_stream_measurement_id = await ga4_stream_repo.read_by(
            field_name="measurement_id", field_value=check_measurement_id
        )
        if (
            a_ga4_stream_title is not None
            or a_ga4_stream_property_id is not None
            or a_ga4_stream_measurement_id is not None
        ):
            raise EntityAlreadyExists(
                entity_info=f"GoAnalytics4Stream {go_property_in.title}"
            )
        website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
        a_website: Website | None = await website_repo.read(
            entry_id=go_property_in.website_id
        )
        if a_website is None:
            raise EntityNotFound(
                entity_info="Website id = {}".format(go_property_in.website_id)
            )
        ga4_repo = GoAnalytics4PropertyRepository(session=permissions.db)
        a_ga4 = await ga4_repo.read(entry_id=go_property_in.ga4_id)
        if a_ga4 is None:
            raise EntityNotFound(
                entity_info="GoAnalytics4Property id = {}".format(go_property_in.ga4_id)
            )
        new_ga4_stream = await ga4_stream_repo.create(
            GoAnalytics4StreamCreate(
                title=check_title,
                stream_id=check_stream_id,
                measurement_id=check_measurement_id,
                ga4_id=go_property_in.ga4_id,
                website_id=go_property_in.website_id,
            )
        )
        new_go_property = GoAnalytics4StreamRead.model_validate(new_ga4_stream)
    elif platform_type == GooglePlatformType.gsc:
        go_property_in = RequestGoSearchConsolePropertyCreate.model_validate(
            go_property_in
        )
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_property_in.website_id,
        )
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="gsc")
        if a_platform is None:  # pragma: no cover
            raise EntityNotFound(entity_info="Platform slug = gsc")
        go_sc_repo = GoSearchConsolePropertyRepository(session=permissions.db)
        a_go_sc_title = await go_sc_repo.read_by(
            field_name="title", field_value=go_property_in.title
        )
        a_go_sc_client_website = await go_sc_repo.exists_by_fields(
            {
                "client_id": go_property_in.client_id,
                "website_id": go_property_in.website_id,
            }
        )
        if a_go_sc_title is not None:
            raise EntityAlreadyExists(
                entity_info="GoSearchConsoleProperty title = {}".format(
                    go_property_in.title,
                )
            )
        if a_go_sc_client_website is not None:
            raise EntityAlreadyExists(
                entity_info="GoSearchConsoleProperty id = {}".format(
                    a_go_sc_client_website.id,
                )
            )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(
            entry_id=go_property_in.client_id
        )
        if a_client is None:
            raise ClientNotFound()
        website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
        a_website: Website | None = await website_repo.read(
            entry_id=go_property_in.website_id
        )
        if a_website is None:
            raise EntityNotFound(
                entity_info="Website id = {}".format(go_property_in.website_id)
            )
        new_go_sc = await go_sc_repo.create(
            GoSearchConsolePropertyCreate(
                **go_property_in.model_dump(), platform_id=a_platform.id
            )
        )
        new_go_property = GoSearchConsolePropertyRead.model_validate(new_go_sc)
    elif platform_type == GooglePlatformType.gads:
        go_property_in = RequestGoAdsPropertyCreate.model_validate(go_property_in)
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="gads")
        if a_platform is None:  # pragma: no cover
            raise EntityNotFound(entity_info="Platform slug = gads")
        goads_repo = GoAdsPropertyRepository(session=permissions.db)
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        check_measurement_id: str = data.get("measurement_id", "")
        a_gads_title = await goads_repo.read_by(
            field_name="title", field_value=check_title
        )
        a_gads_measurement_id = await goads_repo.read_by(
            field_name="measurement_id", field_value=check_measurement_id
        )
        if a_gads_measurement_id is not None or a_gads_title is not None:
            raise EntityAlreadyExists(
                entity_info=f"GoAdsProperty({go_property_in.title})"
            )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(
            entry_id=go_property_in.client_id
        )
        if a_client is None:
            raise ClientNotFound()
        new_goads = await goads_repo.create(
            GoAdsPropertyCreate(
                **go_property_in.model_dump(), platform_id=a_platform.id
            )
        )
        new_go_property = GoAdsPropertyRead.model_validate(new_goads)
    if new_go_property is None:  # pragma: no cover - safety check
        raise EntityNotFound(entity_info=f"Google Property {platform_type} not created")
    return new_go_property


@router.get(
    "/{platform_type}/{go_property_id}",
    name="go_property:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_go_property_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead,
)
async def go_property_read(
    platform_type: GooglePlatformType,
    go_property: GoAnalytics4Property
    | GoAnalytics4Stream
    | GoSearchConsoleProperty
    | GoAdsProperty = Permission(
        [AccessRead, AccessReadRelated, AccessReadSelf], get_go_property_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> (
    GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead
):
    """Retrieve a single google property account by platform_type and id.

    Permissions:
    ------------
    `role=admin|manager` : read all google properties

    `role=user` : only google properties associated with clients they are associated with via
        `user_client` table, and associated with the client via `client_platform` table

    Returns:
    --------
    `GoAnalytics4PropertyRead | GoAnalytics4StreamRead | GoSearchConsolePropertyRead | GoAdsPropertyRead` : the google property account matching the platform_type and property_id

    """
    if hasattr(go_property, "client_id"):
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=go_property.client_id,
        )
    if hasattr(go_property, "website_id"):
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_property.website_id,
        )
    out_schema: (
        GoAnalytics4PropertyRead
        | GoAnalytics4StreamRead
        | GoSearchConsolePropertyRead
        | GoAdsPropertyRead
    )
    if platform_type == GooglePlatformType.ga4:
        out_schema = GoAnalytics4PropertyRead.model_validate(go_property)
    elif platform_type == GooglePlatformType.ga4_stream:
        out_schema = GoAnalytics4StreamRead.model_validate(go_property)
    elif platform_type == GooglePlatformType.gsc:
        out_schema = GoSearchConsolePropertyRead.model_validate(go_property)
    elif platform_type == GooglePlatformType.gads:
        out_schema = GoAdsPropertyRead.model_validate(go_property)
    return out_schema


@router.patch(
    "/{platform_type}/{go_property_id}",
    name="go_property:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_go_property_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead,
)
async def go_property_update(
    platform_type: GooglePlatformType,
    go_property_in: GoAnalytics4PropertyUpdate
    | GoAnalytics4StreamUpdate
    | GoSearchConsolePropertyUpdate
    | GoAdsPropertyUpdate,
    go_property: GoAnalytics4Property
    | GoAnalytics4Stream
    | GoSearchConsoleProperty
    | GoAdsProperty = Permission(
        [AccessUpdate, AccessUpdateRelated, AccessUpdateSelf], get_go_property_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> (
    GoAnalytics4PropertyRead
    | GoAnalytics4StreamRead
    | GoSearchConsolePropertyRead
    | GoAdsPropertyRead
):
    """Update an existing google property: analytics, analytics stream, search concole, ads, etc.

    Permissions:
    ------------
    `role=admin|manager` : update new google properties for all clients

    `role=user` : update only google properties that belong to any clients
        associated with the current user

    Returns:
    --------
    `GoAnalytics4PropertyRead | GoAnalytics4StreamRead | GoSearchConsolePropertyRead | GoAdsPropertyRead` : the updated google property

    """
    update_go_property: (
        GoAnalytics4PropertyRead
        | GoAnalytics4StreamRead
        | GoSearchConsolePropertyRead
        | GoAdsPropertyRead
    ) = None
    if platform_type == GooglePlatformType.ga4:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoAnalytics4Property
        ):
            raise ValidationError(title="GoAnalytics4Property")
        go_property_in = GoAnalytics4PropertyUpdate.model_validate(go_property_in)
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=go_property.client_id,
        )
        ga4_repo = GoAnalytics4PropertyRepository(session=permissions.db)
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        a_title = await ga4_repo.read_by(field_name="title", field_value=check_title)
        if a_title is not None:
            raise EntityAlreadyExists(
                entity_info=f"GoAnalytics4property title = {go_property_in.title})"
            )
        if hasattr(go_property_in, "client_id"):
            client_repo: ClientRepository = ClientRepository(session=permissions.db)
            a_client: Client | None = await client_repo.read(
                entry_id=go_property_in.client_id
            )
            if a_client is None:
                raise ClientNotFound()
            await permissions.verify_user_can_access(
                privileges=[RoleAdmin, RoleManager],
                client_id=go_property_in.client_id,
            )
        update_ga4 = await ga4_repo.update(entry=go_property, schema=go_property_in)
        update_go_property = GoAnalytics4PropertyRead.model_validate(update_ga4)
    elif platform_type == GooglePlatformType.ga4_stream:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoAnalytics4Stream
        ):
            raise ValidationError(title="GoAnalytics4Stream")
        go_property_in = GoAnalytics4StreamUpdate.model_validate(go_property_in)
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_property.website_id,
        )
        ga4_stream_repo = GoAnalytics4StreamRepository(session=permissions.db)
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        a_title = await ga4_stream_repo.read_by(
            field_name="title", field_value=check_title
        )
        if a_title is not None:
            raise EntityAlreadyExists(
                entity_info=f"GoAnalytics4Stream title = {go_property_in.title})"
            )
        if hasattr(go_property_in, "website_id"):
            website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
            a_website: Website | None = await website_repo.read(
                entry_id=go_property_in.website_id
            )
            if a_website is None:
                raise EntityNotFound(
                    entity_info="Website id = {}".format(go_property_in.website_id)
                )
            await permissions.verify_user_can_access(
                privileges=[RoleAdmin, RoleManager],
                website_id=go_property_in.website_id,
            )
        update_ga4_stream = await ga4_stream_repo.update(
            entry=go_property, schema=go_property_in
        )
        update_go_property = GoAnalytics4StreamRead.model_validate(update_ga4_stream)
    elif platform_type == GooglePlatformType.gsc:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoSearchConsoleProperty
        ):
            raise ValidationError(title="GoSearchConsoleProperty")
        go_property_in = GoSearchConsolePropertyUpdate.model_validate(go_property_in)
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_property.website_id,
        )
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=go_property.client_id,
        )
        go_sc_repo = GoSearchConsolePropertyRepository(session=permissions.db)
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        check_client_id: UUID4 | None = data.get("client_id", None)
        check_website_id: UUID4 | None = data.get("website_id", None)
        a_title = await go_sc_repo.read_by(field_name="title", field_value=check_title)
        if a_title is not None:
            raise EntityAlreadyExists(
                entity_info=f"GoSearchConsoleProperty title = {go_property_in.title})"
            )
        if check_client_id is not None:
            client_repo: ClientRepository = ClientRepository(session=permissions.db)
            a_client: Client | None = await client_repo.read(entry_id=check_client_id)
            if a_client is None:
                raise ClientNotFound()
            await permissions.verify_user_can_access(
                privileges=[RoleAdmin, RoleManager],
                client_id=check_client_id,
            )
        if check_website_id is not None:
            website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
            a_website: Website | None = await website_repo.read(
                entry_id=check_website_id
            )
            if a_website is None:
                raise EntityNotFound(
                    entity_info="Website id = {}".format(check_website_id)
                )
            await permissions.verify_user_can_access(
                privileges=[RoleAdmin, RoleManager],
                website_id=go_property_in.website_id,
            )
        update_gsc = await go_sc_repo.update(entry=go_property, schema=go_property_in)
        update_go_property = GoSearchConsolePropertyRead.model_validate(update_gsc)
    elif platform_type == GooglePlatformType.gads:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoAdsProperty
        ):
            raise ValidationError(title="GoAdsProperty")
        go_property_in = GoAdsPropertyUpdate.model_validate(go_property_in)
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=go_property.client_id,
        )
        gads_repo = GoAdsPropertyRepository(session=permissions.db)
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        a_title = await gads_repo.read_by(field_name="title", field_value=check_title)
        if a_title is not None:
            raise EntityAlreadyExists(
                entity_info=f"GoAdsProperty title = {go_property_in.title})"
            )
        if hasattr(go_property_in, "client_id"):
            client_repo: ClientRepository = ClientRepository(session=permissions.db)
            a_client: Client | None = await client_repo.read(
                entry_id=go_property_in.client_id
            )
            if a_client is None:
                raise ClientNotFound()
            await permissions.verify_user_can_access(
                privileges=[RoleAdmin, RoleManager],
                client_id=go_property_in.client_id,
            )
        update_gads = await gads_repo.update(entry=go_property, schema=go_property_in)
        update_go_property = GoAdsPropertyRead.model_validate(update_gads)
    if update_go_property is None:  # pragma: no cover - safety check
        raise EntityNotFound(entity_info=f"Google Property {platform_type} not updated")
    return update_go_property


@router.delete(
    "/{platform_type}/{go_property_id}",
    name="go_property:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_go_property_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def go_property_delete(
    platform_type: GooglePlatformType,
    go_property: GoAnalytics4Property
    | GoAnalytics4Stream
    | GoSearchConsoleProperty
    | GoAdsProperty = Permission([AccessDelete], get_go_property_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Deletes a single google property account by platform_type and id.

    Permissions:
    ------------
    `role=admin|manager` : delete all google properties

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    if platform_type == GooglePlatformType.ga4:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoAnalytics4Property
        ):
            raise ValidationError(title="GoAnalytics4Property")
        ga4_repo = GoAnalytics4PropertyRepository(session=permissions.db)
        await ga4_repo.delete(entry=go_property)
    elif platform_type == GooglePlatformType.ga4_stream:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoAnalytics4Stream
        ):
            raise ValidationError(title="GoAnalytics4Stream")
        ga4_stream_repo = GoAnalytics4StreamRepository(session=permissions.db)
        await ga4_stream_repo.delete(entry=go_property)
    elif platform_type == GooglePlatformType.gsc:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoSearchConsoleProperty
        ):
            raise ValidationError(title="GoAnalytics4Stream")
        gsc_repo = GoSearchConsolePropertyRepository(session=permissions.db)
        await gsc_repo.delete(entry=go_property)
    elif platform_type == GooglePlatformType.gads:
        if not isinstance(  # pragma: no cover - safety check
            go_property, GoAdsProperty
        ):
            raise ValidationError(title="GoAnalytics4Stream")
        gads_repo = GoAdsPropertyRepository(session=permissions.db)
        await gads_repo.delete(entry=go_property)
    return None

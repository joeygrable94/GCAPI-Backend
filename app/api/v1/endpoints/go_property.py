from fastapi import APIRouter, Depends
from httpx import Client

from app.api.deps import (
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
)
from app.api.deps.get_db_items import get_go_property_or_404
from app.api.exceptions.exceptions import (
    ClientNotFound,
    EntityAlreadyExists,
    EntityNotFound,
)
from app.core.security.permissions import (
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.crud.client import ClientRepository
from app.crud.go_a4 import GoAnalytics4PropertyRepository
from app.crud.go_a4_stream import GoAnalytics4StreamRepository
from app.crud.go_ads import GoAdsPropertyRepository
from app.crud.go_sc import GoSearchConsolePropertyRepository
from app.crud.platform import PlatformRepository
from app.crud.website import WebsiteRepository
from app.models.go_a4 import GoAnalytics4Property
from app.models.go_a4_stream import GoAnalytics4Stream
from app.models.go_ads import GoAdsProperty
from app.models.go_sc import GoSearchConsoleProperty
from app.models.website import Website
from app.schemas.go import GooglePlatformType
from app.schemas.go_a4 import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    RequestGoAnalytics4PropertyCreate,
)
from app.schemas.go_a4_stream import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
    RequestGoAnalytics4StreamCreate,
)
from app.schemas.go_ads import (
    GoAdsPropertyCreate,
    GoAdsPropertyRead,
    RequestGoAdsPropertyCreate,
)
from app.schemas.go_sc import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
    RequestGoSearchConsolePropertyCreate,
)

router: APIRouter = APIRouter()


@router.post(
    "/{patform_type}",
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
    | GoSearchConsolePropertyRead
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
    `GoAnalytics4PropertyRead | GoSearchConsolePropertyRead | GoAdsPropertyRead` : the newly created google property

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
        if not isinstance(go_property_in, RequestGoAnalytics4PropertyCreate):
            raise ValueError(
                "Invalid schema for creating a new Google Analytics 4 property"
            )
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="ga4")
        if a_platform is None:
            raise EntityNotFound(entity_info="Platform slug = ga4")
        data = go_property_in.model_dump()
        check_title: str = data.get("title", "")
        check_measurement_id: str = data.get("measurement_id", "")
        check_property_id: str = data.get("property_id", "")
        ga4_repo = GoAnalytics4PropertyRepository(session=permissions.db)
        a_ga4_title = await ga4_repo.read_by(
            field_name="title", field_value=check_title
        )
        a_ga4_measurement_id = await ga4_repo.read_by(
            field_name="measurement_id", field_value=check_measurement_id
        )
        a_ga4_property_id = await ga4_repo.read_by(
            field_name="property_id", field_value=check_property_id
        )
        if (
            a_ga4_measurement_id is not None
            or a_ga4_title is not None
            or a_ga4_property_id is not None
        ):
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
        if not isinstance(go_property_in, RequestGoAnalytics4StreamCreate):
            raise ValueError(
                "Invalid schema for creating a new Google Analytics 4 Stream property"
            )
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="ga4")
        if a_platform is None:
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
        new_ga4_stream = await ga4_repo.create(
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
        if not isinstance(go_property_in, RequestGoSearchConsolePropertyCreate):
            raise ValueError(
                "Invalid schema for creating a new Google Search Console property"
            )
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_property_in.website_id,
        )
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="gsc")
        if a_platform is None:
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
        if not isinstance(go_property_in, RequestGoAdsPropertyCreate):
            raise ValueError("Invalid schema for creating a new Google Ads property")
        platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
        a_platform = await platform_repo.read_by(field_name="slug", field_value="gads")
        if a_platform is None:
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

    if new_go_property is None:
        raise EntityNotFound(entity_info=f"Google Property {platform_type} not created")

    return new_go_property


@router.get(
    "/{patform_type}/{go_property_id}",
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
        [AccessRead, AccessReadSelf, AccessReadRelated], get_go_property_or_404
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
    `PlatformRead` : the platform account matching the platform_id

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        platform_id=go_property.platform_id,
    )
    if platform_type == GooglePlatformType.ga4:
        response_out: GoAnalytics4Property = permissions.get_resource_response(
            resource=go_property,
            responses={
                RoleUser: GoAnalytics4PropertyRead,
            },
        )
        return response_out
    if platform_type == GooglePlatformType.ga4_stream:
        response_out: GoAnalytics4Stream = permissions.get_resource_response(
            resource=go_property,
            responses={
                RoleUser: GoAnalytics4StreamRead,
            },
        )
        return response_out
    if platform_type == GooglePlatformType.gsc:
        response_out: GoSearchConsoleProperty = permissions.get_resource_response(
            resource=go_property,
            responses={
                RoleUser: GoSearchConsolePropertyRead,
            },
        )
        return response_out
    if platform_type == GooglePlatformType.gads:
        response_out: GoAdsProperty = permissions.get_resource_response(
            resource=go_property,
            responses={
                RoleUser: GoAdsPropertyRead,
            },
        )
        return response_out
    raise EntityNotFound(
        entity_info="Google Property {} not found id {}".format(
            platform_type, go_property.id
        )
    )

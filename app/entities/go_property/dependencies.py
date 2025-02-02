from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.go_ga4.crud import (
    GoAnalytics4Property,
    GoAnalytics4PropertyRepository,
)
from app.entities.go_ga4_stream.crud import GoAnalytics4StreamRepository
from app.entities.go_ga4_stream.model import GoAnalytics4Stream
from app.entities.go_gads.crud import GoAdsPropertyRepository
from app.entities.go_gads.model import GoAdsProperty
from app.entities.go_gsc.crud import (
    GoSearchConsoleProperty,
    GoSearchConsolePropertyRepository,
)
from app.entities.go_property.schemas import GooglePlatformType
from app.utilities import parse_id


async def get_go_property_or_404(
    db: AsyncDatabaseSession,
    platform_type: GooglePlatformType,
    go_property_id: Any,
) -> (
    GoAnalytics4Property | GoAnalytics4Stream | GoSearchConsoleProperty | GoAdsProperty
):
    """Parses uuid/int and fetches go property by platform_type and id."""
    parsed_id: UUID = parse_id(go_property_id)
    if platform_type == GooglePlatformType.ga4:
        ga4_repo = GoAnalytics4PropertyRepository(session=db)
        ga4_property: GoAnalytics4Property | None = await ga4_repo.read(parsed_id)
        if ga4_property is None:
            raise EntityNotFound(
                entity_info="GoAnalytics4Property id = {}".format(parsed_id)
            )
        return ga4_property
    elif platform_type == GooglePlatformType.ga4_stream:
        ga4_stream_repo = GoAnalytics4StreamRepository(session=db)
        ga4_stream: GoAnalytics4Stream | None = await ga4_stream_repo.read(parsed_id)
        if ga4_stream is None:
            raise EntityNotFound(
                entity_info="GoAnalytics4Stream id = {}".format(parsed_id)
            )
        return ga4_stream
    elif platform_type == GooglePlatformType.gsc:
        gsc_repo = GoSearchConsolePropertyRepository(session=db)
        gsc_property: GoSearchConsoleProperty | None = await gsc_repo.read(parsed_id)
        if gsc_property is None:
            raise EntityNotFound(
                entity_info="GoSearchConsoleProperty id = {}".format(parsed_id)
            )
        return gsc_property
    elif platform_type == GooglePlatformType.gads:
        gads_repo = GoAdsPropertyRepository(session=db)
        gads_property: GoAdsProperty | None = await gads_repo.read(parsed_id)
        if gads_property is None:
            raise EntityNotFound(entity_info="GoAdsProperty = {}".format(parsed_id))
        return gads_property
    raise EntityNotFound(  # pragma: no cover - safety net fallback
        entity_info="GoogleProperty type = {}, id = {}".format(platform_type, parsed_id)
    )


FetchGooglePropertyOr404 = Annotated[
    GoAnalytics4Property | GoAnalytics4Stream | GoSearchConsoleProperty | GoAdsProperty,
    Depends(get_go_property_or_404),
]

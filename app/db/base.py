# Import all the models, so that Base has them before import by Alembic
from app.db.base_class import Base  # noqa: F401
from app.models.client import Client  # noqa: F401
from app.models.client_website import ClientWebsite  # noqa: F401
from app.models.gcft import GCFT  # noqa: F401
from app.models.gcft_snap import GCFTSnap  # noqa: F401
from app.models.gcft_snap_activeduration import GCFTSnapActiveDuration  # noqa: F401
from app.models.gcft_snap_browserreport import GCFTSnapBrowserReport  # noqa: F401
from app.models.gcft_snap_hotspotclick import GCFTSnapHotspotClick  # noqa: F401
from app.models.gcft_snap_trafficsource import GCFTSnapTrafficSource  # noqa: F401
from app.models.gcft_snap_view import GCFTSnapView  # noqa: F401
from app.models.geocoord import GeoCoord  # noqa: F401
from app.models.go_a4 import GoogleAnalytics4Property  # noqa: F401
from app.models.go_a4_stream import GoogleAnalytics4Stream  # noqa: F401
from app.models.go_cloud import GoogleCloudProperty  # noqa: F401
from app.models.go_sc import GoogleSearchConsoleProperty  # noqa: F401
from app.models.go_sc_country import GoogleSearchConsoleCountry  # noqa: F401
from app.models.go_sc_device import GoogleSearchConsoleDevice  # noqa: F401
from app.models.go_sc_page import GoogleSearchConsolePage  # noqa: F401
from app.models.go_sc_query import GoogleSearchConsoleQuery  # noqa: F401
from app.models.go_sc_searchappearance import (  # noqa: F401
    GoogleSearchConsoleSearchAppearance,
)
from app.models.go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401
from app.models.go_ua_view import GoogleUniversalAnalyticsView  # noqa: F401
from app.models.imageupload import ImageUpload  # noqa: F401
from app.models.note import Note  # noqa: F401
from app.models.sharpspring import SharpSpring  # noqa: F401
from app.models.website import Website  # noqa: F401
from app.models.website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
from app.models.website_map import WebsiteMap  # noqa: F401
from app.models.website_page import WebsitePage  # noqa: F401
from app.models.website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401

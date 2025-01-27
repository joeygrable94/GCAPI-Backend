from .client import ClientRepository
from .client_platform import ClientPlatformRepository
from .client_styleguide import ClientStyleguideRepository
from .client_website import ClientWebsiteRepository
from .gcft import GcftRepository
from .gcft_snap import GcftSnapRepository
from .gcft_snap_activeduration import GcftSnapActivedurationRepository
from .gcft_snap_browserreport import GcftSnapBrowserreportRepository
from .gcft_snap_hotspotclick import GcftSnapHotspotclickRepository
from .gcft_snap_trafficsource import GcftSnapTrafficsourceRepository
from .gcft_snap_view import GcftSnapViewRepository
from .geocoord import GeocoordRepository
from .go_a4 import GoAnalytics4PropertyRepository
from .go_a4_stream import GoAnalytics4StreamRepository
from .go_ads import GoAdsPropertyRepository
from .go_sc import GoSearchConsolePropertyRepository
from .ipaddress import IpaddressRepository
from .platform import PlatformRepository
from .tracking_link import TrackingLinkRepository
from .user import UserRepository
from .user_client import UserClientRepository
from .user_ipaddress import UserIpaddressRepository
from .website import WebsiteRepository
from .website_go_a4 import WebsiteGoAnalytics4PropertyRepository
from .website_keywordcorpus import WebsiteKeywordCorpusRepository
from .website_map import WebsiteMapRepository
from .website_page import WebsitePageRepository
from .website_pagespeedinsights import WebsitePageSpeedInsightsRepository

__all__: list[str] = [
    "ClientRepository",
    "ClientStyleguideRepository",
    "ClientPlatformRepository",
    "ClientWebsiteRepository",
    "GcftRepository",
    "GcftSnapRepository",
    "GcftSnapActivedurationRepository",
    "GcftSnapBrowserreportRepository",
    "GcftSnapHotspotclickRepository",
    "GcftSnapTrafficsourceRepository",
    "GcftSnapViewRepository",
    "GeocoordRepository",
    "GoAdsPropertyRepository",
    "GoAnalytics4PropertyRepository",
    "GoAnalytics4StreamRepository",
    "GoSearchConsolePropertyRepository",
    "IpaddressRepository",
    "PlatformRepository",
    "TrackingLinkRepository",
    "UserRepository",
    "UserClientRepository",
    "UserIpaddressRepository",
    "WebsiteRepository",
    "WebsiteKeywordCorpusRepository",
    "WebsiteMapRepository",
    "WebsitePageRepository",
    "WebsitePageSpeedInsightsRepository",
    "WebsiteGoAnalytics4PropertyRepository",
]

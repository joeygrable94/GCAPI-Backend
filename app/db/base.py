from app.db.base_class import Base
from app.models.client import Client
from app.models.client_platform import ClientPlatform
from app.models.client_styleguide import ClientStyleguide
from app.models.client_website import ClientWebsite
from app.models.gcft import Gcft
from app.models.gcft_snap import GcftSnap
from app.models.gcft_snap_activeduration import GcftSnapActiveduration
from app.models.gcft_snap_browserreport import GcftSnapBrowserreport
from app.models.gcft_snap_hotspotclick import GcftSnapHotspotclick
from app.models.gcft_snap_trafficsource import GcftSnapTrafficsource
from app.models.gcft_snap_view import GcftSnapView
from app.models.geocoord import Geocoord
from app.models.go_a4 import GoAnalytics4Property
from app.models.go_a4_stream import GoAnalytics4Stream
from app.models.go_ads import GoAdsProperty
from app.models.go_sc import GoSearchConsoleProperty
from app.models.ipaddress import Ipaddress
from app.models.platform import Platform
from app.models.tracking_link import TrackingLink
from app.models.user import User
from app.models.user_client import UserClient
from app.models.user_ipaddress import UserIpaddress
from app.models.website import Website
from app.models.website_go_a4 import WebsiteGoAnalytics4Property
from app.models.website_go_ads import WebsiteGoAdsProperty
from app.models.website_keywordcorpus import WebsiteKeywordCorpus
from app.models.website_map import WebsiteMap
from app.models.website_page import WebsitePage
from app.models.website_pagespeedinsights import WebsitePageSpeedInsights

__all__: list[str] = [
    "Base",
    "Client",
    "ClientWebsite",
    "ClientPlatform",
    "ClientStyleguide",
    "Gcft",
    "GcftSnap",
    "GcftSnapActiveduration",
    "GcftSnapBrowserreport",
    "GcftSnapHotspotclick",
    "GcftSnapTrafficsource",
    "GcftSnapView",
    "Geocoord",
    "GoAdsProperty",
    "GoAnalytics4Property",
    "GoAnalytics4Stream",
    "GoSearchConsoleProperty",
    "Ipaddress",
    "TrackingLink",
    "Platform",
    "User",
    "UserClient",
    "UserIpaddress",
    "Website",
    "WebsiteKeywordCorpus",
    "WebsiteMap",
    "WebsitePage",
    "WebsitePageSpeedInsights",
    "WebsiteGoAnalytics4Property",
    "WebsiteGoAdsProperty",
]

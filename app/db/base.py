from app.db.base_class import Base
from app.entities.client.model import Client
from app.entities.client_platform.model import ClientPlatform
from app.entities.client_styleguide.model import ClientStyleguide
from app.entities.client_website.model import ClientWebsite
from app.entities.gcft.model import Gcft
from app.entities.gcft_snap.model import GcftSnap
from app.entities.gcft_snap_active_duration.model import GcftSnapActiveduration
from app.entities.gcft_snap_browser_report.model import GcftSnapBrowserreport
from app.entities.gcft_snap_hotspot_click.model import GcftSnapHotspotclick
from app.entities.gcft_snap_traffic_source.model import GcftSnapTrafficsource
from app.entities.gcft_snap_view.model import GcftSnapView
from app.entities.geocoord.model import Geocoord
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4_stream.model import GoAnalytics4Stream
from app.entities.go_gads.model import GoAdsProperty
from app.entities.go_gsc.model import GoSearchConsoleProperty
from app.entities.ipaddress.model import Ipaddress
from app.entities.platform.model import Platform
from app.entities.tracking_link.model import TrackingLink
from app.entities.user.model import User
from app.entities.user_client.model import UserClient
from app.entities.user_ipaddress.model import UserIpaddress
from app.entities.website.model import Website
from app.entities.website_go_ga4.model import WebsiteGoAnalytics4Property
from app.entities.website_go_gads.model import WebsiteGoAdsProperty
from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus
from app.entities.website_page.model import WebsitePage
from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights

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
    "WebsitePage",
    "WebsitePageSpeedInsights",
    "WebsiteGoAnalytics4Property",
    "WebsiteGoAdsProperty",
]

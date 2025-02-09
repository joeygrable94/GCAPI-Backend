from app.db.base_class import Base
from app.entities.core_audit_log.model import AuditLog
from app.entities.core_geocoord.model import Geocoord
from app.entities.core_ipaddress.model import Ipaddress
from app.entities.core_ipaddress_geocoord.model import IpaddressGeocoord
from app.entities.core_organization.model import Organization
from app.entities.core_permission.model import Permission
from app.entities.core_role.model import Role
from app.entities.core_role_permission.model import RolePermission
from app.entities.core_user.model import User
from app.entities.core_user_ipaddress.model import UserIpaddress
from app.entities.core_user_organization.model import UserOrganization
from app.entities.core_user_organization_role.model import UserOrganizationRole
from app.entities.core_user_permission.model import UserPermission
from app.entities.core_user_role.model import UserRole
from app.entities.gcft.model import Gcft
from app.entities.gcft_snap.model import GcftSnap
from app.entities.gcft_snap_active_duration.model import GcftSnapActiveduration
from app.entities.gcft_snap_browser_report.model import GcftSnapBrowserreport
from app.entities.gcft_snap_hotspot_click.model import GcftSnapHotspotclick
from app.entities.gcft_snap_traffic_source.model import GcftSnapTrafficsource
from app.entities.gcft_snap_view.model import GcftSnapView
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4_stream.model import GoAnalytics4Stream
from app.entities.go_gads.model import GoAdsProperty
from app.entities.go_gsc.model import GoSearchConsoleProperty
from app.entities.organization_platform.model import OrganizationPlatform
from app.entities.organization_styleguide.model import OrganizationStyleguide
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.platform.model import Platform
from app.entities.tracking_link.model import TrackingLink
from app.entities.website.model import Website
from app.entities.website_go_ga4.model import WebsiteGoAnalytics4Property
from app.entities.website_go_gads.model import WebsiteGoAdsProperty
from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus
from app.entities.website_page.model import WebsitePage
from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights

__all__: list[str] = [
    "Base",
    "Organization",
    "OrganizationWebsite",
    "OrganizationPlatform",
    "OrganizationStyleguide",
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
    "UserOrganization",
    "UserIpaddress",
    "AuditLog",
    "IpaddressGeocoord",
    "Permission",
    "Role",
    "RolePermission",
    "UserOrganizationRole",
    "UserPermission",
    "UserRole",
    "Website",
    "WebsiteKeywordCorpus",
    "WebsitePage",
    "WebsitePageSpeedInsights",
    "WebsiteGoAnalytics4Property",
    "WebsiteGoAdsProperty",
]

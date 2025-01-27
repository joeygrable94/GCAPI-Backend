from enum import Enum


# schemas
class GooglePlatformType(Enum):
    ga4 = "analytics"
    ga4_stream = "analytics_stream"
    gsc = "search_console"
    gads = "ads"

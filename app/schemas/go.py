from enum import Enum


class GooglePlatformType(str, Enum):
    ga4 = "ga4"
    ga4_stream = "ga4_stream"
    gsc = "gsc"
    gads = "gads"

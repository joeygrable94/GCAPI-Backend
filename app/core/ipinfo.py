import ipinfo

from app.core.config import settings

ipinfo_handler = ipinfo.getHandler(settings.cloud.ipinfo)

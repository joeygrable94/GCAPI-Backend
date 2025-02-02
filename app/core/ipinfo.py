import ipinfo

from app.config import settings

ipinfo_handler = ipinfo.getHandler(settings.cloud.ipinfo)

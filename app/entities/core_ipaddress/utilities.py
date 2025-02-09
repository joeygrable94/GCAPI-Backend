from ipinfo.details import Details
from pydantic.networks import IPvAnyAddress

from app.core.ipinfo import ipinfo_handler
from app.entities.core_ipaddress.schemas import IpinfoResponse


def get_ipinfo_details(ip_address: IPvAnyAddress) -> IpinfoResponse:
    ip_data: Details = ipinfo_handler.getDetails(ip_address)
    ip_datails: dict = ip_data.details
    country_flag_unicode_value: dict = ip_datails.get(
        "country_flag", dict(unicode=None)
    )
    country_currency_code_value: dict = ip_datails.get(
        "country_currency", dict(code=None)
    )
    continent_code_value: dict = ip_datails.get("continent", dict(code=None))
    continent_name_value: dict = ip_datails.get("continent", dict(name=None))
    return IpinfoResponse(
        address=ip_datails.get("ip", "127.0.0.1"),
        hostname=ip_datails.get("hostname", None),
        is_anycast=ip_datails.get("anycast", None),
        city=ip_datails.get("city", None),
        region=ip_datails.get("region", None),
        country=ip_datails.get("country", None),
        loc=ip_datails.get("loc", None),
        org=ip_datails.get("org", None),
        postal=ip_datails.get("postal", None),
        timezone=ip_datails.get("timezone", None),
        country_name=ip_datails.get("country_name", None),
        is_eu=ip_datails.get("isEU", None) or False,
        country_flag_url=ip_datails.get("country_flag_url", None),
        country_flag_unicode=country_flag_unicode_value.get("unicode", None),
        country_currency_code=country_currency_code_value.get("code", None),
        continent_code=continent_code_value.get("code", None),
        continent_name=continent_name_value.get("name", None),
        latitude=ip_datails.get("latitude", None),
        longitude=ip_datails.get("longitude", None),
    )

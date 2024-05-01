from typing import Any, Dict

from app.schemas import IpinfoResponse


def get_ipinfo_response(data: Dict[str, Any]) -> IpinfoResponse:  # pragma: no cover
    country_flag_unicode_value: dict = data.get("country_flag", dict(unicode=None))
    country_currency_code_value: dict = data.get("country_currency", dict(code=None))
    continent_code_value: dict = data.get("continent", dict(code=None))
    continent_name_value: dict = data.get("continent", dict(name=None))
    return IpinfoResponse(
        address=data.get("ip", "127.0.0.1"),
        hostname=data.get("hostname", None),
        is_anycast=data.get("anycast", None),
        city=data.get("city", None),
        region=data.get("region", None),
        country=data.get("country", None),
        loc=data.get("loc", None),
        org=data.get("org", None),
        postal=data.get("postal", None),
        timezone=data.get("timezone", None),
        country_name=data.get("country_name", None),
        is_eu=data.get("isEU", None) or False,
        country_flag_url=data.get("country_flag_url", None),
        country_flag_unicode=country_flag_unicode_value.get("unicode", None),
        country_currency_code=country_currency_code_value.get("code", None),
        continent_code=continent_code_value.get("code", None),
        continent_name=continent_name_value.get("name", None),
        latitude=data.get("latitude", None),
        longitude=data.get("longitude", None),
    )

from pydantic import UUID4, field_validator
from pydantic.networks import IPvAnyAddress
from pydantic_extra_types.country import CountryAlpha2

from app.db.validators import (
    validate_ip_address_optional,
    validate_ip_address_required,
    validate_ip_city_optional,
    validate_ip_continent_code_optional,
    validate_ip_continent_name_optional,
    validate_ip_country_currency_code_optional,
    validate_ip_country_flag_unicode_optional,
    validate_ip_country_flag_url_optional,
    validate_ip_country_name_optional,
    validate_ip_country_optional,
    validate_ip_hostname_optional,
    validate_ip_latitude_optional,
    validate_ip_loc_optional,
    validate_ip_longitude_optional,
    validate_ip_org_optional,
    validate_ip_postal_optional,
    validate_ip_region_optional,
    validate_ip_timezone_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# ipinfo.io
class IpinfoResponse(BaseSchema):
    # '8.8.8.8'
    address: IPvAnyAddress
    # 'dns.google'
    hostname: str | None
    # True
    is_anycast: bool | None
    # 'Mountain View'
    city: str | None
    # 'California'
    region: str | None
    # 'US'
    country: CountryAlpha2 | None
    # '37.4056,-122.0775'
    loc: str | None
    # 'AS15169 Google LLC'
    org: str | None
    # '94043'
    postal: str | None
    # 'America/Los_Angeles'
    timezone: str | None
    # 'United States'
    country_name: str | None
    # False
    is_eu: bool | None
    # 'https://cdn.ipinfo.io/static/images/countries-flags/US.svg'
    country_flag_url: str | None
    # country_flag: { 'emoji': '🇺🇸', 'unicode': 'U+1F1FA U+1F1F8' }
    country_flag_unicode: str | None
    # country_currency: { 'code': 'USD', 'symbol': '$' }
    country_currency_code: str | None
    # continent: { 'code': 'NA', 'North America'}
    continent_code: str | None
    # continent: { 'code': 'NA', 'North America'}
    continent_name: str | None
    # '37.4056'
    latitude: str | None
    # '-122.0775'
    longitude: str | None


# schemas
class IpaddressBase(BaseSchema):
    hostname: str | None = None
    is_anycast: bool | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    loc: str | None = None
    org: str | None = None
    postal: str | None = None
    timezone: str | None = None
    country_name: str | None = None
    is_eu: bool | None = None
    country_flag_url: str | None = None
    country_flag_unicode: str | None = None
    country_currency_code: str | None = None
    continent_code: str | None = None
    continent_name: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    # relationships
    geocoord_id: UUID4 | None = None

    _validate_hostname = field_validator("hostname", mode="before")(
        validate_ip_hostname_optional
    )
    _validate_city = field_validator("city", mode="before")(validate_ip_city_optional)
    _validate_region = field_validator("region", mode="before")(
        validate_ip_region_optional
    )
    _validate_country = field_validator("country", mode="before")(
        validate_ip_country_optional
    )
    _validate_loc = field_validator("loc", mode="before")(validate_ip_loc_optional)
    _validate_org = field_validator("org", mode="before")(validate_ip_org_optional)
    _validate_postal = field_validator("postal", mode="before")(
        validate_ip_postal_optional
    )
    _validate_timezone = field_validator("timezone", mode="before")(
        validate_ip_timezone_optional
    )
    _validate_country_name = field_validator("country_name", mode="before")(
        validate_ip_country_name_optional
    )
    _validate_country_flag_url = field_validator("country_flag_url", mode="before")(
        validate_ip_country_flag_url_optional
    )
    _validate_country_flag_unicode = field_validator(
        "country_flag_unicode", mode="before"
    )(validate_ip_country_flag_unicode_optional)
    _validate_country_currency_code = field_validator(
        "country_currency_code", mode="before"
    )(validate_ip_country_currency_code_optional)
    _validate_continent_code = field_validator("continent_code", mode="before")(
        validate_ip_continent_code_optional
    )
    _validate_continent_name = field_validator("continent_name", mode="before")(
        validate_ip_continent_name_optional
    )
    _validate_latitude = field_validator("latitude", mode="before")(
        validate_ip_latitude_optional
    )
    _validate_longitude = field_validator("longitude", mode="before")(
        validate_ip_longitude_optional
    )


class IpaddressCreate(IpaddressBase):
    address: str

    _validate_address = field_validator("address", mode="before")(
        validate_ip_address_required
    )


class IpaddressUpdate(IpaddressBase):
    address: str | None = None

    _validate_address = field_validator("address", mode="before")(
        validate_ip_address_optional
    )


class IpaddressRead(IpaddressBase, BaseSchemaRead):
    id: UUID4
    address: IPvAnyAddress

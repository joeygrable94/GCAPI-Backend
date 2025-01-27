from .dates_and_time import get_date, get_datetime_from_int, get_int_from_datetime
from .paginate import paginate
from .regex import (
    domain_in_url_regex,
    domain_name_regex,
    email_regex,
    pw_req_regex,
    scope_regex,
    utm_parameter_value_regex,
)
from .uuids import get_random_username, get_uuid, get_uuid_str, parse_id
from .websites import (
    check_is_sitemap_index,
    check_is_sitemap_page,
    check_is_sitemap_urlset,
    check_is_xml_valid_sitemap,
    fetch_url_page_text,
    fetch_url_status_code,
    parse_sitemap_xml,
    process_sitemap_index,
    process_sitemap_page_urlset,
    process_sitemap_website_page,
)

__all__: list[str] = [
    "get_date",
    "get_datetime_from_int",
    "get_int_from_datetime",
    "get_random_username",
    "paginate",
    "domain_in_url_regex",
    "domain_name_regex",
    "utm_parameter_value_regex",
    "email_regex",
    "pw_req_regex",
    "scope_regex",
    "get_uuid",
    "get_uuid_str",
    "parse_id",
    "fetch_url_status_code",
    "fetch_url_page_text",
    "parse_sitemap_xml",
    "check_is_xml_valid_sitemap",
    "check_is_sitemap_index",
    "check_is_sitemap_page",
    "check_is_sitemap_urlset",
    "process_sitemap_index",
    "process_sitemap_page_urlset",
    "process_sitemap_website_page",
]

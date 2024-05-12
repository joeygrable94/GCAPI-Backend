from .core_tasks import (
    task_request_to_delete_client,
    task_request_to_delete_user,
    task_speak,
)
from .data_buckets import task_create_client_data_bucket
from .user_tasks import task_fetch_ipinfo
from .website_tasks import (
    task_website_page_pagespeedinsights_fetch,
    task_website_sitemap_process_xml,
)

__all__: list[str] = [
    "task_speak",
    "task_fetch_ipinfo",
    "task_request_to_delete_user",
    "task_request_to_delete_client",
    "task_create_client_data_bucket",
    "task_website_sitemap_process_xml",
    "task_website_page_pagespeedinsights_fetch",
]

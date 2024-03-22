from .core_tasks import (
    task_request_to_delete_client,
    task_request_to_delete_user,
    task_speak,
)
from .website_tasks import (
    task_website_page_pagespeedinsights_fetch,
    task_website_sitemap_fetch_pages,
)

__all__: list[str] = [
    "task_speak",
    "task_request_to_delete_user",
    "task_request_to_delete_client",
    "task_website_sitemap_fetch_pages",
    "task_website_page_pagespeedinsights_fetch",
]

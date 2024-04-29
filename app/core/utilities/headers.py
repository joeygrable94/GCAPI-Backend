from typing import Dict

from asgi_correlation_id.context import correlation_id


def get_global_headers(inject_headers: Dict[str, str] | None = None) -> Dict[str, str]:
    global_headers = {
        "x-request-id": correlation_id.get() or "",
        "Access-Control-Expose-Headers": "x-request-id",
    }
    if inject_headers is not None:
        global_headers.update(inject_headers)
    return global_headers

class ApiException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def get_global_headers(inject_headers: dict[str, str] | None = None) -> dict[str, str]:
    global_headers = {
        "Access-Control-Expose-Headers": "x-request-id",
    }
    if inject_headers is not None:
        global_headers.update(inject_headers)  # pragma: no cover
    return global_headers

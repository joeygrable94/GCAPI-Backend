from fastapi import Request


def get_request_client_ip(request: Request) -> str:
    forwarded_ip = request.headers.get("X-Forwarded-For")
    if forwarded_ip:
        return forwarded_ip.split(",")[0]
    elif request.client is not None:
        return request.client.host
    return "::0"  # pragma: no cover

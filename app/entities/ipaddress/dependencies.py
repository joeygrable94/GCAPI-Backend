from typing import Annotated

from fastapi import Depends, Request


def get_request_ip(request: Request) -> str:
    forwarded_ip = request.headers.get("X-Forwarded-For")
    if forwarded_ip:
        return forwarded_ip.split(",")[0]
    elif request.client is not None:
        return request.client.host
    return "127.0.0.1"  # pragma: no cover


RequestClientIp = Annotated[str, Depends(get_request_ip)]

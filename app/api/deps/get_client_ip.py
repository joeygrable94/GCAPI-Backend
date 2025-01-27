from ipaddress import IPv4Address
from typing import Annotated

from fastapi import Depends, Request
from pydantic import IPvAnyAddress


def get_request_client_ip(request: Request) -> IPv4Address:
    forwarded_ip = request.headers.get("X-Forwarded-For")
    if forwarded_ip:
        return IPv4Address(address=forwarded_ip.split(",")[0])
    elif request.client is not None:
        return IPv4Address(request.client.host)
    return IPv4Address("127.0.0.1")  # pragma: no cover


RequestClientIp = Annotated[IPvAnyAddress, Depends(get_request_client_ip)]

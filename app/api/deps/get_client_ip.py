from fastapi import Request


def get_request_client_ip(request: Request) -> str:
    client_ip: str
    forwarded_ip = request.headers.get("X-Forwarded-For")
    if forwarded_ip:
        client_ip = forwarded_ip.split(",")[0]
    elif request.client:
        client_ip = request.client.host
    else:
        client_ip = "::0"
    return client_ip

from fastapi import FastAPI
from fastapi.routing import APIRoute


def make_routes_map(app: FastAPI) -> None:
    endpoints = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoints.append(route.path)
    with open("docs/endpoints.txt", "w") as f:
        f.write("\n".join(endpoints))

from fastapi import FastAPI

from .system import router_system
from .v1 import router_v1

ROUTERS = (router_system, router_v1,)


def register_routers(app: FastAPI) -> None:
    for router in ROUTERS:
        app.include_router(router)

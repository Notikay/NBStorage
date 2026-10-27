from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from infrastructure.bootstrap.dependencies import init_container
from infrastructure.config import configure_logging
from infrastructure.config.settings import load_settings

from .core.exception_handlers import register_exception_handlers
from .core.lifespan import lifespan
from .core.middlewares import register_middlewares
from .routers.register import register_routers


def create_app() -> FastAPI:
    settings = load_settings()
    configure_logging(settings.environment, settings.debug)

    app = FastAPI(
        title=settings.api.title,
        summary=settings.api.summary,
        description=settings.api.description,
        version=settings.api.version,
        openapi_url=settings.api.openapi_url,
        docs_url=settings.api.docs_url,
        redoc_url=settings.api.redoc_url,
        lifespan=lifespan,
    )

    register_middlewares(app, settings)
    register_exception_handlers(app)
    register_routers(app)

    container = init_container(settings)
    setup_dishka(container, app)

    return app

# TODO: Rate-limiter
# TODO: Кеширование через Redis
# TODO: Переход на асинхронный код
# TODO: Nginx

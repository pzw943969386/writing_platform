from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from loguru import logger
from .datebase.sqlite import sqlite_service
from .api.tools import tools_router
from .api.article import article_router
from .api.write import write_router


def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            await sqlite_service.create_table()
            logger.info("应用程序启动")
            yield
        finally:
            logger.info("应用程序关闭")

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(article_router, prefix="/article")
    app.include_router(tools_router, prefix="/tools")
    app.include_router(write_router, prefix="/write")

    @app.get("/openapi.json", include_in_schema=False)
    async def custom_openapi():
        """自定义OpenAPI JSON路径"""
        if app.openapi_schema:
            return app.openapi_schema
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        return app.openapi_schema

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        """自定义Swagger UI文档页面"""
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=app.title + " - Swagger UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        )

    return app


app = create_app()

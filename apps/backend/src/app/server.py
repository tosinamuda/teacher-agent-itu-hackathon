"""The HTTP application: its routes, the frontend's origins, static files, and error mapping."""

from __future__ import annotations

import os

# The whole ORM model graph loads here, before any router imports a domain: loading the
# experiments and artefacts packages in the other order trips a circular import between them.
import app.db.metadata  # noqa: F401  # isort: skip

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.cors import build_cors_origin_regex
from app.domains.content.infrastructure.wiring import build_content_mcp_server
from app.domains.content_engine.mcp.server import http_route
from app.dspy_setup import configure_dspy
from app.lifespan import lifespan
from app.router import api_router
from app.shared.concluded import ConcludedLessonError

MCP_PATH = "/mcp"


def create_app() -> FastAPI:
    configure_dspy()
    app = FastAPI(title="Backend API", version="0.1.0", lifespan=lifespan)
    _allow_the_frontend(app)
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.add_exception_handler(ConcludedLessonError, _concluded_lesson)
    app.include_router(api_router)
    _serve_the_content_engine(app)
    return app


def _serve_the_content_engine(app: FastAPI) -> None:
    """Serve the content engine's MCP server at ``/mcp``; the lifespan runs its sessions."""
    server = build_content_mcp_server()
    app.state.content_mcp = server
    app.router.routes.append(http_route(server, MCP_PATH))


def _allow_the_frontend(app: FastAPI) -> None:
    """Let the deployed frontend, a separate origin, call the API.

    CORS_ALLOWED_ORIGINS is the deploy's comma- or space-separated list of origin patterns
    (exact origins or ``*`` wildcards, see ``app/cors.py``); localhost on any port is always
    allowed for development.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=build_cors_origin_regex(os.environ.get("CORS_ALLOWED_ORIGINS", "")),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def _concluded_lesson(_request: Request, exc: Exception) -> JSONResponse:
    """A write that reached a concluded study's record: 409, and the record stays as it was."""
    if not isinstance(exc, ConcludedLessonError):  # the only class this handler is registered for
        raise exc
    return JSONResponse(status_code=409, content={"detail": exc.detail})

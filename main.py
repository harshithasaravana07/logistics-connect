"""Application entry point: creates the FastAPI app, middleware, error handlers and routers."""
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1 import api_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import setup_logging
from app.core.rate_limit import RateLimitMiddleware
from app.db.session import engine
from app.ws.routes import router as ws_router

setup_logging()
log = logging.getLogger("app")


@asynccontextmanager
async def lifespan(_: FastAPI):
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    log.info("%s started (%s)", settings.APP_NAME, settings.ENVIRONMENT)
    yield


app = FastAPI(
    title=settings.APP_NAME, version="1.0.0", lifespan=lifespan,
    description="Backend API for the AI-powered Smart Logistics Accessibility Intelligence Platform "
                "for the North Eastern Region of India. Click **Authorize** and log in to try protected endpoints. "
                "WebSocket: `ws://HOST/ws/live` (protocol described in the README).")

app.add_middleware(RateLimitMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    # only method + path + status are logged: never bodies, query strings, tokens or passwords
    log.info("%s %s -> %s (%.0f ms)", request.method, request.url.path, response.status_code,
             (time.perf_counter() - start) * 1000)
    return response


def _error(status_code: int, code: str, message: str, details=None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": {"code": code, "message": message, "details": details}})


def _validation_details(errors) -> list[dict]:
    return [{"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]} for e in errors]


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError):
    return _error(exc.status_code, exc.code, exc.message, exc.details)


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(_: Request, exc: StarletteHTTPException):
    codes = {401: "unauthorized", 403: "forbidden", 404: "not_found", 405: "method_not_allowed"}
    return _error(exc.status_code, codes.get(exc.status_code, "http_error"), str(exc.detail))


@app.exception_handler(RequestValidationError)
async def request_validation_handler(_: Request, exc: RequestValidationError):
    return _error(422, "validation_error", "Request validation failed", _validation_details(exc.errors()))


@app.exception_handler(ValidationError)
async def pydantic_validation_handler(_: Request, exc: ValidationError):
    return _error(422, "validation_error", "Validation failed", _validation_details(exc.errors()))


@app.exception_handler(IntegrityError)
async def integrity_handler(_: Request, exc: IntegrityError):
    pgcode = getattr(exc.orig, "pgcode", None)
    if pgcode == "23505":
        return _error(409, "conflict", "A record with the same unique value already exists")
    if pgcode == "23503":
        return _error(422, "invalid_reference", "A referenced record (district, segment, user ...) does not exist "
                                               "or is still in use")
    log.warning("Integrity error pgcode=%s", pgcode)
    return _error(422, "integrity_error", "The data violates a database rule")


@app.exception_handler(Exception)
async def unhandled_handler(_: Request, exc: Exception):
    log.exception("Unhandled error")  # full traceback goes to the server log only
    return _error(500, "internal_error", "Something went wrong on the server")


@app.get("/health", tags=["System"], summary="Liveness + database check")
def health():
    with engine.connect() as conn:
        postgis = conn.execute(text("SELECT PostGIS_Version()")).scalar()
    return {"status": "ok", "postgis": postgis}


app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)

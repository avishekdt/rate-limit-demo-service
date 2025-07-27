# app/main.py
from fastapi import FastAPI
from app.limiter import RateLimiter
from app.config import settings
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exception_handler import register_exception_handlers
from app.logger_middleware import RequestLogger
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s - %(message)s"
)

app = FastAPI(
    title="Rate Limit Demo Service",
    description="A demo FastAPI app with in-memory rate limiting middleware.",
    version="0.1.0",
    contact={
        "name": "Avishek",
        "url": "https://github.com/avishekdt",
    },
)   
app.add_middleware(RequestLogger)
# Inject limiter with values from settings
app.add_middleware(
    RateLimiter,
    max_requests=settings.MAX_REQUESTS, 
    window_seconds=settings.WINDOW_SECONDS
)

register_exception_handlers(app)


@app.get("/", tags=["Root"], summary="Root endpoint")
def root():
    return {"message": "Welcome to the rate limit demo!"}


@app.get("/ping", tags=["Health"], summary="Ping endpoint", description="Simple ping check to test rate limiting.")
async def ping():
    return {"message": "pong"}


@app.get("/config-check", tags=["Config"], summary="Check rate limit config")
def read_config():
    return {
        "max_requests": settings.MAX_REQUESTS,
        "window": settings.WINDOW_SECONDS,
    }

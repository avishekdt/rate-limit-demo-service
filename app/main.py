# app/main.py
from fastapi import FastAPI
from app.limiter import RateLimiter
from app.config import settings

app = FastAPI()

# Inject limiter with values from settings
app.add_middleware(
    RateLimiter,
    max_requests=settings.MAX_REQUESTS,
    window_seconds=settings.WINDOW_SECONDS
)


@app.get("/")
def root():
    return {"message": "Welcome to the rate limit demo!"}



@app.get("/config-check")
def read_config():
    return {
        "max_requests": settings.MAX_REQUESTS,
        "window": settings.WINDOW_SECONDS,
    }

"""def read_config():
    return {
        "max_requests": settings.RATE_LIMIT_MAX_REQUESTS,
        "window": settings.RATE_LIMIT_TIME_WINDOW,
    }"""


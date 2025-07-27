# app/limiter.py
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("rate_limiter")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()

        request_log = f"Request from IP {ip} -> {request.url.path}"
        window = self.clients.get(ip, [])

        # Clean old timestamps
        window = [t for t in window if now - t < self.window]
        window.append(now)
        self.clients[ip] = window

        if len(window) > self.max_requests:
            logger.warning(f"{request_log} - BLOCKED (Rate Limit Exceeded)")
            return Response(
                content="Too Many Requests",
                status_code=429,
                headers={"Retry-After": str(self.window)},
            )

        response = await call_next(request)
        remaining = self.max_requests - len(window)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        logger.info(f"{request_log} - ALLOWED ({remaining} remaining)")
        return response

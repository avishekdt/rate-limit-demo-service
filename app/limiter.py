import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send
import logging
logger = logging.getLogger("rate_limiter")

class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}  # In-memory store
        logger.info("✅ RateLimiter middleware initialized")

    async def dispatch(self, request: Request, call_next):
        logger.info(f"📥 Incoming request from {request.client.host}")
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.clients:
            self.clients[client_ip] = []

        # Filter old requests
        request_times = [
            t for t in self.clients[client_ip]
            if t > current_time - self.window_seconds
        ]
        self.clients[client_ip] = request_times

        if len(request_times) >= self.max_requests:
            retry_after = int(self.window_seconds - (current_time - request_times[0]))
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after)
                }
            )

        # Allow request
        self.clients[client_ip].append(current_time)
        remaining = self.max_requests - len(self.clients[client_ip])
        reset = int(self.window_seconds)

        # Modify response before returning it
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset)

        return response

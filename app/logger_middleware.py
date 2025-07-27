import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("request_logger")

class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host
        method = request.method
        path = request.url.path

        logger.info(f"📥 {client_ip} - {method} {path} (incoming)")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("💥 Exception occurred while processing request")
            raise

        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"📤 {client_ip} - {method} {path} → {response.status_code} ({process_time:.2f}ms)"
        )

        return response

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logging import logger

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(f"CorrelationID: {correlation_id} - {request.method} {request.url.path} completed in {process_time:.2f}s")
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        except Exception as e:
            logger.error(f"CorrelationID: {correlation_id} - Error processing request: {str(e)}")
            raise
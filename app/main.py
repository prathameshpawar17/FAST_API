from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import cache, sms, employees, auth, textract
from app.services.sms_gateway import sms_gateway
from app.core.logging import setup_logging
from app.db.database import Base
from app.db.database import engine
from app.middleware.correlation_id import CorrelationIdMiddleware
import asyncio
import logging

setup_logging()
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(cache.router, tags=["cache"])
app.include_router(sms.router, tags=["sms"])
app.include_router(employees.router, tags=["employees"])
app.include_router(auth.router, tags=["auth"])
app.include_router(textract.router, tags=["textract"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request started: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Request completed: {request.method} {request.url}")
    return response

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(sms_gateway.retry_failed_messages())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from app.api.routes import cache, sms
from app.services.sms_gateway import sms_gateway
from app.core.logging import setup_logging
import asyncio

setup_logging()

app = FastAPI()

app.include_router(cache.router, tags=["cache"])
app.include_router(sms.router, tags=["sms"])

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(sms_gateway.retry_failed_messages())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_logging import ErrorLoggingMiddleware
from app.routers import textract
from app.config import settings

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom error logging middleware
app.add_middleware(ErrorLoggingMiddleware)

# Include routers
app.include_router(textract.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Day 3 API"}
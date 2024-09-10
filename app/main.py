# app/main.py
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.api.endpoints import employee
from app.core.config import settings
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management System")

# Add middleware
app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

# Include routers
app.include_router(employee.router, prefix="/api/v1/employees", tags=["employees"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Management System"}
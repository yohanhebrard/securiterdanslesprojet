"""API v1 routes"""
from fastapi import APIRouter

from app.api.v1 import upload, download

api_router = APIRouter()

# Include sub-routers
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(download.router, prefix="/download", tags=["download"])

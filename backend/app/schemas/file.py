"""
File schemas for API requests and responses
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    """Response after successful file upload"""

    file_id: str = Field(..., description="Unique file identifier")
    download_url: str = Field(..., description="One-time download URL")
    download_token: str = Field(..., description="Download token")
    expires_at: datetime = Field(..., description="Expiration timestamp (UTC)")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")

    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "550e8400-e29b-41d4-a716-446655440000",
                "download_url": "http://localhost:8000/api/v1/download/a1b2c3d4...",
                "download_token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
                "expires_at": "2025-01-06T15:30:00Z",
                "filename": "document.pdf",
                "file_size": 1048576,
                "mime_type": "application/pdf",
            }
        }


class FileInfoResponse(BaseModel):
    """File metadata without downloading"""

    filename: str
    file_size: int
    mime_type: str
    uploaded_at: datetime
    expires_at: datetime
    is_available: bool
    antivirus_status: str

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.pdf",
                "file_size": 1048576,
                "mime_type": "application/pdf",
                "uploaded_at": "2025-01-05T15:30:00Z",
                "expires_at": "2025-01-06T15:30:00Z",
                "is_available": True,
                "antivirus_status": "clean",
            }
        }


class UploadRequest(BaseModel):
    """Upload request parameters"""

    ttl_hours: Optional[int] = Field(
        24, ge=1, le=48, description="Time to live in hours (1-48)"
    )

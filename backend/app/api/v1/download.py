"""
File Download Endpoint
Handles secure one-time file download with atomic deletion
"""
import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.core.config import settings
from app.core.database import get_db
from app.models.file import File as FileModel
from app.models.audit_log import AuditLog
from app.schemas.file import FileInfoResponse
from app.services.token_service import TokenService
from app.services.encryption import encryption_service
from app.services.storage import StorageService

router = APIRouter()

# Initialize services
token_service = TokenService()
storage_service = StorageService()


def _is_test_mode() -> bool:
    """Check if running in test mode (SQLite doesn't support FOR UPDATE)"""
    return os.environ.get("ENVIRONMENT") == "test"


@router.get("/info/{token}", response_model=FileInfoResponse)
async def get_file_info(
    token: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get file metadata without downloading

    Args:
        token: Download token
        request: FastAPI request object
        db: Database session

    Returns:
        FileInfoResponse with file metadata

    Raises:
        HTTPException: 404 if not found, 410 if expired/downloaded
    """

    # Hash token to find file
    token_hash = token_service.hash_token(token)

    # Query file from database
    file_record = db.query(FileModel).filter(FileModel.token_hash == token_hash).first()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Check if file is available
    if not file_record.is_available:
        if file_record.is_expired:
            detail = "File has expired"
        elif file_record.is_downloaded:
            detail = "File has already been downloaded"
        else:
            detail = "File is not available"

        raise HTTPException(status_code=410, detail=detail)

    # Log audit event
    ip_hash = token_service.hash_ip(request.client.host)
    audit_log = AuditLog(
        event_type="info_view",
        file_id=file_record.id,
        ip_hash=ip_hash,
        event_metadata={
            "filename": file_record.filename,
        },
    )
    db.add(audit_log)
    db.commit()

    return FileInfoResponse(
        filename=file_record.filename,
        file_size=file_record.file_size,
        mime_type=file_record.mime_type,
        expires_at=file_record.expires_at,
        uploaded_at=file_record.uploaded_at,
        is_available=file_record.is_available,
        antivirus_status=file_record.antivirus_status,
    )


@router.get("/{token}")
async def download_file(
    token: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Download file with one-time use and atomic deletion

    Steps:
    1. Validate token and find file
    2. Check file availability (not expired, not downloaded)
    3. Mark as downloaded BEFORE streaming (atomic operation)
    4. Retrieve encrypted file from MinIO
    5. Decrypt file
    6. Stream to client
    7. Delete from storage after successful download
    8. Log audit event

    Args:
        token: Download token
        request: FastAPI request object
        db: Database session

    Returns:
        StreamingResponse with decrypted file

    Raises:
        HTTPException: 404 if not found, 410 if expired/downloaded
    """

    # Step 1: Hash token to find file
    token_hash = token_service.hash_token(token)

    # Query file from database with row-level locking (FOR UPDATE)
    # Note: SQLite doesn't support FOR UPDATE, so skip in test mode
    query = db.query(FileModel).filter(FileModel.token_hash == token_hash)
    if not _is_test_mode():
        query = query.with_for_update()
    file_record = query.first()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Step 2: Check if file is available
    if not file_record.is_available:
        if file_record.is_expired:
            detail = "File has expired"
        elif file_record.is_downloaded:
            detail = "File has already been downloaded (one-time use)"
        else:
            detail = "File is not available"

        raise HTTPException(status_code=410, detail=detail)

    # Step 3: Mark as downloaded ATOMICALLY (prevents concurrent downloads)
    file_record.downloaded_at = datetime.utcnow()
    db.commit()

    try:
        # Step 4: Retrieve encrypted file from MinIO
        try:
            encrypted_content = storage_service.download_file(file_record.storage_key)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Storage retrieval failed: {str(e)}"
            )

        # Step 5: Decrypt file
        try:
            decrypted_content = encryption_service.decrypt_file(
                encrypted_content,
                file_record.encryption_metadata
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Decryption failed: {str(e)}"
            )

        # Step 6: Log successful download
        ip_hash = token_service.hash_ip(request.client.host)
        audit_log = AuditLog(
            event_type="download",
            file_id=file_record.id,
            ip_hash=ip_hash,
            event_metadata={
                "filename": file_record.filename,
                "file_size": file_record.file_size,
            },
        )
        db.add(audit_log)
        db.commit()

        # Step 7: Delete from storage (async, after streaming starts)
        # Note: In production, this should be a background task
        try:
            storage_service.delete_file(file_record.storage_key)
        except Exception as e:
            # Log deletion failure but don't block download
            error_log = AuditLog(
                event_type="error",
                file_id=file_record.id,
                ip_hash=ip_hash,
                event_metadata={
                    "error": "Storage deletion failed",
                    "details": str(e),
                },
            )
            db.add(error_log)
            db.commit()

        # Step 8: Stream file to client
        file_stream = io.BytesIO(decrypted_content)

        return StreamingResponse(
            file_stream,
            media_type=file_record.mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="{file_record.filename}"',
                "Content-Length": str(file_record.file_size),
                # Security headers
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                "Pragma": "no-cache",
            },
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        ip_hash = token_service.hash_ip(request.client.host)
        error_log = AuditLog(
            event_type="error",
            file_id=file_record.id,
            ip_hash=ip_hash,
            event_metadata={
                "error": "Download failed",
                "details": str(e),
            },
        )
        db.add(error_log)
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )

"""
File Upload Endpoint
Handles secure file upload with antivirus scan, encryption, and storage
"""
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.file import File as FileModel
from app.models.audit_log import AuditLog
from app.schemas.file import FileUploadResponse
from app.services.token_service import TokenService
from app.services.encryption import encryption_service
from app.services.storage import StorageService
from app.services.antivirus import antivirus_service

router = APIRouter()

# Initialize services
token_service = TokenService()
storage_service = StorageService()


@router.post("", response_model=FileUploadResponse, status_code=201)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    ttl_hours: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Upload a file securely

    Steps:
    1. Validate file size and type
    2. Scan for malware with ClamAV
    3. Encrypt file with AES-256-GCM
    4. Store in MinIO
    5. Generate secure token
    6. Save metadata to database
    7. Log audit event

    Args:
        request: FastAPI request object (for IP tracking)
        file: Uploaded file
        ttl_hours: Time-to-live in hours (default: 24)
        db: Database session

    Returns:
        FileUploadResponse with download URL and token

    Raises:
        HTTPException: 400 for invalid file, 413 for too large, 422 for malware
    """

    # Step 1: Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Check file size limit
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")

    # Step 2: Scan for malware
    is_clean, scan_result = antivirus_service.scan_file(file_content)

    if not is_clean:
        # Log malware detection
        ip_hash = token_service.hash_ip(request.client.host)
        audit_log = AuditLog(
            event_type="malware_detected",
            ip_hash=ip_hash,
            event_metadata={
                "filename": file.filename,
                "scan_result": scan_result,
                "file_size": file_size,
            },
        )
        db.add(audit_log)
        db.commit()

        raise HTTPException(
            status_code=422,
            detail=f"File rejected: {scan_result}"
        )

    # Step 3: Encrypt file
    try:
        encrypted_content, encryption_metadata = encryption_service.encrypt_file(file_content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Encryption failed: {str(e)}"
        )

    # Step 4: Generate unique storage key
    file_id = uuid.uuid4()
    storage_key = f"{file_id}.enc"

    # Step 5: Store in MinIO
    try:
        storage_service.upload_file(
            object_name=storage_key,
            data=encrypted_content,
            content_type="application/octet-stream",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Storage failed: {str(e)}"
        )

    # Step 6: Generate secure token
    download_token, token_hash = token_service.generate_token()

    # Calculate expiration time
    ttl = ttl_hours if ttl_hours else settings.DEFAULT_TTL_HOURS
    expires_at = datetime.utcnow() + timedelta(hours=ttl)

    # Step 7: Save file metadata to database
    ip_hash = token_service.hash_ip(request.client.host)

    file_record = FileModel(
        id=file_id,
        token_hash=token_hash,
        filename=file.filename,
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        storage_key=storage_key,
        encryption_metadata=encryption_metadata,
        expires_at=expires_at,
        ip_hash=ip_hash,
        antivirus_status="clean",
    )

    db.add(file_record)
    db.flush()  # Flush to ensure file_id exists before adding audit log

    # Step 8: Log audit event
    audit_log = AuditLog(
        event_type="upload",
        file_id=file_id,
        ip_hash=ip_hash,
        event_metadata={
            "filename": file.filename,
            "file_size": file_size,
            "mime_type": file.content_type,
            "ttl_hours": ttl,
        },
    )
    db.add(audit_log)

    # Commit transaction
    db.commit()
    db.refresh(file_record)

    # Step 9: Generate download URL
    download_url = f"{settings.API_BASE_URL}/api/v1/download/{download_token}"

    return FileUploadResponse(
        file_id=str(file_id),
        download_url=download_url,
        download_token=download_token,
        expires_at=expires_at,
        filename=file.filename,
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
    )

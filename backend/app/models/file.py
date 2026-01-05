"""
File model - Stores metadata for uploaded files
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, BigInteger, DateTime, Integer, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class File(Base):
    """File metadata model"""

    __tablename__ = "files"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Token (hashed)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)

    # File metadata
    filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # bytes

    # Storage
    storage_key = Column(String(255), unique=True, nullable=False)  # S3 object key

    # Encryption metadata
    encryption_metadata = Column(JSON, nullable=True)  # IV, tag, KEK version

    # User tracking (anonymized)
    ip_hash = Column(String(64), nullable=False, index=True)  # SHA-256(IP + salt)

    # Timestamps
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False, index=True)
    downloaded_at = Column(DateTime, nullable=True)  # NULL = not yet downloaded

    # Antivirus status
    antivirus_status = Column(
        String(20), nullable=False, default="pending"
    )  # pending, clean, infected
    antivirus_scanned_at = Column(DateTime, nullable=True)

    # Audit
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<File {self.id} - {self.filename}>"

    @property
    def is_expired(self) -> bool:
        """Check if file has expired"""
        return datetime.utcnow() > self.expires_at

    @property
    def is_downloaded(self) -> bool:
        """Check if file has been downloaded"""
        return self.downloaded_at is not None

    @property
    def is_available(self) -> bool:
        """Check if file is available for download"""
        return (
            not self.is_expired
            and not self.is_downloaded
            and self.antivirus_status == "clean"
        )

    def set_expiry(self, hours: int) -> None:
        """Set file expiration time"""
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)

"""
Audit Log model - Tracks all security events
"""
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

from app.core.database import Base


class AuditLog(Base):
    """Audit log model for security events"""

    __tablename__ = "audit_logs"

    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Event information
    event_type = Column(
        String(50), nullable=False, index=True
    )  # upload, download, delete, error, abuse

    # Reference to file (nullable if file is deleted)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), nullable=True)

    # User tracking (anonymized)
    ip_hash = Column(String(64), nullable=False, index=True)
    user_agent_hash = Column(String(64), nullable=True)

    # Event metadata (flexible JSON field)
    metadata = Column(JSON, nullable=True)

    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AuditLog {self.id} - {self.event_type} at {self.timestamp}>"

"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-05 12:00:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables"""

    # Create files table
    op.create_table(
        'files',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('token_hash', sa.String(64), nullable=False, unique=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('mime_type', sa.String(100), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('storage_key', sa.String(255), nullable=False, unique=True),
        sa.Column('encryption_metadata', postgresql.JSON(), nullable=True),
        sa.Column('ip_hash', sa.String(64), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('downloaded_at', sa.DateTime(), nullable=True),
        sa.Column('antivirus_status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('antivirus_scanned_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Create indexes on files table
    op.create_index('ix_files_token_hash', 'files', ['token_hash'])
    op.create_index('ix_files_expires_at', 'files', ['expires_at'])
    op.create_index('ix_files_ip_hash', 'files', ['ip_hash'])

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('file_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ip_hash', sa.String(64), nullable=False),
        sa.Column('user_agent_hash', sa.String(64), nullable=True),
        sa.Column('metadata', postgresql.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    # Create indexes on audit_logs table
    op.create_index('ix_audit_logs_event_type', 'audit_logs', ['event_type'])
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])
    op.create_index('ix_audit_logs_ip_hash', 'audit_logs', ['ip_hash'])

    # Create foreign key
    op.create_foreign_key(
        'fk_audit_logs_file_id',
        'audit_logs',
        'files',
        ['file_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('audit_logs')
    op.drop_table('files')

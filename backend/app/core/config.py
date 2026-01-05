"""
Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # App
    APP_NAME: str = "SecureShare"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production-min-32-chars"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://secureshare:devpassword@postgres:5432/secureshare"

    # Redis
    REDIS_URL: str = "redis://:redispassword@redis:6379/0"

    # Storage (MinIO/S3)
    STORAGE_TYPE: str = "minio"
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET: str = "secureshare-files"
    MINIO_QUARANTINE_BUCKET: str = "secureshare-quarantine"
    MINIO_SECURE: bool = False

    # Vault
    VAULT_ADDR: str = "http://vault:8200"
    VAULT_TOKEN: str = "dev-root-token"
    VAULT_TRANSIT_KEY_NAME: str = "file-encryption"

    # ClamAV
    ANTIVIRUS_ENABLED: bool = True
    CLAMAV_HOST: str = "clamav"
    CLAMAV_PORT: int = 3310
    CLAMAV_TIMEOUT: int = 120

    # Security
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_GLOBAL_PER_MINUTE: int = 100
    RATE_LIMIT_UPLOAD_PER_HOUR: int = 10
    RATE_LIMIT_DOWNLOAD_PER_HOUR: int = 50

    # File Upload
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_MIME_TYPES: str = "application/pdf,image/jpeg,image/png,image/gif,application/zip,text/plain"

    # Token
    TOKEN_LENGTH: int = 32  # bytes (256 bits)
    DEFAULT_TTL_HOURS: int = 24
    MAX_TTL_HOURS: int = 48

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    CORS_ALLOW_CREDENTIALS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

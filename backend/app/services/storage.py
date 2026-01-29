"""
Storage Service - MinIO/S3 integration
"""
import io
import os
from typing import Optional
from app.core.config import settings


class StorageService:
    """Service for file storage operations (MinIO/S3)"""

    def __init__(self):
        self._client: Optional[object] = None
        self._initialized = False
        # In-memory storage for testing
        self._test_storage: dict = {}

    @property
    def client(self):
        """Lazy initialization of MinIO client"""
        if self._client is None and not self._is_test_mode():
            from minio import Minio
            self._client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE,
            )
            self._ensure_buckets()
        return self._client

    def _is_test_mode(self) -> bool:
        """Check if running in test mode"""
        return os.environ.get("ENVIRONMENT") == "test"

    def _ensure_buckets(self):
        """Ensure required buckets exist"""
        if self._is_test_mode():
            return
        try:
            from minio.error import S3Error
            if not self._client.bucket_exists(settings.MINIO_BUCKET):
                self._client.make_bucket(settings.MINIO_BUCKET)
            if not self._client.bucket_exists(settings.MINIO_QUARANTINE_BUCKET):
                self._client.make_bucket(settings.MINIO_QUARANTINE_BUCKET)
        except Exception:
            pass  # Buckets may already exist

    def upload_file(
        self, object_name: str, data: bytes, content_type: str = "application/octet-stream"
    ) -> bool:
        """
        Upload file to storage

        Args:
            object_name: S3 object key
            data: File content as bytes
            content_type: MIME type

        Returns:
            bool: True if successful
        """
        # Test mode: use in-memory storage
        if self._is_test_mode():
            self._test_storage[object_name] = data
            return True

        try:
            data_stream = io.BytesIO(data)
            self.client.put_object(
                settings.MINIO_BUCKET,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type,
            )
            return True
        except Exception as e:
            print(f"Storage upload error: {e}")
            return False

    def download_file(self, object_name: str) -> bytes:
        """
        Download file from storage

        Args:
            object_name: S3 object key

        Returns:
            bytes: File content

        Raises:
            Exception: If file not found or download fails
        """
        # Test mode: use in-memory storage
        if self._is_test_mode():
            if object_name in self._test_storage:
                return self._test_storage[object_name]
            raise Exception(f"File not found: {object_name}")

        response = self.client.get_object(settings.MINIO_BUCKET, object_name)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def delete_file(self, object_name: str) -> bool:
        """
        Delete file from storage

        Args:
            object_name: S3 object key

        Returns:
            bool: True if successful
        """
        # Test mode: use in-memory storage
        if self._is_test_mode():
            if object_name in self._test_storage:
                del self._test_storage[object_name]
            return True

        try:
            self.client.remove_object(settings.MINIO_BUCKET, object_name)
            return True
        except Exception as e:
            print(f"Storage delete error: {e}")
            return False

    def file_exists(self, object_name: str) -> bool:
        """Check if file exists in storage"""
        # Test mode: use in-memory storage
        if self._is_test_mode():
            return object_name in self._test_storage

        try:
            self.client.stat_object(settings.MINIO_BUCKET, object_name)
            return True
        except Exception:
            return False


# Singleton instance
storage_service = StorageService()

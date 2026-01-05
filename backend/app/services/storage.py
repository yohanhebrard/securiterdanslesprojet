"""
Storage Service - MinIO/S3 integration
"""
import io
from typing import BinaryIO
from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class StorageService:
    """Service for file storage operations (MinIO/S3)"""

    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._ensure_buckets()

    def _ensure_buckets(self):
        """Ensure required buckets exist"""
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET):
                self.client.make_bucket(settings.MINIO_BUCKET)
            if not self.client.bucket_exists(settings.MINIO_QUARANTINE_BUCKET):
                self.client.make_bucket(settings.MINIO_QUARANTINE_BUCKET)
        except S3Error:
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
        except S3Error as e:
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
            S3Error: If file not found or download fails
        """
        try:
            response = self.client.get_object(settings.MINIO_BUCKET, object_name)
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
        try:
            self.client.remove_object(settings.MINIO_BUCKET, object_name)
            return True
        except S3Error as e:
            print(f"Storage delete error: {e}")
            return False

    def file_exists(self, object_name: str) -> bool:
        """Check if file exists in storage"""
        try:
            self.client.stat_object(settings.MINIO_BUCKET, object_name)
            return True
        except S3Error:
            return False


# Singleton instance
storage_service = StorageService()

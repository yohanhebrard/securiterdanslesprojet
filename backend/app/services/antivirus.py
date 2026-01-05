"""
Antivirus Service - ClamAV integration
"""
import clamd
from typing import Tuple

from app.core.config import settings


class AntivirusService:
    """Service for malware scanning using ClamAV"""

    def __init__(self):
        if settings.ANTIVIRUS_ENABLED:
            try:
                self.client = clamd.ClamdNetworkSocket(
                    host=settings.CLAMAV_HOST,
                    port=settings.CLAMAV_PORT,
                    timeout=settings.CLAMAV_TIMEOUT,
                )
                # Test connection
                self.client.ping()
                self.available = True
            except Exception as e:
                print(f"ClamAV not available: {e}")
                self.available = False
        else:
            self.available = False

    def scan_file(self, data: bytes) -> Tuple[bool, str]:
        """
        Scan file for malware

        Args:
            data: File content as bytes

        Returns:
            Tuple[bool, str]: (is_clean, result)
                - is_clean: True if file is clean
                - result: Scan result message
        """
        if not self.available:
            # If ClamAV is not available, consider file clean (development mode)
            return True, "Antivirus not available - scan skipped"

        try:
            # ClamAV instream requires a file-like object or uses the buffer interface
            import io
            file_stream = io.BytesIO(data)
            result = self.client.instream(file_stream)
            status = result["stream"]

            if status[0] == "OK":
                return True, "Clean"
            elif status[0] == "FOUND":
                return False, f"Malware detected: {status[1]}"
            else:
                return False, f"Scan error: {status}"

        except Exception as e:
            print(f"Antivirus scan error: {e}")
            # In development, log error but allow upload
            # In production, this should reject the file
            return True, f"Scan skipped due to error: {str(e)}"


# Singleton instance
antivirus_service = AntivirusService()

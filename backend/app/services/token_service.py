"""
Token Service - Generate and validate secure tokens
"""
import secrets
import hashlib
from typing import Tuple

from app.core.config import settings


class TokenService:
    """Service for generating and validating cryptographically secure tokens"""

    @staticmethod
    def generate_token() -> Tuple[str, str]:
        """
        Generate a cryptographically secure token

        Returns:
            Tuple[str, str]: (token, token_hash)
                - token: Raw token to send to user (URL-safe base64)
                - token_hash: SHA-256 hash to store in database
        """
        # Generate random token (256 bits = 32 bytes)
        token_bytes = secrets.token_bytes(settings.TOKEN_LENGTH)
        token = secrets.token_urlsafe(settings.TOKEN_LENGTH)

        # Hash token for storage (SHA-256)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        return token, token_hash

    @staticmethod
    def hash_token(token: str) -> str:
        """
        Hash a token using SHA-256

        Args:
            token: Raw token string

        Returns:
            str: SHA-256 hash (hex)
        """
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def hash_ip(ip: str, salt: str = "") -> str:
        """
        Hash IP address for privacy (RGPD compliant)

        Args:
            ip: IP address
            salt: Optional daily salt for hashing

        Returns:
            str: SHA-256 hash (hex)
        """
        data = f"{ip}{salt}".encode()
        return hashlib.sha256(data).hexdigest()

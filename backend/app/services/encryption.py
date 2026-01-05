"""
Encryption Service - AES-256-GCM encryption
"""
import os
from typing import Tuple, Dict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings


class EncryptionService:
    """Service for file encryption/decryption using AES-256-GCM"""

    def __init__(self):
        # For demo purposes, we generate a key
        # In production, this should come from Vault KMS
        self.key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    def encrypt_file(self, data: bytes) -> Tuple[bytes, Dict[str, str]]:
        """
        Encrypt file data using AES-256-GCM

        Args:
            data: File content as bytes

        Returns:
            Tuple[bytes, Dict]: (encrypted_data, metadata)
                - encrypted_data: Ciphertext
                - metadata: IV and other encryption metadata
        """
        # Generate random IV (96 bits = 12 bytes for GCM)
        iv = os.urandom(12)

        # Encrypt
        ciphertext = self.aesgcm.encrypt(iv, data, None)

        # Return encrypted data and metadata
        metadata = {
            "algorithm": "AES-256-GCM",
            "iv": iv.hex(),
            "key_version": "1",
        }

        return ciphertext, metadata

    def decrypt_file(self, ciphertext: bytes, metadata: Dict[str, str]) -> bytes:
        """
        Decrypt file data

        Args:
            ciphertext: Encrypted file content
            metadata: Encryption metadata (IV, etc.)

        Returns:
            bytes: Decrypted file content

        Raises:
            Exception: If decryption fails
        """
        iv = bytes.fromhex(metadata["iv"])
        plaintext = self.aesgcm.decrypt(iv, ciphertext, None)
        return plaintext


# Singleton instance
encryption_service = EncryptionService()

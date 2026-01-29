"""
Unit Tests for Backend Services
"""
import pytest
from app.services.token_service import TokenService
from app.services.encryption import EncryptionService


class TestTokenService:
    """Tests for TokenService"""

    def test_generate_token_returns_tuple(self):
        """Test that generate_token returns a tuple of (token, hash)"""
        service = TokenService()
        result = service.generate_token()

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_generate_token_different_each_time(self):
        """Test that each token generation is unique"""
        service = TokenService()

        token1, hash1 = service.generate_token()
        token2, hash2 = service.generate_token()

        assert token1 != token2
        assert hash1 != hash2

    def test_token_hash_is_sha256(self):
        """Test that token hash is a valid SHA-256 hex digest"""
        service = TokenService()
        _, token_hash = service.generate_token()

        # SHA-256 produces 64 hex characters
        assert len(token_hash) == 64
        assert all(c in "0123456789abcdef" for c in token_hash)

    def test_hash_token_consistency(self):
        """Test that hash_token produces consistent results"""
        service = TokenService()
        token, expected_hash = service.generate_token()

        computed_hash = service.hash_token(token)
        assert computed_hash == expected_hash

    def test_hash_ip_anonymization(self):
        """Test IP hashing for RGPD compliance"""
        service = TokenService()

        ip = "192.168.1.100"
        hashed_ip = service.hash_ip(ip)

        # Should return a SHA-256 hash
        assert len(hashed_ip) == 64

        # Same IP should produce same hash
        assert service.hash_ip(ip) == hashed_ip

        # Different IP should produce different hash
        assert service.hash_ip("192.168.1.101") != hashed_ip

    def test_hash_ip_with_salt(self):
        """Test IP hashing with salt"""
        service = TokenService()
        ip = "192.168.1.100"

        hash1 = service.hash_ip(ip, salt="salt1")
        hash2 = service.hash_ip(ip, salt="salt2")

        assert hash1 != hash2


class TestEncryptionService:
    """Tests for EncryptionService"""

    def test_encrypt_file_returns_tuple(self):
        """Test that encrypt_file returns ciphertext and metadata"""
        service = EncryptionService()
        data = b"Test data for encryption"

        ciphertext, metadata = service.encrypt_file(data)

        assert isinstance(ciphertext, bytes)
        assert isinstance(metadata, dict)

    def test_encrypt_file_metadata_structure(self):
        """Test encryption metadata structure"""
        service = EncryptionService()
        data = b"Test data"

        _, metadata = service.encrypt_file(data)

        assert "algorithm" in metadata
        assert "iv" in metadata
        assert "key_version" in metadata
        assert metadata["algorithm"] == "AES-256-GCM"

    def test_encrypt_decrypt_roundtrip(self):
        """Test that encryption and decryption work correctly"""
        service = EncryptionService()
        original_data = b"This is sensitive test data that should be encrypted"

        ciphertext, metadata = service.encrypt_file(original_data)
        decrypted_data = service.decrypt_file(ciphertext, metadata)

        assert decrypted_data == original_data

    def test_ciphertext_differs_from_plaintext(self):
        """Test that ciphertext is different from plaintext"""
        service = EncryptionService()
        data = b"Test data"

        ciphertext, _ = service.encrypt_file(data)

        assert ciphertext != data

    def test_different_iv_for_each_encryption(self):
        """Test that each encryption uses a different IV"""
        service = EncryptionService()
        data = b"Same data"

        _, metadata1 = service.encrypt_file(data)
        _, metadata2 = service.encrypt_file(data)

        assert metadata1["iv"] != metadata2["iv"]

    def test_encrypt_empty_data(self):
        """Test encryption of empty data"""
        service = EncryptionService()
        data = b""

        ciphertext, metadata = service.encrypt_file(data)
        decrypted = service.decrypt_file(ciphertext, metadata)

        assert decrypted == data

    def test_encrypt_large_data(self):
        """Test encryption of large data"""
        service = EncryptionService()
        # 1 MB of data
        data = b"x" * (1024 * 1024)

        ciphertext, metadata = service.encrypt_file(data)
        decrypted = service.decrypt_file(ciphertext, metadata)

        assert decrypted == data


class TestAntivirusService:
    """Tests for AntivirusService (mocked)"""

    def test_scan_returns_tuple(self):
        """Test that scan returns (is_clean, result) tuple"""
        # Import after environment is set
        from app.services.antivirus import antivirus_service

        result = antivirus_service.scan_file(b"Test content")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)

    def test_scan_clean_file_in_test_mode(self):
        """Test that scan returns clean in test mode (antivirus disabled)"""
        from app.services.antivirus import antivirus_service

        is_clean, message = antivirus_service.scan_file(b"Normal file content")

        # With ANTIVIRUS_ENABLED=false, should return clean
        assert is_clean is True

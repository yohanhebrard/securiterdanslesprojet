"""
Integration Tests for API Endpoints
"""
import pytest
import io
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check_returns_200(self, client: TestClient):
        """Test health endpoint returns 200"""
        response = client.get("/health")

        assert response.status_code == 200

    def test_health_check_response_structure(self, client: TestClient):
        """Test health endpoint response structure"""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert data["status"] == "healthy"


class TestUploadEndpoint:
    """Tests for file upload endpoint"""

    def test_upload_file_success(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test successful file upload"""
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}

        response = client.post("/api/v1/upload", files=files)

        assert response.status_code == 201
        data = response.json()

        assert "file_id" in data
        assert "download_url" in data
        assert "download_token" in data
        assert "expires_at" in data
        assert "filename" in data
        assert "file_size" in data
        assert "mime_type" in data

    def test_upload_file_returns_correct_filename(
        self, client: TestClient, sample_file_content: bytes
    ):
        """Test that upload returns the correct filename"""
        filename = "my-document.pdf"
        files = {"file": (filename, io.BytesIO(sample_file_content), "application/pdf")}

        response = client.post("/api/v1/upload", files=files)
        data = response.json()

        assert data["filename"] == filename

    def test_upload_file_returns_correct_size(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test that upload returns the correct file size"""
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}

        response = client.post("/api/v1/upload", files=files)
        data = response.json()

        assert data["file_size"] == len(sample_file_content)

    def test_upload_empty_file_fails(self, client: TestClient, sample_filename: str):
        """Test that uploading empty file fails"""
        files = {"file": (sample_filename, io.BytesIO(b""), "text/plain")}

        response = client.post("/api/v1/upload", files=files)

        assert response.status_code == 400
        assert "Empty file" in response.json()["detail"]

    def test_upload_without_file_fails(self, client: TestClient):
        """Test that request without file fails"""
        response = client.post("/api/v1/upload")

        assert response.status_code == 422  # Validation error

    def test_upload_generates_unique_tokens(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test that each upload generates a unique token"""
        files1 = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}
        files2 = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}

        response1 = client.post("/api/v1/upload", files=files1)
        response2 = client.post("/api/v1/upload", files=files2)

        token1 = response1.json()["download_token"]
        token2 = response2.json()["download_token"]

        assert token1 != token2


class TestDownloadEndpoint:
    """Tests for file download endpoint"""

    def test_download_file_success(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test successful file download"""
        # First upload a file
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}
        upload_response = client.post("/api/v1/upload", files=files)
        token = upload_response.json()["download_token"]

        # Then download it
        download_response = client.get(f"/api/v1/download/{token}")

        assert download_response.status_code == 200
        assert download_response.content == sample_file_content

    def test_download_sets_content_disposition(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test that download sets Content-Disposition header"""
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}
        upload_response = client.post("/api/v1/upload", files=files)
        token = upload_response.json()["download_token"]

        download_response = client.get(f"/api/v1/download/{token}")

        assert "content-disposition" in download_response.headers
        assert sample_filename in download_response.headers["content-disposition"]

    def test_download_one_time_use(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test that file can only be downloaded once"""
        # Upload file
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}
        upload_response = client.post("/api/v1/upload", files=files)
        token = upload_response.json()["download_token"]

        # First download should succeed
        response1 = client.get(f"/api/v1/download/{token}")
        assert response1.status_code == 200

        # Second download should fail
        response2 = client.get(f"/api/v1/download/{token}")
        assert response2.status_code == 410
        assert "already been downloaded" in response2.json()["detail"]

    def test_download_invalid_token(self, client: TestClient):
        """Test download with invalid token returns 404"""
        response = client.get("/api/v1/download/invalid-token-12345")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestInfoEndpoint:
    """Tests for file info endpoint"""

    def test_info_endpoint_returns_metadata(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test that info endpoint returns file metadata"""
        # Upload file
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}
        upload_response = client.post("/api/v1/upload", files=files)
        token = upload_response.json()["download_token"]

        # Get info
        info_response = client.get(f"/api/v1/download/info/{token}")

        assert info_response.status_code == 200
        data = info_response.json()

        assert data["filename"] == sample_filename
        assert data["file_size"] == len(sample_file_content)
        assert data["is_available"] is True
        assert "expires_at" in data
        assert "uploaded_at" in data
        assert "antivirus_status" in data

    def test_info_does_not_consume_download(
        self, client: TestClient, sample_file_content: bytes, sample_filename: str
    ):
        """Test that viewing info doesn't consume the download"""
        # Upload file
        files = {"file": (sample_filename, io.BytesIO(sample_file_content), "text/plain")}
        upload_response = client.post("/api/v1/upload", files=files)
        token = upload_response.json()["download_token"]

        # View info multiple times
        client.get(f"/api/v1/download/info/{token}")
        client.get(f"/api/v1/download/info/{token}")

        # Download should still work
        download_response = client.get(f"/api/v1/download/{token}")
        assert download_response.status_code == 200

    def test_info_invalid_token(self, client: TestClient):
        """Test info with invalid token returns 404"""
        response = client.get("/api/v1/download/info/invalid-token-12345")

        assert response.status_code == 404


class TestSecurityHeaders:
    """Tests for security headers"""

    def test_security_headers_present(self, client: TestClient):
        """Test that security headers are present in responses"""
        response = client.get("/health")

        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        assert "content-security-policy" in response.headers
        assert "referrer-policy" in response.headers

    def test_x_frame_options_deny(self, client: TestClient):
        """Test X-Frame-Options is set to DENY"""
        response = client.get("/health")

        assert response.headers["x-frame-options"] == "DENY"

    def test_x_content_type_options_nosniff(self, client: TestClient):
        """Test X-Content-Type-Options is set to nosniff"""
        response = client.get("/health")

        assert response.headers["x-content-type-options"] == "nosniff"

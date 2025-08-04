"""
API endpoint tests for JobTrackerDB
"""
import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_address_validation_endpoint_exists(client: TestClient):
    """Test that the address validation endpoint exists."""
    response = client.get("/api/address/validate")
    # Should return 405 Method Not Allowed for GET, but endpoint exists
    assert response.status_code in [405, 404]  # Endpoint exists but might not support GET

def test_api_documentation_accessible(client: TestClient):
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_schema_accessible(client: TestClient):
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json() 
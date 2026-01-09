import pytest
from fastapi import status

def test_security_headers_on_root_endpoint(client):
    """Test that security headers are present in responses"""
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    
    # Check for security headers
    assert "Content-Security-Policy" in response.headers
    assert "X-Content-Type-Options" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    
    assert "X-XSS-Protection" in response.headers
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    
    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"
    
    assert "Strict-Transport-Security" in response.headers
    assert "max-age=31536000" in response.headers["Strict-Transport-Security"]
    
    assert "Referrer-Policy" in response.headers
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    
    assert "Permissions-Policy" in response.headers

def test_security_headers_on_api_endpoint(client):
    """Test that security headers are present on API endpoints"""
    response = client.get("/api/branches")
    
    assert response.status_code == status.HTTP_200_OK
    
    # Verify headers are present on API endpoints too
    assert "Content-Security-Policy" in response.headers
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "Strict-Transport-Security" in response.headers

def test_csp_header_content(client):
    """Test Content Security Policy header configuration"""
    response = client.get("/")
    
    csp = response.headers["Content-Security-Policy"]
    
    # Verify CSP directives
    assert "default-src 'self'" in csp
    assert "script-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp

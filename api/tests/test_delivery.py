import pytest
from fastapi import status
from unittest.mock import patch, MagicMock
import subprocess
from app.seed_data import deliveries as seed_deliveries

def test_get_all_deliveries(client):
    response = client.get("/api/deliveries")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_deliveries)

def test_create_delivery(client, test_delivery):
    response = client.post("/api/deliveries", json=test_delivery)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_delivery

def test_get_delivery(client):
    # Get first delivery from seed data
    first_delivery = seed_deliveries[0]
    response = client.get(f"/api/deliveries/{first_delivery.deliveryId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["deliveryId"] == first_delivery.deliveryId

def test_get_delivery_not_found(client):
    response = client.get("/api/deliveries/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_delivery(client, test_delivery):
    # First create a delivery
    create_response = client.post("/api/deliveries", json=test_delivery)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the delivery
    updated_delivery = test_delivery.copy()
    updated_delivery["name"] = "Updated Test Delivery"
    response = client.put(f"/api/deliveries/{test_delivery['deliveryId']}", json=updated_delivery)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Test Delivery"

def test_update_delivery_not_found(client, test_delivery):
    response = client.put("/api/deliveries/99999", json=test_delivery)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_delivery(client, test_delivery):
    # First create a delivery
    create_response = client.post("/api/deliveries", json=test_delivery)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the delivery
    response = client.delete(f"/api/deliveries/{test_delivery['deliveryId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify delivery is deleted
    get_response = client.get(f"/api/deliveries/{test_delivery['deliveryId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_delivery_not_found(client):
    response = client.delete("/api/deliveries/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Security Tests for Command Injection Prevention

def test_update_delivery_status_without_command(client):
    """Test status update without notifyCommand"""
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["delivery"]["status"] == "delivered"
    assert "commandOutput" not in response.json()

@patch('subprocess.run')
def test_update_delivery_status_with_allowed_command(mock_run, client):
    """Test status update with whitelisted command"""
    mock_run.return_value = MagicMock(stdout="Command executed", stderr="", returncode=0)
    
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "echo 'Delivery completed'"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["delivery"]["status"] == "delivered"
    assert "commandOutput" in response.json()
    
    # Verify subprocess.run was called without shell=True
    mock_run.assert_called_once()
    call_args = mock_run.call_args
    assert call_args[1].get('capture_output') == True
    assert call_args[1].get('text') == True
    assert call_args[1].get('timeout') == 30
    # Verify shell=True is NOT in the call
    assert 'shell' not in call_args[1] or call_args[1].get('shell') == False

def test_update_delivery_status_with_disallowed_command(client):
    """Test that disallowed commands are rejected - prevents command injection"""
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "rm -rf /"  # Malicious command
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not allowed" in response.json()["detail"].lower()

def test_update_delivery_status_with_shell_injection_attempt(client):
    """Test that shell injection attempts are prevented"""
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "echo test && cat /etc/passwd"  # Shell injection attempt
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    # This is SAFE: '&&' becomes an argument to echo, not a shell operator (no shell=True)
    # The command executes successfully but just echoes the text, doesn't execute cat
    assert response.status_code == status.HTTP_200_OK
    # Verify that the output is just the echo output, not the passwd file
    assert "commandOutput" in response.json()
    # The output should be "test && cat /etc/passwd" (echo just prints its arguments)
    output = response.json()["commandOutput"]
    assert "root:" not in output  # Should NOT contain passwd file contents

def test_update_delivery_status_with_empty_command(client):
    """Test that empty commands are safely handled"""
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": ""
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    # Empty string is falsy, so the command block is skipped - this is safe behavior
    assert response.status_code == status.HTTP_200_OK
    assert "commandOutput" not in response.json()
    assert response.json()["delivery"]["status"] == "delivered"

@patch('subprocess.run')
def test_update_delivery_status_command_timeout(mock_run, client):
    """Test that command execution timeout is handled"""
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=30)
    
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "echo test"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_408_REQUEST_TIMEOUT
    assert "timeout" in response.json()["detail"].lower()

def test_update_delivery_status_delivery_not_found(client):
    """Test status update for non-existent delivery"""
    status_update = {
        "status": "delivered",
        "notifyCommand": "echo test"
    }
    response = client.put("/api/deliveries/99999/status", json=status_update)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@patch('subprocess.run')
def test_update_delivery_status_with_command_error(mock_run, client):
    """Test handling of command execution errors"""
    mock_run.return_value = MagicMock(
        stdout="", 
        stderr="Error occurred", 
        returncode=1
    )
    
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "echo test"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    assert "commandError" in response.json()
    assert response.json()["commandError"] == "Error occurred"

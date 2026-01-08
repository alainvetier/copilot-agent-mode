import pytest
from fastapi import status
from unittest.mock import patch, MagicMock
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

# Test status update functionality (the critical high-risk path)
def test_update_delivery_status_without_command(client):
    # Get first delivery from seed data
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["delivery"]["status"] == "delivered"
    assert "commandOutput" not in response.json()

def test_update_delivery_status_not_found(client):
    status_update = {
        "status": "delivered"
    }
    response = client.put("/api/deliveries/99999/status", json=status_update)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@patch('subprocess.run')
def test_update_delivery_status_with_command_success(mock_run, client):
    # Mock successful command execution
    mock_result = MagicMock()
    mock_result.stdout = "Notification sent successfully"
    mock_run.return_value = mock_result
    
    # Get first delivery from seed data
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "echo 'test notification'"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["delivery"]["status"] == "delivered"
    assert response.json()["commandOutput"] == "Notification sent successfully"
    
    # Verify subprocess.run was called with correct parameters
    mock_run.assert_called_once_with(
        "echo 'test notification'",
        shell=True,
        capture_output=True,
        text=True
    )

@patch('subprocess.run')
def test_update_delivery_status_with_command_exception(mock_run, client):
    # Mock command execution failure
    mock_run.side_effect = Exception("Command execution failed")
    
    # Get first delivery from seed data
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "invalid_command"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Command execution failed" in response.json()["detail"]

@patch('subprocess.run')
def test_update_delivery_status_with_failing_command(mock_run, client):
    # Mock command that returns non-zero exit code with error output
    mock_result = MagicMock()
    mock_result.stdout = "Error: command not found"
    mock_result.returncode = 1
    mock_run.return_value = mock_result
    
    # Get first delivery from seed data
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "delivered",
        "notifyCommand": "nonexistent_command"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    # Even if command fails, the API should still return the output
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["delivery"]["status"] == "delivered"
    assert "Error: command not found" in response.json()["commandOutput"]

@patch('subprocess.run')
def test_update_delivery_status_with_empty_command_output(mock_run, client):
    # Mock command with empty output
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_run.return_value = mock_result
    
    # Get first delivery from seed data
    first_delivery = seed_deliveries[0]
    status_update = {
        "status": "in-transit",
        "notifyCommand": "true"
    }
    response = client.put(f"/api/deliveries/{first_delivery.deliveryId}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["delivery"]["status"] == "in-transit"
    assert response.json()["commandOutput"] == ""

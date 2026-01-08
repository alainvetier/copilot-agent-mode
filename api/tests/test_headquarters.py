import pytest
from fastapi import status
from app.seed_data import headquarters as seed_headquarters

def test_get_all_headquarters(client):
    response = client.get("/api/headquarters")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_headquarters)

def test_create_headquarters(client, test_headquarters):
    response = client.post("/api/headquarters", json=test_headquarters)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_headquarters

def test_get_headquarters(client):
    # Get first headquarters from seed data
    first_hq = seed_headquarters[0]
    response = client.get(f"/api/headquarters/{first_hq.headquartersId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["headquartersId"] == first_hq.headquartersId

def test_get_headquarters_not_found(client):
    response = client.get("/api/headquarters/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_headquarters(client, test_headquarters):
    # First create a headquarters
    create_response = client.post("/api/headquarters", json=test_headquarters)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the headquarters
    updated_hq = test_headquarters.copy()
    updated_hq["name"] = "Updated Test HQ"
    response = client.put(f"/api/headquarters/{test_headquarters['headquartersId']}", json=updated_hq)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Test HQ"

def test_update_headquarters_not_found(client, test_headquarters):
    response = client.put("/api/headquarters/99999", json=test_headquarters)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_headquarters(client, test_headquarters):
    # First create a headquarters
    create_response = client.post("/api/headquarters", json=test_headquarters)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the headquarters
    response = client.delete(f"/api/headquarters/{test_headquarters['headquartersId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify headquarters is deleted
    get_response = client.get(f"/api/headquarters/{test_headquarters['headquartersId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_headquarters_not_found(client):
    response = client.delete("/api/headquarters/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

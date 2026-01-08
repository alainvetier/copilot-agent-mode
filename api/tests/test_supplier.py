import pytest
from fastapi import status
from app.seed_data import suppliers as seed_suppliers

def test_get_all_suppliers(client):
    response = client.get("/api/suppliers")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_suppliers)

def test_create_supplier(client, test_supplier):
    response = client.post("/api/suppliers", json=test_supplier)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_supplier

def test_get_supplier(client):
    # Get first supplier from seed data
    first_supplier = seed_suppliers[0]
    response = client.get(f"/api/suppliers/{first_supplier.supplierId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["supplierId"] == first_supplier.supplierId

def test_get_supplier_not_found(client):
    response = client.get("/api/suppliers/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_supplier(client, test_supplier):
    # First create a supplier
    create_response = client.post("/api/suppliers", json=test_supplier)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the supplier
    updated_supplier = test_supplier.copy()
    updated_supplier["name"] = "Updated Test Supplier"
    response = client.put(f"/api/suppliers/{test_supplier['supplierId']}", json=updated_supplier)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Test Supplier"

def test_update_supplier_not_found(client, test_supplier):
    response = client.put("/api/suppliers/99999", json=test_supplier)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_supplier(client, test_supplier):
    # First create a supplier
    create_response = client.post("/api/suppliers", json=test_supplier)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the supplier
    response = client.delete(f"/api/suppliers/{test_supplier['supplierId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify supplier is deleted
    get_response = client.get(f"/api/suppliers/{test_supplier['supplierId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_supplier_not_found(client):
    response = client.delete("/api/suppliers/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

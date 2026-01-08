import pytest
from fastapi import status
from app.seed_data import orders as seed_orders

def test_get_all_orders(client):
    response = client.get("/api/orders")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_orders)

def test_create_order(client, test_order):
    response = client.post("/api/orders", json=test_order)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_order

def test_get_order(client):
    # Get first order from seed data
    first_order = seed_orders[0]
    response = client.get(f"/api/orders/{first_order.orderId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["orderId"] == first_order.orderId

def test_get_order_not_found(client):
    response = client.get("/api/orders/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_order(client, test_order):
    # First create an order
    create_response = client.post("/api/orders", json=test_order)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the order
    updated_order = test_order.copy()
    updated_order["name"] = "Updated Test Order"
    response = client.put(f"/api/orders/{test_order['orderId']}", json=updated_order)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Test Order"

def test_update_order_not_found(client, test_order):
    response = client.put("/api/orders/99999", json=test_order)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_order(client, test_order):
    # First create an order
    create_response = client.post("/api/orders", json=test_order)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the order
    response = client.delete(f"/api/orders/{test_order['orderId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify order is deleted
    get_response = client.get(f"/api/orders/{test_order['orderId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_order_not_found(client):
    response = client.delete("/api/orders/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

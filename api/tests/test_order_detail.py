import pytest
from fastapi import status
from app.seed_data import order_details as seed_order_details

def test_get_all_order_details(client):
    response = client.get("/api/order-details")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_order_details)

def test_create_order_detail(client, test_order_detail):
    response = client.post("/api/order-details", json=test_order_detail)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_order_detail

def test_get_order_detail(client):
    # Get first order detail from seed data
    first_detail = seed_order_details[0]
    response = client.get(f"/api/order-details/{first_detail.orderDetailId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["orderDetailId"] == first_detail.orderDetailId

def test_get_order_detail_not_found(client):
    response = client.get("/api/order-details/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_order_detail(client, test_order_detail):
    # First create an order detail
    create_response = client.post("/api/order-details", json=test_order_detail)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the order detail
    updated_detail = test_order_detail.copy()
    updated_detail["quantity"] = 20
    response = client.put(f"/api/order-details/{test_order_detail['orderDetailId']}", json=updated_detail)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 20

def test_update_order_detail_not_found(client, test_order_detail):
    response = client.put("/api/order-details/99999", json=test_order_detail)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_order_detail(client, test_order_detail):
    # First create an order detail
    create_response = client.post("/api/order-details", json=test_order_detail)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the order detail
    response = client.delete(f"/api/order-details/{test_order_detail['orderDetailId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify order detail is deleted
    get_response = client.get(f"/api/order-details/{test_order_detail['orderDetailId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_order_detail_not_found(client):
    response = client.delete("/api/order-details/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

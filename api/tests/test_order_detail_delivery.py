import pytest
from fastapi import status
from app.seed_data import order_detail_deliveries as seed_order_detail_deliveries

def test_get_all_order_detail_deliveries(client):
    response = client.get("/api/order-detail-deliveries")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_order_detail_deliveries)

def test_create_order_detail_delivery(client, test_order_detail_delivery):
    response = client.post("/api/order-detail-deliveries", json=test_order_detail_delivery)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_order_detail_delivery

def test_get_order_detail_delivery(client):
    # Get first order detail delivery from seed data
    first_odd = seed_order_detail_deliveries[0]
    response = client.get(f"/api/order-detail-deliveries/{first_odd.orderDetailDeliveryId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["orderDetailDeliveryId"] == first_odd.orderDetailDeliveryId

def test_get_order_detail_delivery_not_found(client):
    response = client.get("/api/order-detail-deliveries/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_order_detail_delivery(client, test_order_detail_delivery):
    # First create an order detail delivery
    create_response = client.post("/api/order-detail-deliveries", json=test_order_detail_delivery)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the order detail delivery
    updated_odd = test_order_detail_delivery.copy()
    updated_odd["quantity"] = 15
    response = client.put(f"/api/order-detail-deliveries/{test_order_detail_delivery['orderDetailDeliveryId']}", json=updated_odd)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 15

def test_update_order_detail_delivery_not_found(client, test_order_detail_delivery):
    response = client.put("/api/order-detail-deliveries/99999", json=test_order_detail_delivery)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_order_detail_delivery(client, test_order_detail_delivery):
    # First create an order detail delivery
    create_response = client.post("/api/order-detail-deliveries", json=test_order_detail_delivery)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the order detail delivery
    response = client.delete(f"/api/order-detail-deliveries/{test_order_detail_delivery['orderDetailDeliveryId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify order detail delivery is deleted
    get_response = client.get(f"/api/order-detail-deliveries/{test_order_detail_delivery['orderDetailDeliveryId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_order_detail_delivery_not_found(client):
    response = client.delete("/api/order-detail-deliveries/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

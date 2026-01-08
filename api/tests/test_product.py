import pytest
from fastapi import status
from app.seed_data import products as seed_products

def test_get_all_products(client):
    response = client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_products)

def test_create_product(client, test_product):
    response = client.post("/api/products", json=test_product)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_product

def test_get_product(client):
    # Get first product from seed data
    first_product = seed_products[0]
    response = client.get(f"/api/products/{first_product.productId}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["productId"] == first_product.productId

def test_get_product_not_found(client):
    response = client.get("/api/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_product(client, test_product):
    # First create a product
    create_response = client.post("/api/products", json=test_product)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Update the product
    updated_product = test_product.copy()
    updated_product["name"] = "Updated Test Product"
    response = client.put(f"/api/products/{test_product['productId']}", json=updated_product)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Test Product"

def test_update_product_not_found(client, test_product):
    response = client.put("/api/products/99999", json=test_product)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_product(client, test_product):
    # First create a product
    create_response = client.post("/api/products", json=test_product)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Delete the product
    response = client.delete(f"/api/products/{test_product['productId']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify product is deleted
    get_response = client.get(f"/api/products/{test_product['productId']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_product_not_found(client):
    response = client.delete("/api/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routes import branch, delivery, headquarters, order, order_detail, order_detail_delivery, product, supplier

@pytest.fixture(autouse=True)
def reset_branch_data():
    # Reset branch data before each test
    branch.branches = branch.branches.copy()
    yield
    # Reset after test
    branch.branches = list(branch.seed_branches)

@pytest.fixture(autouse=True)
def reset_delivery_data():
    # Reset delivery data before each test
    delivery.deliveries = delivery.deliveries.copy()
    yield
    # Reset after test
    delivery.deliveries = list(delivery.seed_deliveries)

@pytest.fixture(autouse=True)
def reset_headquarters_data():
    # Reset headquarters data before each test
    headquarters.headquarters = headquarters.headquarters.copy()
    yield
    # Reset after test
    headquarters.headquarters = list(headquarters.seed_headquarters)

@pytest.fixture(autouse=True)
def reset_order_data():
    # Reset order data before each test
    order.orders = order.orders.copy()
    yield
    # Reset after test
    order.orders = list(order.seed_orders)

@pytest.fixture(autouse=True)
def reset_order_detail_data():
    # Reset order detail data before each test
    order_detail.order_details = order_detail.order_details.copy()
    yield
    # Reset after test
    order_detail.order_details = list(order_detail.seed_order_details)

@pytest.fixture(autouse=True)
def reset_order_detail_delivery_data():
    # Reset order detail delivery data before each test
    order_detail_delivery.order_detail_deliveries = order_detail_delivery.order_detail_deliveries.copy()
    yield
    # Reset after test
    order_detail_delivery.order_detail_deliveries = list(order_detail_delivery.seed_order_detail_deliveries)

@pytest.fixture(autouse=True)
def reset_product_data():
    # Reset product data before each test
    product.products = product.products.copy()
    yield
    # Reset after test
    product.products = list(product.seed_products)

@pytest.fixture(autouse=True)
def reset_supplier_data():
    # Reset supplier data before each test
    supplier.suppliers = supplier.suppliers.copy()
    yield
    # Reset after test
    supplier.suppliers = list(supplier.seed_suppliers)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_branch():
    return {
        "branchId": 999,
        "headquartersId": 1,
        "name": "Test Branch",
        "description": "Test branch for unit tests",
        "address": "123 Test St",
        "contactPerson": "Test Person",
        "email": "test@example.com",
        "phone": "555-0123"
    }

@pytest.fixture
def test_delivery():
    return {
        "deliveryId": 999,
        "supplierId": 1,
        "deliveryDate": "2026-02-01T00:00:00",
        "name": "Test Delivery",
        "description": "Test delivery for unit tests",
        "status": "pending"
    }

@pytest.fixture
def test_headquarters():
    return {
        "headquartersId": 999,
        "name": "Test Headquarters",
        "description": "Test headquarters for unit tests",
        "address": "123 Test Ave",
        "contactPerson": "Test Manager",
        "email": "test@testcorp.com",
        "phone": "555-0999"
    }

@pytest.fixture
def test_order():
    return {
        "orderId": 999,
        "branchId": 1,
        "orderDate": "2026-02-01T00:00:00",
        "name": "Test Order",
        "description": "Test order for unit tests",
        "status": "pending"
    }

@pytest.fixture
def test_order_detail():
    return {
        "orderDetailId": 999,
        "orderId": 1,
        "productId": 1,
        "quantity": 10,
        "unitPrice": 99.99,
        "notes": "Test order detail"
    }

@pytest.fixture
def test_order_detail_delivery():
    return {
        "orderDetailDeliveryId": 999,
        "orderDetailId": 1,
        "deliveryId": 1,
        "quantity": 5,
        "notes": "Test order detail delivery"
    }

@pytest.fixture
def test_product():
    return {
        "productId": 999,
        "supplierId": 1,
        "name": "Test Product",
        "description": "Test product for unit tests",
        "price": 49.99,
        "sku": "TEST-001",
        "unit": "piece",
        "imgName": "test-product.png",
        "discount": None
    }

@pytest.fixture
def test_supplier():
    return {
        "supplierId": 999,
        "name": "Test Supplier",
        "description": "Test supplier for unit tests",
        "contactPerson": "Test Contact",
        "email": "contact@testsupplier.com",
        "phone": "555-0888"
    }
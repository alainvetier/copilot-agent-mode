import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routes import branch, delivery  # Import the route modules to access their state

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
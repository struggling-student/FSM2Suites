import pytest
from fastapi.testclient import TestClient
from main import app, sessions, carts, products_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def clean_data():
    # Clear data before each test
    sessions.clear()
    carts.clear()
    yield
    # Clean up after test
    sessions.clear()
    carts.clear()

class TestLogin:
    def test_successful_login(self, client, clean_data):
        response = client.post("/login", json={
            "email": "test@example.com",
            "password": "password123"  # Correct password from API
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "token" in data
        assert data["user"]["email"] == "test@example.com"

    def test_failed_login_invalid_credentials(self, client, clean_data):
        response = client.post("/login", json={
            "email": "invalid@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "Invalid email or password" in data["message"]

    def test_login_missing_fields(self, client, clean_data):
        response = client.post("/login", json={
            "email": "test@example.com"
            # missing password
        })
        assert response.status_code == 422  # Validation error

class TestProducts:
    def test_get_products(self, client, clean_data):
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert len(data["products"]) == len(products_db)
        
        # Check first product structure
        product = data["products"][0]
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "price" in product

class TestCart:
    def test_add_to_cart_without_session(self, client, clean_data):
        response = client.post("/cart/add", json={
            "id": 1,
            "quantity": 2
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_add_invalid_product_to_cart(self, client, clean_data):
        response = client.post("/cart/add", json={
            "id": 999,  # Non-existent product
            "quantity": 1
        })
        assert response.status_code == 404
        data = response.json()
        assert "Product not found" in data["detail"]

    def test_add_zero_quantity(self, client, clean_data):
        response = client.post("/cart/add", json={
            "id": 1,
            "quantity": 0
        })
        # API allows zero quantity (doesn't validate it)
        assert response.status_code == 200

    def test_get_empty_cart(self, client, clean_data):
        response = client.get("/cart")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0.0

    def test_cart_workflow(self, client, clean_data):
        # Add item to cart
        response = client.post("/cart/add", json={
            "id": 1,
            "quantity": 2
        })
        assert response.status_code == 200

        # Get cart
        response = client.get("/cart")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 2
        assert data["total"] > 0

        # Update cart item
        response = client.post("/cart/update", json={
            "id": 1,
            "quantity": 3
        })
        assert response.status_code == 200

        # Verify update
        response = client.get("/cart")
        data = response.json()
        assert data["items"][0]["quantity"] == 3

        # Remove from cart
        response = client.post("/cart/remove", json={
            "id": 1
        })
        assert response.status_code == 200

        # Verify removal
        response = client.get("/cart")
        data = response.json()
        assert len(data["items"]) == 0

class TestCheckout:
    def test_start_checkout_empty_cart(self, client, clean_data):
        response = client.post("/checkout/start")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "Cart is empty" in data["message"]

    def test_checkout_workflow(self, client, clean_data):
        # Add item to cart first
        client.post("/cart/add", json={
            "id": 1,
            "quantity": 1
        })

        # Start checkout
        response = client.post("/checkout/start")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Payment success
        response = client.post("/checkout/pay", json={
            "forceSuccess": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_payment_failure(self, client, clean_data):
        # Add item to cart first
        client.post("/cart/add", json={
            "id": 1,
            "quantity": 1
        })

        # Start checkout
        client.post("/checkout/start")

        # Payment failure
        response = client.post("/checkout/pay", json={
            "forceSuccess": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False

    def test_cancel_checkout(self, client, clean_data):
        # Add item to cart first
        client.post("/cart/add", json={
            "id": 1,
            "quantity": 1
        })

        # Start checkout
        client.post("/checkout/start")

        # Cancel checkout
        response = client.post("/checkout/cancel")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

class TestLogout:
    def test_logout(self, client, clean_data):
        # Login first
        client.post("/login", json={
            "email": "test@example.com",
            "password": "password"
        })

        # Logout
        response = client.post("/logout")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

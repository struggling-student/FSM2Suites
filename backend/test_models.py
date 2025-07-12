import pytest
from pydantic import ValidationError
from main import LoginRequest, CartAddRequest, Product

class TestModels:
    def test_login_request_valid(self):
        request = LoginRequest(email="test@example.com", password="password123")
        assert request.email == "test@example.com"
        assert request.password == "password123"

    def test_login_request_accepts_any_email_format(self):
        # The model doesn't validate email format, just requires a string
        request = LoginRequest(email="invalid-email", password="password123")
        assert request.email == "invalid-email"

    def test_cart_add_request_valid(self):
        request = CartAddRequest(id=1, quantity=2)
        assert request.id == 1
        assert request.quantity == 2

    def test_cart_add_request_negative_quantity(self):
        # This should be caught by the API logic, not pydantic validation
        request = CartAddRequest(id=1, quantity=-1)
        assert request.quantity == -1

    def test_product_model(self):
        product = Product(
            id=1,
            name="Test Product",
            description="A test product",
            price=99.99
        )
        assert product.id == 1
        assert product.name == "Test Product"
        assert product.price == 99.99

    def test_product_model_invalid_price(self):
        with pytest.raises(ValidationError):
            Product(
                id=1,
                name="Test Product",
                description="A test product",
                price="invalid_price"  # Should be float
            )

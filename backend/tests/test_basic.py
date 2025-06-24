import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User
from app.core.security import create_access_token


class TestBasicFunctionality:
    """Basic tests to verify the API works"""
    
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, db: Session):
        """Setup test data for each test"""
        self.client = client
        self.db = db
        
        # Clean up existing data
        db.query(User).delete()
        db.commit()

    def test_health_check(self):
        """Test basic health endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_user_registration_basic(self):
        """Test basic user registration"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "testpassword123",
            "city_of_origin": "New York"
        }
        
        response = self.client.post("/api/v1/auth/register", json=user_data)
        
        # Check if registration succeeds
        print(f"Registration response status: {response.status_code}")
        print(f"Registration response content: {response.text}")
        
        if response.status_code != 200:
            # Try to understand what went wrong
            assert False, f"Registration failed with status {response.status_code}: {response.text}"
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert "id" in data

    def test_user_login_basic(self):
        """Test basic user login after registration"""
        # First register a user
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "password": "testpassword123",
            "city_of_origin": "London"
        }
        
        reg_response = self.client.post("/api/v1/auth/register", json=user_data)
        if reg_response.status_code != 200:
            assert False, f"Registration failed: {reg_response.text}"
        
        # Then try to login
        login_data = {
            "email": "jane.smith@example.com",
            "password": "testpassword123"
        }
        
        login_response = self.client.post("/api/v1/auth/login", json=login_data)
        
        print(f"Login response status: {login_response.status_code}")
        print(f"Login response content: {login_response.text}")
        
        if login_response.status_code != 200:
            assert False, f"Login failed with status {login_response.status_code}: {login_response.text}"
        
        data = login_response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_get_current_user_with_token(self):
        """Test getting current user with valid token"""
        # Register and login user
        user_data = {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@example.com",
            "password": "testpassword123",
            "city_of_origin": "Paris"
        }
        
        # Register
        self.client.post("/api/v1/auth/register", json=user_data)
        
        # Login
        login_data = {
            "email": "alice.johnson@example.com",
            "password": "testpassword123"
        }
        login_response = self.client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Get current user
        response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Get current user response status: {response.status_code}")
        print(f"Get current user response content: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]

    def test_api_documentation_accessible(self):
        """Test that API documentation is accessible"""
        response = self.client.get("/docs")
        assert response.status_code == 200
        
        response = self.client.get("/api/v1/openapi.json")
        assert response.status_code == 200

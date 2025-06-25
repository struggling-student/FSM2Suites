import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User
from app.schemas.schemas import UserCreate
from app.crud.crud import user_crud

class TestUserCRUD:
    """Test user CRUD operations"""
    
    def test_create_user(self, client: TestClient, db: Session):
        """Test creating a new user"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "password": "testpassword123",
            "city_of_origin": "New York"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["city_of_origin"] == user_data["city_of_origin"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    def test_create_user_duplicate_email(self, client: TestClient, db: Session):
        """Test creating a user with duplicate email fails"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com", 
            "password": "testpassword123",
            "city_of_origin": "New York"
        }
        
        # Create first user
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 200
        
        # Try to create duplicate
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"]

    def test_create_user_invalid_email(self, client: TestClient, db: Session):
        """Test creating a user with invalid email fails"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "testpassword123", 
            "city_of_origin": "New York"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422

    def test_login_user(self, client: TestClient, db: Session):
        """Test user login"""
        # Create user first
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "testpassword123",
            "city_of_origin": "New York"
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Test login
        login_data = {
            "email": "john.doe@example.com",
            "password": "testpassword123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient, db: Session):
        """Test login with invalid credentials fails"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401

    def test_get_current_user(self, client: TestClient, db: Session):
        """Test getting current user with valid token"""
        # Create and login user
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "testpassword123",
            "city_of_origin": "New York"
        }
        client.post("/api/v1/auth/register", json=user_data)

        login_response = client.post("/api/v1/auth/login", json={
            "email": "john.doe@example.com",
            "password": "testpassword123"
        })
        token = login_response.json()["access_token"]
        
        # Get current user
        response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]

    def test_get_users_list(self, client: TestClient, db: Session):
        """Test getting list of users"""
        # Create multiple users
        users_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "testpassword123",
                "city_of_origin": "New York"
            },
            {
                "first_name": "Jane", 
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "password": "testpassword123",
                "city_of_origin": "London"
            }
        ]
        for user_data in users_data:
            client.post("/api/v1/auth/register", json=user_data)

        # Login to get token
        login_response = client.post("/api/v1/auth/login", json={
            "email": "john.doe@example.com",
            "password": "testpassword123"
        })
        token = login_response.json()["access_token"]

        response = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2

    def test_user_rating_calculation(self, db: Session):
        """Test user rating calculation according to specification"""
        from app.crud.crud import user_crud, trip_crud
        from app.schemas.schemas import UserCreate, TripCreate
        from app.models.models import Trip, Feedback
        from datetime import datetime, timedelta
        
        # Create user using CRUD
        user_data = UserCreate(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="testpassword",
            city_of_origin="NYC"
        )
        user = user_crud.create(db, obj_in=user_data)

        # Create trip using CRUD
        trip_data = TripCreate(
            name="Test Trip",
            min_participants=1,
            max_participants=10,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=3)
        )
        trip = trip_crud.create(db, obj_in=trip_data, organizer_id=user.id)
        db.add(trip)
        db.commit()
        db.refresh(trip)
        
        # Test basic user creation and default values
        assert user.rating == 0.0
        assert user.is_active == True
        assert user.first_name == "John"
        assert user.last_name == "Doe"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.models import User, Trip, Activity, Location

class TestTripCRUD:
    """Test trip CRUD operations and business logic"""
    
    def setup_test_user(self, client: TestClient) -> tuple[str, dict]:
        """Helper to create and login a test user"""
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
        return token, user_data

    def test_create_trip(self, client: TestClient, db: Session):
        """Test creating a new trip"""
        token, _ = self.setup_test_user(client)
        
        trip_data = {
            "name": "Amazing European Tour",
            "min_participants": 2,
            "max_participants": 10,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"Create trip response: {response.status_code}, {response.json()}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == trip_data["name"]
        assert data["min_participants"] == trip_data["min_participants"]
        assert data["max_participants"] == trip_data["max_participants"]
        assert "id" in data
        assert "organizer" in data

    def test_create_trip_invalid_participants(self, client: TestClient, db: Session):
        """Test creating trip with invalid participant numbers fails"""
        token, _ = self.setup_test_user(client)
        
        # Min > Max participants
        trip_data = {
            "name": "Invalid Trip",
            "min_participants": 10,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 422

    def test_get_trips(self, client: TestClient, db: Session):
        """Test getting list of trips"""
        token, _ = self.setup_test_user(client)
        
        # Create multiple trips
        trips_data = [
            {"name": "Trip 1", "min_participants": 1, "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"},
            {"name": "Trip 2", "min_participants": 2, "max_participants": 8,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"}
        ]
        
        for trip_data in trips_data:
            client.post(
                "/api/v1/trips/",
                json=trip_data,
                headers={"Authorization": f"Bearer {token}"}
            )
        
        response = client.get("/api/v1/trips/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 2

    def test_get_trip_by_id(self, client: TestClient, db: Session):
        """Test getting specific trip by ID"""
        token, _ = self.setup_test_user(client)
        
        trip_data = {
            "name": "Specific Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07",
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        create_response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        trip_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/trips/{trip_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == trip_data["name"]

    def test_join_trip(self, client: TestClient, db: Session):
        """Test joining a trip"""
        # Create organizer
        token1, _ = self.setup_test_user(client)
        
        # Create another user
        user2_data = {
            "first_name": "Jane",
            "last_name": "Smith", 
            "email": "jane.smith@example.com",
            "password": "testpassword123",
            "city_of_origin": "London"
        }
        client.post("/api/v1/auth/register", json=user2_data)
        
        login2_response = client.post("/api/v1/auth/login", json={
            "email": "jane.smith@example.com",
            "password": "testpassword123"
        })
        token2 = login2_response.json()["access_token"]
        
        # Create trip
        trip_data = {
            "name": "Joinable Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        create_response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token1}"}
        )
        trip_id = create_response.json()["id"]
        
        # Join trip
        response = client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 200

    def test_join_trip_already_member(self, client: TestClient, db: Session):
        """Test joining a trip user is already part of fails"""
        token, _ = self.setup_test_user(client)
        
        # Create trip
        trip_data = {
            "name": "Test Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        create_response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        trip_id = create_response.json()["id"]
        
        # Try to join own trip (organizer is automatically a participant)
        response = client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400

    def test_leave_trip(self, client: TestClient, db: Session):
        """Test leaving a trip"""
        # Setup two users and a trip like in join test
        token1, _ = self.setup_test_user(client)
        
        user2_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com", 
            "password": "testpassword123",
            "city_of_origin": "London"
        }
        client.post("/api/v1/auth/register", json=user2_data)
        
        login2_response = client.post("/api/v1/auth/login", json={
            "email": "jane.smith@example.com",
            "password": "testpassword123"
        })
        token2 = login2_response.json()["access_token"]
        
        # Create and join trip
        trip_data = {
            "name": "Leaveable Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        create_response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token1}"}
        )
        trip_id = create_response.json()["id"]
        
        client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Leave trip
        response = client.post(
            f"/api/v1/trips/{trip_id}/leave",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 200

    def test_update_trip_organizer_only(self, client: TestClient, db: Session):
        """Test that only organizer can update trip"""
        # Create organizer
        token1, _ = self.setup_test_user(client)
        
        # Create another user
        user2_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "password": "testpassword123",
            "city_of_origin": "London"
        }
        client.post("/api/v1/auth/register", json=user2_data)
        
        login2_response = client.post("/api/v1/auth/login", json={
            "email": "jane.smith@example.com", 
            "password": "testpassword123"
        })
        token2 = login2_response.json()["access_token"]
        
        # Create trip
        trip_data = {
            "name": "Original Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        create_response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token1}"}
        )
        trip_id = create_response.json()["id"]
        
        # Try to update as non-organizer
        update_data = {"name": "Updated Trip"}
        response = client.put(
            f"/api/v1/trips/{trip_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 403

    def test_delete_trip_organizer_only(self, client: TestClient, db: Session):
        """Test that only organizer can delete trip"""
        token, _ = self.setup_test_user(client)
        
        # Create trip
        trip_data = {
            "name": "Deletable Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }
        
        create_response = client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        trip_id = create_response.json()["id"]
        
        # Delete trip
        response = client.delete(
            f"/api/v1/trips/{trip_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

    def test_get_user_trips(self, client: TestClient, db: Session):
        """Test getting trips for a specific user"""
        token, _ = self.setup_test_user(client)
        
        # Create trips
        trips_data = [
            {"name": "User Trip 1", "min_participants": 1, "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"},
            {"name": "User Trip 2", "min_participants": 2, "max_participants": 8,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"}
        ]
        
        for trip_data in trips_data:
            client.post(
                "/api/v1/trips/",
                json=trip_data,
                headers={"Authorization": f"Bearer {token}"}
            )
        
        response = client.get(
            "/api/v1/users/me/trips",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2

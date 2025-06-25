import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User, Trip, Location
from app.core.security import create_access_token


class TestTripFunctionality:
    """Test trip-related functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, db: Session):
        """Setup test data for each test"""
        self.client = client
        self.db = db
        
        # Clean up existing data
        db.query(Trip).delete()
        db.query(User).delete()
        db.query(Location).delete()
        db.commit()
        
        # Create test location using CRUD to properly generate ID
        from app.crud.crud import location_crud
        from app.schemas.schemas import LocationCreate
        
        location_data = LocationCreate(
            address="123 Test St",
            city="Test City",
            region="Test Region",
            country="Test Country"
        )
        self.location = location_crud.create(db, obj_in=location_data)

    def create_and_login_user(self, email: str, first_name: str = "Test", last_name: str = "User") -> tuple[str, dict]:
        """Helper to create and login a user, returns (token, user_data)"""
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": "testpassword123",
            "city_of_origin": "Test City"
        }
        
        # Register user
        reg_response = self.client.post("/api/v1/auth/register", json=user_data)
        assert reg_response.status_code == 200
        user_info = reg_response.json()
        
        # Login user
        login_data = {
            "email": email,
            "password": "testpassword123"
        }
        login_response = self.client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        return token, user_info

    def test_create_trip_success(self):
        """Test successful trip creation"""
        token, user_info = self.create_and_login_user("organizer@test.com", "Trip", "Organizer")
        
        trip_data = {
            "name": "Amazing Paris Adventure",
            "min_participants": 2,
            "max_participants": 8,
            "start_date": "2024-07-01T09:00:00",
            "end_date": "2024-07-07T18:00:00"
        }
        
        response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Trip creation response status: {response.status_code}")
        print(f"Trip creation response content: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == trip_data["name"]
        assert data["min_participants"] == trip_data["min_participants"]
        assert data["max_participants"] == trip_data["max_participants"]
        assert "id" in data

    def test_create_trip_unauthorized(self):
        """Test trip creation without authentication fails"""
        trip_data = {
            "name": "Unauthorized Trip",
            "min_participants": 2,
            "max_participants": 8,
            "organizer_id": "fake-id"
        }
        
        response = self.client.post("/api/v1/trips/", json=trip_data)
        assert response.status_code == 401

    def test_create_trip_invalid_participants(self):
        """Test trip creation with invalid participant numbers"""
        token, user_info = self.create_and_login_user("organizer2@test.com")
        
        # Test max < min
        invalid_trip_data = {
            "name": "Invalid Trip",
            "min_participants": 5,
            "max_participants": 3,  # Less than min
            "organizer_id": user_info["id"]
        }
        
        response = self.client.post(
            "/api/v1/trips/",
            json=invalid_trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 422  # Validation error

    def test_get_trips_list(self):
        """Test getting list of trips"""
        # Create some trips
        token1, user1 = self.create_and_login_user("user1@test.com")
        token2, user2 = self.create_and_login_user("user2@test.com")

        trips_data = [
            {
                "name": "Trip 1",
                "min_participants": 2,
                "max_participants": 5,
                "start_date": "2024-08-01T09:00:00",
                "end_date": "2024-08-05T18:00:00",
                "token": token1
            },
            {
                "name": "Trip 2",
                "min_participants": 1,
                "max_participants": 10,
                "start_date": "2024-09-01T09:00:00",
                "end_date": "2024-09-10T18:00:00",
                "token": token2
            }
        ]
        
        created_trips = []
        for trip_data in trips_data:
            token = trip_data.pop("token")
            response = self.client.post(
                "/api/v1/trips/",
                json=trip_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            created_trips.append(response.json())
        
        # Get all trips
        response = self.client.get("/api/v1/trips/")
        assert response.status_code == 200

        trips_response = response.json()
        assert trips_response["total"] == 2
        assert len(trips_response["trips"]) == 2
        
        trip_names = [trip["name"] for trip in trips_response["trips"]]
        assert "Trip 1" in trip_names
        assert "Trip 2" in trip_names

    def test_get_trip_by_id(self):
        """Test getting specific trip by ID"""
        token, user_info = self.create_and_login_user("organizer3@test.com")
        
        # Create trip
        trip_data = {
            "name": "Detailed Trip",
            "min_participants": 2,
            "max_participants": 6,
            "start_date": "2024-08-15T09:00:00",
            "end_date": "2024-08-20T18:00:00"
        }
        
        create_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        trip_id = create_response.json()["id"]
        
        # Get trip by ID
        response = self.client.get(f"/api/v1/trips/{trip_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Detailed Trip"
        assert data["id"] == trip_id

    def test_join_trip_success(self):
        """Test successfully joining a trip"""
        # Create organizer and participant
        organizer_token, organizer_info = self.create_and_login_user("organizer4@test.com", "Trip", "Organizer")
        participant_token, participant_info = self.create_and_login_user("participant@test.com", "Trip", "Participant")
        
        # Create trip
        trip_data = {
            "name": "Join Test Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-09-01T09:00:00",
            "end_date": "2024-09-05T18:00:00"
        }
        
        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        trip_id = trip_response.json()["id"]
        
        # Participant joins trip
        response = self.client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {participant_token}"}
        )
        
        assert response.status_code == 200
        
        # Verify participant is in trip
        trip_details = self.client.get(f"/api/v1/trips/{trip_id}")
        trip_data = trip_details.json()
        
        participant_ids = [p["id"] for p in trip_data["participants"]]
        assert participant_info["id"] in participant_ids

    def test_join_trip_already_member(self):
        """Test joining trip user is already part of"""
        organizer_token, organizer_info = self.create_and_login_user("organizer5@test.com")
        participant_token, participant_info = self.create_and_login_user("participant2@test.com")
        
        # Create trip
        trip_data = {
            "name": "Double Join Test",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-09-10T09:00:00",
            "end_date": "2024-09-15T18:00:00"
        }
        
        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        trip_id = trip_response.json()["id"]
        
        # Join first time (should succeed)
        response1 = self.client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {participant_token}"}
        )
        assert response1.status_code == 200
        
        # Try to join again (should fail)
        response2 = self.client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {participant_token}"}
        )
        assert response2.status_code == 400  # Bad Request for duplicate join

    def test_leave_trip_success(self):
        """Test successfully leaving a trip"""
        organizer_token, organizer_info = self.create_and_login_user("organizer6@test.com")
        participant_token, participant_info = self.create_and_login_user("participant3@test.com")
        
        # Create trip and join
        trip_data = {
            "name": "Leave Test Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-09-20T09:00:00",
            "end_date": "2024-09-25T18:00:00"
        }
        
        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        trip_id = trip_response.json()["id"]
        
        # Join trip
        self.client.post(
            f"/api/v1/trips/{trip_id}/join",
            headers={"Authorization": f"Bearer {participant_token}"}
        )
        
        # Leave trip
        response = self.client.post(
            f"/api/v1/trips/{trip_id}/leave",
            headers={"Authorization": f"Bearer {participant_token}"}
        )
        
        assert response.status_code == 200
        
        # Verify participant is no longer in trip
        trip_details = self.client.get(f"/api/v1/trips/{trip_id}")
        trip_data = trip_details.json()
        
        participant_ids = [p["id"] for p in trip_data["participants"]]
        assert participant_info["id"] not in participant_ids

    def test_update_trip_organizer_only(self):
        """Test that only organizer can update trip"""
        organizer_token, organizer_info = self.create_and_login_user("organizer7@test.com")
        other_user_token, other_user_info = self.create_and_login_user("other@test.com")
        
        # Create trip
        trip_data = {
            "name": "Update Test Trip",
            "min_participants": 2,
            "max_participants": 6,
            "start_date": "2024-10-01T09:00:00",
            "end_date": "2024-10-05T18:00:00"
        }
        
        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        trip_id = trip_response.json()["id"]
        
        # Organizer updates trip (should succeed)
        update_data = {
            "name": "Updated Trip Name",
            "max_participants": 8
        }
        
        response = self.client.put(
            f"/api/v1/trips/{trip_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        assert response.status_code == 200
        
        # Other user tries to update (should fail)
        response = self.client.put(
            f"/api/v1/trips/{trip_id}",
            json={"name": "Hacked Name"},
            headers={"Authorization": f"Bearer {other_user_token}"}
        )
        assert response.status_code == 403

    def test_delete_trip_organizer_only(self):
        """Test that only organizer can delete trip"""
        organizer_token, organizer_info = self.create_and_login_user("organizer8@test.com")
        other_user_token, other_user_info = self.create_and_login_user("other2@test.com")
        
        # Create trip
        trip_data = {
            "name": "Delete Test Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-10-10T09:00:00",
            "end_date": "2024-10-15T18:00:00"
        }
        
        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        trip_id = trip_response.json()["id"]
        
        # Other user tries to delete (should fail)
        response = self.client.delete(
            f"/api/v1/trips/{trip_id}",
            headers={"Authorization": f"Bearer {other_user_token}"}
        )
        assert response.status_code == 403
        
        # Organizer deletes trip (should succeed)
        response = self.client.delete(
            f"/api/v1/trips/{trip_id}",
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        assert response.status_code == 200
        
        # Verify trip is deleted
        response = self.client.get(f"/api/v1/trips/{trip_id}")
        assert response.status_code == 404

    def test_get_user_trips(self):
        """Test getting trips for a specific user"""
        user_token, user_info = self.create_and_login_user("user@test.com")
        organizer_token, organizer_info = self.create_and_login_user("organizer9@test.com")
        
        # Create trip organized by user
        organized_trip = {
            "name": "My Organized Trip",
            "min_participants": 2,
            "max_participants": 5,
            "start_date": "2024-10-20T09:00:00",
            "end_date": "2024-10-25T18:00:00"
        }
        
        self.client.post(
            "/api/v1/trips/",
            json=organized_trip,
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        # Create trip organized by someone else and join it
        other_trip = {
            "name": "Someone Else's Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-11-01T09:00:00",
            "end_date": "2024-11-05T18:00:00"
        }
        
        other_trip_response = self.client.post(
            "/api/v1/trips/",
            json=other_trip,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        other_trip_id = other_trip_response.json()["id"]
        
        # Join the other trip
        self.client.post(
            f"/api/v1/trips/{other_trip_id}/join",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        # Get user's trips
        response = self.client.get(
            "/api/v1/auth/me/trips",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == 200
        user_trips = response.json()
        
        # Should include both organized and participated trips
        assert len(user_trips) == 2
        
        trip_names = [trip["name"] for trip in user_trips]
        assert "My Organized Trip" in trip_names
        assert "Someone Else's Trip" in trip_names

    def test_trip_capacity_limits(self):
        """Test that trips respect capacity limits"""
        organizer_token, organizer_info = self.create_and_login_user("organizer10@test.com")
        
        # Create trip with very limited capacity
        trip_data = {
            "name": "Limited Capacity Trip",
            "min_participants": 1,
            "max_participants": 2,  # Only 2 spots
            "start_date": "2024-11-10T09:00:00",
            "end_date": "2024-11-15T18:00:00"
        }
        
        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {organizer_token}"}
        )
        trip_id = trip_response.json()["id"]
        
        # Create participants and try to join
        participants = []
        for i in range(3):  # Try to join 3 people to a 2-person trip
            token, user_info = self.create_and_login_user(f"participant{i}@test.com")
            participants.append((token, user_info))
        
        successful_joins = 0
        for token, user_info in participants:
            response = self.client.post(
                f"/api/v1/trips/{trip_id}/join",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                successful_joins += 1
        
        # Should not exceed capacity
        assert successful_joins <= 2
        
        # Verify by checking trip details
        trip_details = self.client.get(f"/api/v1/trips/{trip_id}")
        trip_data = trip_details.json()
        assert len(trip_data["participants"]) <= 2

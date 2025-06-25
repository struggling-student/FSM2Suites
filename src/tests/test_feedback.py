import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.models import User, Trip, Activity, Location, Feedback
from app.core.security import create_access_token


class TestFeedback:
    
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, db: Session):
        """Setup test data for each test"""
        self.client = client
        self.db = db
        
        # Clean up any existing data
        db.query(Feedback).delete()
        db.query(Activity).delete()
        db.query(Trip).delete()
        db.query(User).delete()
        db.query(Location).delete()
        db.commit()
        
        # Create test users
        self.organizer_data = {
            "first_name": "Jane",
            "last_name": "Organizer",
            "email": "jane@example.com",
            "password": "testpass123",
            "city_of_origin": "London"
        }
        
        self.user1_data = {
            "first_name": "John",
            "last_name": "Participant1",
            "email": "john@example.com",
            "password": "testpass123",
            "city_of_origin": "New York"
        }
        
        self.user2_data = {
            "first_name": "Alice",
            "last_name": "Participant2",
            "email": "alice@example.com",
            "password": "testpass123",
            "city_of_origin": "Paris"
        }
         # Register users
        org_response = self.client.post("/api/v1/auth/register", json=self.organizer_data)
        self.organizer_id = org_response.json()["id"]

        user1_response = self.client.post("/api/v1/auth/register", json=self.user1_data)
        self.user1_id = user1_response.json()["id"]

        user2_response = self.client.post("/api/v1/auth/register", json=self.user2_data)
        self.user2_id = user2_response.json()["id"]

        # Login to get tokens
        org_login = self.client.post("/api/v1/auth/login", json={"email": "jane@example.com", "password": "testpass123"})
        self.organizer_token = org_login.json()["access_token"]
        
        user1_login = self.client.post("/api/v1/auth/login", json={"email": "john@example.com", "password": "testpass123"})
        self.user1_token = user1_login.json()["access_token"]
        
        user2_login = self.client.post("/api/v1/auth/login", json={"email": "alice@example.com", "password": "testpass123"})
        self.user2_token = user2_login.json()["access_token"]
        
        # Create test location
        import uuid
        self.location = Location(
            id=str(uuid.uuid4()),
            address="123 Test St",
            city="Test City",
            region="Test Region",
            country="Test Country"
        )
        db.add(self.location)
        db.commit()
        db.refresh(self.location)
         # Create test trip
        trip_data = {
            "name": "Feedback Test Trip",
            "min_participants": 1,
            "max_participants": 5,
            "start_date": "2024-06-01",
            "end_date": "2024-06-07"
        }

        trip_response = self.client.post(
            "/api/v1/trips/",
            json=trip_data,
            headers={"Authorization": f"Bearer {self.organizer_token}"}
        )
        print(f"Trip creation response: {trip_response.status_code}, {trip_response.json()}")
        self.trip_id = trip_response.json()["id"]
        
        # Users join the trip
        self.client.post(
            f"/api/v1/trips/{self.trip_id}/join",
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        self.client.post(
            f"/api/v1/trips/{self.trip_id}/join",
            headers={"Authorization": f"Bearer {self.user2_token}"}
        )
        
        # Create test activity
        activity_data = {
            "name": "Feedback Test Activity",
            "type": "tour",
            "start_time": "2024-06-01T10:00:00",
            "duration": 120,
            "price": 25.00,
            "location": {
                "address": self.location.address,
                "city": self.location.city,
                "region": self.location.region,
                "country": self.location.country
            },
            "description": "Activity for feedback testing"
        }
        
        activity_response = self.client.post(
            f"/api/v1/activities/trip/{self.trip_id}",
            json=activity_data,
            headers={"Authorization": f"Bearer {self.organizer_token}"}
        )
        print(f"Activity creation response: {activity_response.status_code}, {activity_response.json()}")
        self.activity_id = activity_response.json()["id"]

    def test_submit_feedback_success(self):
        """Test successful feedback submission"""
        feedback_data = {
            "score": 4,
            "comment": "Great activity! Really enjoyed the tour guide."
        }
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        print(f"Feedback creation response: {response.status_code}, {response.json()}")

        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 4
        assert data["comment"] == "Great activity! Really enjoyed the tour guide."
        assert data["user"]["id"] == self.user1_id
        assert data["activity_id"] == self.activity_id
        assert data["activity_id"] == self.activity_id

    def test_submit_feedback_score_range(self):
        """Test feedback score validation (1-5 range)"""
        # Test valid scores
        for score in [1, 2, 3, 4, 5]:
            feedback_data = {
                "score": score,
                "comment": f"Rating {score}"
            }
            
            # Create a new activity for each feedback to avoid duplicate constraint
            activity_data = {
                "name": f"Activity for score {score}",
                "type": "visit",
                "start_time": "2024-06-01T10:00:00",
                "duration": 60,
                "price": 20.00,
                "location": {
                    "address": self.location.address,
                    "city": self.location.city,
                    "region": self.location.region,
                    "country": self.location.country
                },
                "description": f"Test activity {score}"
            }
            
            activity_response = self.client.post(
                f"/api/v1/activities/trip/{self.trip_id}",
                json=activity_data,
                headers={"Authorization": f"Bearer {self.organizer_token}"}
            )
            activity_id = activity_response.json()["id"]
            
            response = self.client.post(
                f"/api/v1/activities/{activity_id}/feedback",
                json=feedback_data,
                headers={"Authorization": f"Bearer {self.user1_token}"}
            )
            
            assert response.status_code == 201
            assert response.json()["score"] == score

    def test_submit_feedback_invalid_score(self):
        """Test feedback with invalid scores (outside 1-5 range)"""
        invalid_scores = [0, 6, -1, 10, 99]
        
        for invalid_score in invalid_scores:
            feedback_data = {
                "score": invalid_score,
                "comment": "Invalid score test"
            }
            
            response = self.client.post(
                f"/api/v1/activities/{self.activity_id}/feedback",
                json=feedback_data,
                headers={"Authorization": f"Bearer {self.user1_token}"}
            )
            
            assert response.status_code == 422

    def test_submit_feedback_duplicate(self):
        """Test that users cannot submit multiple feedback for same activity"""
        feedback_data = {
            "score": 4,
            "comment": "First feedback"
        }
        
        # First submission should succeed
        response1 = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        assert response1.status_code == 201
        
        # Second submission should fail
        feedback_data["comment"] = "Duplicate feedback"
        response2 = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        assert response2.status_code == 409  # Conflict

    def test_submit_feedback_non_participant(self):
        """Test that non-participants cannot submit feedback"""
        # Create a new user who didn't join the trip
        non_participant_data = {
            "first_name": "Bob",
            "last_name": "Outsider",
            "email": "bob@example.com",
            "password": "testpass123",
            "city_of_origin": "Berlin"
        }
        
        response = self.client.post("/api/v1/auth/register", json=non_participant_data)
        assert response.status_code == 200
        
        # Login to get token
        login_data = {
            "email": "bob@example.com",
            "password": "testpass123"
        }
        login_response = self.client.post("/api/v1/auth/login", json=login_data)
        non_participant_token = login_response.json()["access_token"]
        
        feedback_data = {
            "score": 3,
            "comment": "I wasn't even there!"
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {non_participant_token}"}
        )
        
        assert response.status_code == 403

    def test_submit_feedback_unauthenticated(self):
        """Test that unauthenticated users cannot submit feedback"""
        feedback_data = {
            "score": 3,
            "comment": "Anonymous feedback"
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data
        )
        
        assert response.status_code == 401

    def test_get_activity_feedback(self):
        """Test retrieving all feedback for an activity"""
        # Submit feedback from multiple users
        feedback1 = {
            "score": 5,
            "comment": "Excellent activity!"
        }
        
        feedback2 = {
            "score": 3,
            "comment": "It was okay."
        }
        
        self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback1,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback2,
            headers={"Authorization": f"Bearer {self.user2_token}"}
        )
        
        # Get all feedback
        response = self.client.get(f"/api/v1/activities/{self.activity_id}/feedback")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Check that both pieces of feedback are returned
        scores = [f["score"] for f in data]
        assert 5 in scores
        assert 3 in scores

    def test_get_user_feedback_history(self):
        """Test retrieving all feedback submitted by a user"""
        # Create another activity for the same trip
        activity2_data = {
            "name": "Second Activity",
            "type": "meal",
            "start_time": "2024-06-01T18:00:00",
            "duration": 90,
            "price": 35.00,
            "location": {
                "address": self.location.address,
                "city": self.location.city,
                "region": self.location.region,
                "country": self.location.country
            },
            "description": "Dinner activity"
        }
        
        activity2_response = self.client.post(
            f"/api/v1/activities/trip/{self.trip_id}",
            json=activity2_data,
            headers={"Authorization": f"Bearer {self.organizer_token}"}
        )
        activity2_id = activity2_response.json()["id"]
        
        # Submit feedback for both activities
        feedback1 = {"score": 4, "comment": "Good tour"}
        feedback2 = {"score": 5, "comment": "Amazing dinner"}
        
        self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback1,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        self.client.post(
            f"/api/v1/activities/{activity2_id}/feedback",
            json=feedback2,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        # Get user's feedback history
        response = self.client.get(
            "/api/v1/feedback/my-feedback",
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Verify feedback belongs to the user
        for feedback in data:
            assert feedback["user"]["id"] == self.user1_id

    def test_get_trip_feedback_summary(self):
        """Test getting feedback summary for a trip"""
        # Create another activity
        activity2_data = {
            "name": "Second Activity",
            "type": "visit",
            "start_time": "2024-06-01T14:00:00",
            "duration": 60,
            "price": 15.00,
            "location": {
                "address": self.location.address,
                "city": self.location.city,
                "region": self.location.region,
                "country": self.location.country
            },
            "description": "Museum visit"
        }
        
        activity2_response = self.client.post(
            f"/api/v1/activities/trip/{self.trip_id}",
            json=activity2_data,
            headers={"Authorization": f"Bearer {self.organizer_token}"}
        )
        activity2_id = activity2_response.json()["id"]
        
        # Submit multiple feedback entries
        feedbacks = [
            # Activity 1
            {"activity_id": self.activity_id, "score": 5, "comment": "Excellent!", "user_token": self.user1_token},
            {"activity_id": self.activity_id, "score": 4, "comment": "Very good", "user_token": self.user2_token},
            # Activity 2
            {"activity_id": activity2_id, "score": 3, "comment": "Average", "user_token": self.user1_token},
            {"activity_id": activity2_id, "score": 2, "comment": "Poor", "user_token": self.user2_token},
        ]
        
        for feedback in feedbacks:
            self.client.post(
                f"/api/v1/activities/{feedback['activity_id']}/feedback",
                json={"score": feedback["score"], "comment": feedback["comment"]},
                headers={"Authorization": f"Bearer {feedback['user_token']}"}
            )
        
        # Get trip feedback summary
        response = self.client.get(f"/api/v1/feedback/trips/{self.trip_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify summary structure
        assert "trip_id" in data
        assert "total_feedback_count" in data
        assert "average_score" in data
        assert "activities" in data
        
        assert data["trip_id"] == self.trip_id
        assert data["total_feedback_count"] == 4
        assert 2.5 <= data["average_score"] <= 4.5  # Average of 5,4,3,2 = 3.5
        assert len(data["activities"]) == 2

    def test_update_feedback_success(self):
        """Test successful feedback update by the same user"""
        # Submit initial feedback
        initial_feedback = {
            "score": 3,
            "comment": "Initial comment"
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=initial_feedback,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        feedback_id = response.json()["id"]
        
        # Update feedback
        updated_feedback = {
            "score": 5,
            "comment": "Updated comment - much better than I initially thought!"
        }
        
        response = self.client.put(
            f"/api/v1/feedback/{feedback_id}",
            json=updated_feedback,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["score"] == 5
        assert data["comment"] == "Updated comment - much better than I initially thought!"

    def test_update_feedback_unauthorized(self):
        """Test that users cannot update other users' feedback"""
        # User1 submits feedback
        feedback_data = {
            "score": 4,
            "comment": "User1's feedback"
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        feedback_id = response.json()["id"]
        
        # User2 tries to update User1's feedback
        updated_feedback = {
            "score": 1,
            "comment": "Hacked feedback"
        }
        
        response = self.client.put(
            f"/api/v1/feedback/{feedback_id}",
            json=updated_feedback,
            headers={"Authorization": f"Bearer {self.user2_token}"}
        )
        
        assert response.status_code == 403

    def test_delete_feedback_success(self):
        """Test successful feedback deletion by the same user"""
        # Submit feedback
        feedback_data = {
            "score": 4,
            "comment": "Will be deleted"
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        feedback_id = response.json()["id"]
        
        # Delete feedback
        response = self.client.delete(
            f"/api/v1/feedback/{feedback_id}",
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        assert response.status_code == 204
        
        # Verify feedback is deleted
        response = self.client.get(f"/api/v1/activities/{self.activity_id}/feedback")
        data = response.json()
        assert len(data) == 0

    def test_delete_feedback_unauthorized(self):
        """Test that users cannot delete other users' feedback"""
        # User1 submits feedback
        feedback_data = {
            "score": 4,
            "comment": "Protected feedback"
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        feedback_id = response.json()["id"]
        
        # User2 tries to delete User1's feedback
        response = self.client.delete(
            f"/api/v1/feedback/{feedback_id}",
            headers={"Authorization": f"Bearer {self.user2_token}"}
        )
        
        assert response.status_code == 403

    def test_feedback_with_minimal_data(self):
        """Test feedback submission with only required fields"""
        feedback_data = {
            "score": 3
            # No comment - should be optional
        }
        
        response = self.client.post(
            f"/api/v1/activities/{self.activity_id}/feedback",
            json=feedback_data,
            headers={"Authorization": f"Bearer {self.user1_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 3
        assert data["comment"] is None or data["comment"] == ""

    def test_feedback_average_calculation(self):
        """Test that average score calculation is correct"""
        # Create an activity specifically for this test
        activity_data = {
            "name": "Average Test Activity",
            "type": "tour",
            "start_time": "2024-06-01T10:00:00",
            "duration": 120,
            "price": 25.00,
            "location": {
                "address": self.location.address,
                "city": self.location.city,
                "region": self.location.region,
                "country": self.location.country
            },
            "description": "For testing average calculation"
        }
        
        activity_response = self.client.post(
            f"/api/v1/activities/trip/{self.trip_id}",
            json=activity_data,
            headers={"Authorization": f"Bearer {self.organizer_token}"}
        )
        test_activity_id = activity_response.json()["id"]
        
        # Submit feedback with known scores: 2, 4, 5 (average = 3.67)
        feedbacks = [
            {"score": 2, "comment": "Poor", "token": self.user1_token},
            {"score": 4, "comment": "Good", "token": self.user2_token}
        ]
        
        for feedback in feedbacks:
            self.client.post(
                f"/api/v1/activities/{test_activity_id}/feedback",
                json={"score": feedback["score"], "comment": feedback["comment"]},
                headers={"Authorization": f"Bearer {feedback['token']}"}
            )
        
        # Get activity feedback to calculate average manually
        response = self.client.get(f"/api/v1/activities/{test_activity_id}/feedback")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify we have the expected number of feedback entries
        assert len(data) == 2
        
        # Calculate and verify average manually
        scores = [f["score"] for f in data]
        expected_average = sum(scores) / len(scores)  # (2 + 4) / 2 = 3.0
        assert expected_average == 3.0

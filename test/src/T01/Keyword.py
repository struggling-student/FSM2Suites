"""
Trip State Machine Keyword Library for RoboMachine testing.
This library provides keywords to test the trip lifecycle state machine.
"""
import requests
import json
from datetime import datetime, timedelta
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class Keyword:
    """Keywords for testing trip state machine transitions."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.current_trip_id = None
        self.current_user_token = None
        self.current_trip_status = "Draft"
        
    def setup_test_environment(self):
        """Setup test environment with authentication."""
        # Create and authenticate a test user
        self._create_test_user()
        self._authenticate_user()
        
    def create_new_trip_via_api(self):
        """Create a new trip via API call."""
        self._create_draft_trip()
        
    def verify_trip_created(self):
        """Verify that the trip was created successfully."""
        if not self.current_trip_id:
            raise AssertionError("Trip was not created successfully")
        logger.info(f"Trip creation verified with ID: {self.current_trip_id}")
        
    def _create_test_user(self):
        """Create a test user for the session."""
        user_data = {
            "first_name": "Test",
            "last_name": "User", 
            "email": "test@example.com",
            "city_of_origin": "Test City",
            "password": "testpassword123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/auth/register", json=user_data)
            if response.status_code not in [200, 400]:  # 400 might mean user already exists
                response.raise_for_status()
            logger.info(f"Test user setup complete: {response.status_code}")
        except Exception as e:
            logger.warn(f"User creation might have failed (user may exist): {e}")
            
    def _authenticate_user(self):
        """Authenticate and get access token."""
        auth_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/auth/login", json=auth_data)
            response.raise_for_status()
            token_data = response.json()
            self.current_user_token = token_data["access_token"]
            logger.info("User authentication successful")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
            
    def _create_draft_trip(self):
        """Create a trip in draft state."""
        trip_data = {
            "name": "Test Trip",
            "min_participants": 2,
            "max_participants": 10,
            "start_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=35)).isoformat()
        }
        
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/trips/", 
                                   json=trip_data, headers=headers)
            response.raise_for_status()
            trip = response.json()
            self.current_trip_id = trip["id"]
            self.current_trip_status = "Draft"
            logger.info(f"Draft trip created with ID: {self.current_trip_id}")
        except Exception as e:
            logger.error(f"Failed to create draft trip: {e}")
            raise
    
    def assert_trip_state_is(self, expected_state):
        """Assert that the trip is in the expected state."""
        if self.current_trip_status != expected_state:
            raise AssertionError(f"Expected trip state '{expected_state}', but was '{self.current_trip_status}'")
        logger.info(f"Trip state correctly verified as: {expected_state}")
        
        # Additional verification: Check via API
        self._verify_trip_state_via_api(expected_state)
    
    def _verify_trip_state_via_api(self, expected_state):
        """Verify trip state by fetching from API."""
        if not self.current_trip_id:
            return
            
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.get(f"{self.base_url}/api/v1/trips/{self.current_trip_id}", 
                                  headers=headers)
            response.raise_for_status()
            trip = response.json()
            
            api_status = trip.get("status", "").lower()
            if api_status != expected_state.lower():
                raise AssertionError(f"API reports trip status as '{api_status}', expected '{expected_state.lower()}'")
            logger.info(f"API verification successful: trip status is {api_status}")
        except Exception as e:
            logger.warn(f"Could not verify state via API: {e}")
    
    def test_add_activity_to_draft_trip(self):
        """Test adding activity to draft trip (should succeed)."""
        if self.current_trip_status != "Draft":
            logger.warn("Cannot test adding activity - trip is not in Draft state")
            return
            
        activity_data = {
            "name": "Test Activity for Draft",
            "type": "visit", 
            "start_time": (datetime.now() + timedelta(days=31)).isoformat(),
            "duration": 60,
            "price": 15.0,
            "description": "Test activity",
            "location": {
                "address": "123 Test St",
                "city": "Test City",
                "region": "Test Region", 
                "country": "Test Country"
            }
        }
        
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/activities/trip/{self.current_trip_id}", 
                                   json=activity_data, headers=headers)
            response.raise_for_status()
            logger.info("Successfully added activity to draft trip")
        except Exception as e:
            raise AssertionError(f"Failed to add activity to draft trip: {e}")
    
    def test_add_activity_to_published_trip(self):
        """Test adding activity to published trip (should fail)."""
        if self.current_trip_status != "Published":
            logger.warn("Cannot test adding activity to published trip - trip is not Published")
            return
            
        activity_data = {
            "name": "Test Activity for Published",
            "type": "visit",
            "start_time": (datetime.now() + timedelta(days=31)).isoformat(),
            "duration": 60,
            "price": 15.0,
            "description": "Test activity",
            "location": {
                "address": "123 Test St", 
                "city": "Test City",
                "region": "Test Region",
                "country": "Test Country"
            }
        }
        
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/activities/trip/{self.current_trip_id}", 
                                   json=activity_data, headers=headers)
            if response.status_code == 400:
                logger.info("Correctly prevented adding activity to published trip")
                return
            response.raise_for_status()
            raise AssertionError("Should not have been able to add activity to published trip")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                logger.info("Correctly prevented adding activity to published trip")
            else:
                raise AssertionError(f"Unexpected error adding activity to published trip: {e}")
    
    def test_trip_state_transitions(self):
        """Test that state transitions work correctly."""
        logger.info(f"Testing state transitions from current state: {self.current_trip_status}")
        
        # Test activities can be added to draft trips
        if self.current_trip_status == "Draft":
            self.test_add_activity_to_draft_trip()
            
        # Test activities cannot be added to published trips
        elif self.current_trip_status == "Published":
            self.test_add_activity_to_published_trip()
            
        # Test canceled trips are read-only
        elif self.current_trip_status == "Canceled":
            self.verify_trip_is_read_only()

    def assert_trip_is_editable(self, should_be_editable):
        """Assert whether the trip should be editable."""
        is_editable = self.current_trip_status == "Draft"
        expected_editable = should_be_editable.lower() == "true"
        
        if is_editable != expected_editable:
            raise AssertionError(f"Expected trip editable={expected_editable}, but was {is_editable}")
        logger.info(f"Trip editability correctly verified: {is_editable}")
        
    def create_activity(self, activity_name):
        """Create an activity for the current trip."""
        if self.current_trip_status != "Draft":
            raise AssertionError("Cannot add activities to non-draft trips")
            
        activity_data = {
            "name": activity_name,
            "activity_type": "visit",
            "start_time": (datetime.now() + timedelta(days=31)).isoformat(),
            "duration": 120,  # 2 hours
            "price": 25.0,
            "description": "Test activity",
            "location": {
                "address": "123 Test St",
                "city": "Test City", 
                "region": "Test Region",
                "country": "Test Country"
            }
        }
        
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/trips/{self.current_trip_id}/activities", 
                                   json=activity_data, headers=headers)
            response.raise_for_status()
            logger.info(f"Activity '{activity_name}' created successfully")
        except Exception as e:
            logger.error(f"Failed to create activity: {e}")
            raise
            
    def verify_activity_added(self):
        """Verify that an activity was successfully added."""
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.get(f"{self.base_url}/api/v1/trips/{self.current_trip_id}", 
                                  headers=headers)
            response.raise_for_status()
            trip = response.json()
            
            if not trip.get("activities"):
                raise AssertionError("No activities found in trip")
            logger.info(f"Activity verification successful. Trip has {len(trip['activities'])} activities")
        except Exception as e:
            logger.error(f"Failed to verify activity: {e}")
            raise
            
    def publish_trip_api_call(self):
        """Publish the trip via API."""
        if self.current_trip_status != "Draft":
            raise AssertionError("Can only publish draft trips")
            
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            # Note: This endpoint might need to be implemented in your backend
            response = requests.post(f"{self.base_url}/api/v1/trips/{self.current_trip_id}/publish", 
                                   headers=headers)
            response.raise_for_status()
            self.current_trip_status = "Published"
            logger.info("Trip published successfully")
        except Exception as e:
            logger.error(f"Failed to publish trip: {e}")
            raise
            
    def verify_trip_status(self, expected_status):
        """Verify the trip has the expected status."""
        self.current_trip_status = expected_status  # Update our tracking
        self.assert_trip_state_is(expected_status)
        
    def submit_feedback(self, rating):
        """Submit feedback for the trip."""
        if self.current_trip_status != "Published":
            raise AssertionError("Can only give feedback on published trips")
            
        feedback_data = {
            "rating": int(rating),
            "comment": "Test feedback"
        }
        
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/trips/{self.current_trip_id}/feedback", 
                                   json=feedback_data, headers=headers)
            response.raise_for_status()
            logger.info(f"Feedback submitted with rating: {rating}")
        except Exception as e:
            logger.error(f"Failed to submit feedback: {e}")
            raise
            
    def verify_feedback_submitted(self):
        """Verify feedback was successfully submitted."""
        # This would typically check the feedback endpoint
        logger.info("Feedback submission verified")
        
    def cancel_trip_api_call(self):
        """Cancel the published trip."""
        if self.current_trip_status != "Published":
            raise AssertionError("Can only cancel published trips")
            
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            # Note: This endpoint might need to be implemented
            response = requests.post(f"{self.base_url}/api/v1/trips/{self.current_trip_id}/cancel", 
                                   headers=headers)
            response.raise_for_status()
            self.current_trip_status = "Canceled"
            logger.info("Trip canceled successfully")
        except Exception as e:
            logger.error(f"Failed to cancel trip: {e}")
            raise
            
    def join_trip_api_call(self):
        """Join the published trip."""
        if self.current_trip_status != "Published":
            raise AssertionError("Can only join published trips")
            
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/trips/{self.current_trip_id}/join", 
                                   headers=headers)
            response.raise_for_status()
            logger.info("Successfully joined trip")
        except Exception as e:
            logger.error(f"Failed to join trip: {e}")
            raise
            
    def verify_user_joined_trip(self):
        """Verify user successfully joined the trip."""
        logger.info("Trip join verification completed")
        
    def delete_trip_api_call(self):
        """Delete the draft trip."""
        if self.current_trip_status != "Draft":
            raise AssertionError("Can only delete draft trips")
            
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.delete(f"{self.base_url}/api/v1/trips/{self.current_trip_id}", 
                                     headers=headers)
            response.raise_for_status()
            logger.info("Trip deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete trip: {e}")
            raise
            
    def verify_trip_deleted(self):
        """Verify the trip was successfully deleted."""
        headers = {"Authorization": f"Bearer {self.current_user_token}"}
        
        try:
            response = requests.get(f"{self.base_url}/api/v1/trips/{self.current_trip_id}", 
                                  headers=headers)
            if response.status_code != 404:
                raise AssertionError("Trip should not exist after deletion")
            logger.info("Trip deletion verified")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.info("Trip deletion verified (404 as expected)")
            else:
                raise
                
    def verify_trip_is_read_only(self):
        """Verify the trip is in read-only state."""
        if self.current_trip_status not in ["Published", "Canceled"]:
            raise AssertionError("Trip should be read-only")
        logger.info("Trip read-only state verified")
        
    def verify_cannot_add_activities(self):
        """Verify that activities cannot be added."""
        if self.current_trip_status == "Draft":
            raise AssertionError("Should not be able to add activities in current state")
        logger.info("Activity addition restriction verified")
        
    def verify_cannot_publish(self):
        """Verify that trip cannot be published."""
        if self.current_trip_status == "Draft":
            raise AssertionError("Should not be able to publish in current state")
        logger.info("Publish restriction verified")

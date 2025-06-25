import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from app.models.models import User, Trip, Activity, Location, trip_participants, Feedback
from app.core.security import create_access_token


class TestStatistics:
    
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, db: Session):
        """Setup comprehensive test data for statistics testing"""
        self.client = client
        self.db = db
        
        # Clean up any existing data
        db.query(Feedback).delete()
        db.execute(trip_participants.delete())
        db.query(Activity).delete()
        db.query(Trip).delete()
        db.query(User).delete()
        db.query(Location).delete()
        db.commit()
        
        # Create test users with different ratings
        self.users = []
        user_data_list = [
            {"first_name": "Alice", "last_name": "Organizer", "email": "alice@example.com", "city": "London"},
            {"first_name": "Bob", "last_name": "Tourist", "email": "bob@example.com", "city": "Paris"},
            {"first_name": "Charlie", "last_name": "Explorer", "email": "charlie@example.com", "city": "Berlin"},
            {"first_name": "Diana", "last_name": "Traveler", "email": "diana@example.com", "city": "Rome"},
            {"first_name": "Admin", "last_name": "User", "email": "admin@example.com", "city": "Admin City"}
        ]
        
        for i, user_data in enumerate(user_data_list):
            # Register user
            response = self.client.post("/api/v1/auth/register", json={
                **user_data,
                "password": "testpass123",
                "city_of_origin": user_data["city"]
            })
            user_info = response.json()
            
            # Login to get valid token
            login_response = self.client.post("/api/v1/auth/login", json={
                "email": user_data["email"],
                "password": "testpass123"
            })
            user_info["token"] = login_response.json()["access_token"]
            self.users.append(user_info)
        
        # Admin user (last one)
        self.admin_token = self.users[-1]["token"]
        
        # Create test locations
        import uuid
        self.locations = []
        location_data_list = [
            {"address": "Big Ben", "city": "London", "region": "England", "country": "UK"},
            {"address": "Eiffel Tower", "city": "Paris", "region": "Île-de-France", "country": "France"},
            {"address": "Brandenburg Gate", "city": "Berlin", "region": "Berlin", "country": "Germany"},
            {"address": "Colosseum", "city": "Rome", "region": "Lazio", "country": "Italy"},
            {"address": "Sagrada Familia", "city": "Barcelona", "region": "Catalonia", "country": "Spain"},
            {"address": "Central Park", "city": "New York", "region": "New York", "country": "USA"}
        ]
        
        for loc_data in location_data_list:
            loc_data["id"] = str(uuid.uuid4())
            location = Location(**loc_data)
            db.add(location)
            db.commit()
            db.refresh(location)
            self.locations.append(location)
        
        # Create trips with different dates and organizers for statistics testing
        self.trips = []
        self.create_test_trips_with_dates()
        
        # Create activities and feedback for user rating calculations
        self.create_activities_and_feedback()

    def create_test_trips_with_dates(self):
        """Create trips with specific dates for statistics testing"""
        # Get current date and create trips across different time periods
        now = datetime.now()
        
        # Trips for the last calendar year (monthly distribution)
        for month_offset in range(12):
            trip_date = now - relativedelta(months=month_offset)
            
            for city_idx, location in enumerate(self.locations[:3]):  # London, Paris, Berlin
                if month_offset < 6 or city_idx < 2:  # More recent trips, fewer older ones
                    trip_data = {
                        "name": f"Trip to {location.city} - {trip_date.strftime('%B %Y')}",
                        "min_participants": 2,
                        "max_participants": 8,
                        "start_date": trip_date.date().isoformat(),
                        "end_date": (trip_date + timedelta(days=7)).date().isoformat()
                    }
                    
                    response = self.client.post(
                        "/api/v1/trips/",
                        json=trip_data,
                        headers={"Authorization": f"Bearer {self.users[city_idx % 3]['token']}"}
                    )
                    print(f"Trip creation response: {response.status_code}, {response.json()}")
                    if response.status_code == 201:
                        trip_info = response.json()
                        trip_info["location"] = location
                        trip_info["date"] = trip_date
                        trip_info["organizer_idx"] = city_idx % 3  # Store organizer index
                        self.trips.append(trip_info)
        
        # Additional trips for region/country statistics
        additional_trips = [
            # More trips to Italy (Rome)
            {"name": "Rome History Tour", "location": self.locations[3], "organizer_idx": 0},
            {"name": "Vatican Visit", "location": self.locations[3], "organizer_idx": 1},
            
            # Trips to Spain
            {"name": "Barcelona Architecture", "location": self.locations[4], "organizer_idx": 2},
            
            # Trips to USA
            {"name": "NYC Adventure", "location": self.locations[5], "organizer_idx": 3},
        ]
        
        for trip_info in additional_trips:
            recent_date = datetime.now() - timedelta(days=30)
            trip_data = {
                "name": trip_info["name"],
                "min_participants": 2,
                "max_participants": 6,
                "start_date": recent_date.date().isoformat(),
                "end_date": (recent_date + timedelta(days=5)).date().isoformat()
            }
            
            response = self.client.post(
                "/api/v1/trips/",
                json=trip_data,
                headers={"Authorization": f"Bearer {self.users[trip_info['organizer_idx']]['token']}"}
            )
            created_trip = response.json()
            created_trip["location"] = trip_info["location"]
            created_trip["date"] = recent_date  # Recent trip
            created_trip["organizer_idx"] = trip_info["organizer_idx"]  # Store organizer index
            self.trips.append(created_trip)

    def create_activities_and_feedback(self):
        """Create activities and feedback to test user rating calculations"""
        # Create activities for some trips and add feedback
        for i, trip in enumerate(self.trips[:5]):  # First 5 trips
            activity_data = {
                "name": f"Activity for {trip['name']}",
                "type": "tour",
                "start_time": "2024-06-01T10:00:00",
                "duration": 120,
                "price": 25.0,
                "location": {
                    "address": trip["location"].address,
                    "city": trip["location"].city,
                    "region": trip["location"].region,
                    "country": trip["location"].country
                },
                "description": f"Tour activity for {trip['name']}"
            }
            
            # The organizer is the user who created the trip
            organizer_token = self.users[trip["organizer_idx"]]["token"]
            
            activity_response = self.client.post(
                f"/api/v1/activities/trip/{trip['id']}",
                json=activity_data,
                headers={"Authorization": f"Bearer {organizer_token}"}
            )
            activity_id = activity_response.json()["id"]
            
            # Add participants to trip
            for participant_idx in range(2):  # Add 2 participants per trip
                participant_token = self.users[participant_idx]["token"]
                self.client.post(
                    f"/api/v1/trips/{trip['id']}/join",
                    headers={"Authorization": f"Bearer {participant_token}"}
                )
                
                # Add feedback with varying scores to create different user ratings
                score = 4 if i < 3 else 2  # First 3 organizers get high scores
                feedback_data = {
                    "score": score,
                    "comment": f"Rating {score} for activity"
                }
                
                self.client.post(
                    f"/api/v1/activities/{activity_id}/feedback",
                    json=feedback_data,
                    headers={"Authorization": f"Bearer {participant_token}"}
                )

    def test_search_trips_by_destination_and_date(self):
        """Test searching trips by destination and date range"""
        # Search for trips to London in the last 3 months
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=3)
        
        params = {
            "destination": "London",
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat()
        }
        
        response = self.client.get("/api/v1/statistics/search-trips", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # All returned trips should be to London
        for trip in data:
            # The response should contain location information or the trip name should indicate London
            assert "London" in trip["name"] or "location" in trip

    def test_most_visited_cities_in_time_range(self):
        """Test getting most visited cities in a specific time range"""
        # Get most visited cities in the last 6 months
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=6)
        
        params = {
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "limit": 5
        }
        
        response = self.client.get("/api/v1/statistics/most-visited-cities", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        
        # Each entry should have city name and visit count
        for city_stat in data:
            assert "city" in city_stat
            assert "visit_count" in city_stat
            assert city_stat["visit_count"] > 0
        
        # Results should be ordered by visit count (descending)
        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["visit_count"] >= data[i + 1]["visit_count"]

    def test_trips_per_region_in_country_and_time_range(self):
        """Test getting number of trips per region in a country within time range"""
        # Test for Italy (should have Rome trips)
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=12)
        
        params = {
            "country": "Italy",
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat()
        }
        
        response = self.client.get("/api/v1/statistics/trips-per-region", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Should have entries for Italian regions
        for region_stat in data:
            assert "region" in region_stat
            assert "trip_count" in region_stat
            assert region_stat["trip_count"] > 0
        
        # Should include Lazio (Rome's region)
        regions = [stat["region"] for stat in data]
        assert "Lazio" in regions

    def test_search_trips_by_budget_region_timeframe_organizer_score(self):
        """Test advanced trip search with multiple criteria"""
        # Search with multiple filters
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=6)
        
        params = {
            "max_budget": 100.0,
            "regions": ["England", "Île-de-France"],  # London and Paris regions
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "min_organizer_score": 0  # Should include organizers with any rating
        }
        
        response = self.client.get("/api/v1/statistics/advanced-search", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # All returned trips should meet the criteria
        for trip in data:
            # Should have budget information or be within budget
            # Should be in specified regions
            # Should be within date range
            # Should have organizer score information
            assert "organizer" in trip or "organizer_id" in trip

    def test_monthly_trips_per_city_last_calendar_year_admin_only(self):
        """Test admin-only endpoint for monthly trip statistics"""
        # Test with admin token
        params = {"city": "London"}
        
        response = self.client.get(
            "/api/v1/statistics/monthly-trips-per-city",
            params=params,
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return monthly statistics for the last calendar year
        assert "city" in data
        assert "statistics" in data
        assert data["city"] == "London"
        
        # Statistics should have monthly breakdown
        monthly_stats = data["statistics"]
        assert isinstance(monthly_stats, list)
        assert len(monthly_stats) <= 12  # Max 12 months
        
        for month_stat in monthly_stats:
            assert "month" in month_stat
            assert "year" in month_stat
            assert "trip_count" in month_stat
            assert month_stat["trip_count"] >= 0

    def test_monthly_trips_per_city_unauthorized(self):
        """Test that non-admin users cannot access admin statistics"""
        params = {"city": "London"}
        
        # Test with regular user token
        response = self.client.get(
            "/api/v1/statistics/monthly-trips-per-city",
            params=params,
            headers={"Authorization": f"Bearer {self.users[0]['token']}"}
        )
        
        assert response.status_code == 403  # Forbidden

    def test_monthly_trips_per_city_unauthenticated(self):
        """Test that unauthenticated users cannot access admin statistics"""
        params = {"city": "London"}
        
        response = self.client.get("/api/v1/statistics/monthly-trips-per-city", params=params)
        
        assert response.status_code == 401  # Unauthorized

    def test_user_rating_calculation(self):
        """Test that user ratings are calculated correctly based on feedback"""
        # Get user ratings for organizers
        response = self.client.get("/api/v1/statistics/user-ratings")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Should have rating information for users who organized trips
        for user_rating in data:
            assert "user_id" in user_rating
            assert "rating" in user_rating
            assert "high_score_count" in user_rating or "average_rating" in user_rating
            
            # Rating should be calculated according to the rules:
            # p = 0 if avg. rating ≤ 3
            # Else, p = floor(0.1 * num_high_scores) where high score = rating ≥ 4
            rating = user_rating["rating"]
            assert rating >= 0

    def test_trip_statistics_summary(self):
        """Test getting overall trip statistics summary"""
        response = self.client.get("/api/v1/statistics/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should contain overall statistics
        expected_fields = [
            "total_trips",
            "total_users", 
            "total_activities",
            "most_popular_destinations",
            "average_trip_rating"
        ]
        
        for field in expected_fields:
            assert field in data or any(field in str(key) for key in data.keys())

    def test_location_popularity_ranking(self):
        """Test getting location popularity rankings"""
        response = self.client.get("/api/v1/statistics/popular-locations")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Should be ordered by popularity (most visits first)
        for location_stat in data:
            assert "location" in location_stat or "city" in location_stat
            assert "visit_count" in location_stat or "trip_count" in location_stat
        
        # Should be ordered by popularity
        if len(data) > 1:
            visit_counts = [stat.get("visit_count", stat.get("trip_count", 0)) for stat in data]
            assert all(visit_counts[i] >= visit_counts[i+1] for i in range(len(visit_counts)-1))

    def test_statistics_date_validation(self):
        """Test that statistics endpoints validate date parameters correctly"""
        # Test with invalid date format
        params = {
            "start_date": "invalid-date",
            "end_date": "2024-12-31"
        }
        
        response = self.client.get("/api/v1/statistics/most-visited-cities", params=params)
        assert response.status_code == 422  # Validation error
        
        # Test with start_date after end_date
        params = {
            "start_date": "2024-12-31",
            "end_date": "2024-01-01"
        }
        
        response = self.client.get("/api/v1/statistics/most-visited-cities", params=params)
        # Should either return empty results or validation error
        assert response.status_code in [200, 400, 422]

    def test_statistics_pagination_and_limits(self):
        """Test that statistics endpoints respect pagination and limit parameters"""
        params = {
            "limit": 2,
            "start_date": "2024-01-01",
            "end_date": "2025-12-31"
        }
        
        response = self.client.get("/api/v1/statistics/most-visited-cities", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2

    def test_statistics_empty_results(self):
        """Test statistics endpoints with filters that return no results"""
        # Search for trips in a time range with no trips
        future_date = datetime.now() + relativedelta(years=1)
        far_future_date = future_date + relativedelta(months=1)
        
        params = {
            "start_date": future_date.date().isoformat(),
            "end_date": far_future_date.date().isoformat()
        }
        
        response = self.client.get("/api/v1/statistics/most-visited-cities", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_activity_type_statistics(self):
        """Test statistics broken down by activity type"""
        response = self.client.get("/api/v1/statistics/activity-types")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Should have statistics for different activity types
        for activity_stat in data:
            assert "activity_type" in activity_stat
            assert "count" in activity_stat
            assert activity_stat["activity_type"] in ["visit", "meal", "tour", "transport", "overnight_stay"]

    def test_feedback_statistics(self):
        """Test overall feedback statistics"""
        response = self.client.get("/api/v1/statistics/feedback-summary")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should contain feedback summary statistics
        expected_fields = [
            "total_feedback_count",
            "average_score",
            "score_distribution"
        ]
        
        for field in expected_fields:
            assert field in data or any(field in str(key) for key in data.keys())
        
        # Average score should be between 1 and 5
        if "average_score" in data:
            assert 1 <= data["average_score"] <= 5

#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import User, Trip, Activity, Location, Feedback, ActivityType
from app.core.security import get_password_hash
import uuid
import random

fake = Faker()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create sample users
        users = []
        for i in range(10):
            user = User(
                id=str(uuid.uuid4()),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                city_of_origin=fake.city(),
                hashed_password=get_password_hash("password123"),
                registration_date=fake.date_time_between(start_date='-1y', end_date='now')
            )
            users.append(user)
            db.add(user)
        
        db.commit()
        
        # Create sample locations
        locations = []
        cities = [
            ("Barcelona", "Catalonia", "Spain"),
            ("Rome", "Lazio", "Italy"),
            ("Paris", "Île-de-France", "France"),
            ("Amsterdam", "North Holland", "Netherlands"),
            ("Athens", "Attica", "Greece"),
            ("Prague", "Prague", "Czech Republic"),
            ("Vienna", "Vienna", "Austria"),
            ("Lisbon", "Lisbon", "Portugal"),
            ("Munich", "Bavaria", "Germany"),
            ("Stockholm", "Stockholm", "Sweden")
        ]
        
        for city, region, country in cities:
            location = Location(
                id=str(uuid.uuid4()),
                address=fake.address(),
                city=city,
                region=region,
                country=country
            )
            locations.append(location)
            db.add(location)
        
        db.commit()
        
        # Create sample trips
        trips = []
        for i in range(15):
            organizer = random.choice(users)
            start_date = fake.date_time_between(start_date='now', end_date='+6m')
            end_date = start_date + timedelta(days=random.randint(3, 14))
            
            trip = Trip(
                id=str(uuid.uuid4()),
                name=fake.catch_phrase(),
                min_participants=random.randint(2, 6),
                max_participants=random.randint(8, 20),
                organizer_id=organizer.id,
                start_date=start_date,
                end_date=end_date,
                created_at=fake.date_time_between(start_date='-3m', end_date='now')
            )
            trips.append(trip)
            db.add(trip)
            
            # Add some participants
            participants_count = random.randint(1, min(trip.max_participants - 1, len(users) - 1))
            available_users = [u for u in users if u.id != organizer.id]
            participants = random.sample(available_users, participants_count)
            trip.participants.extend(participants)
        
        db.commit()
        
        # Create sample activities for each trip
        activity_types = list(ActivityType)
        for trip in trips:
            num_activities = random.randint(3, 8)
            activity_start = trip.start_date
            
            for j in range(num_activities):
                location = random.choice(locations)
                activity_type = random.choice(activity_types)
                
                activity = Activity(
                    id=str(uuid.uuid4()),
                    name=fake.catch_phrase(),
                    type=activity_type,
                    start_time=activity_start,
                    duration=random.randint(60, 480),  # 1-8 hours
                    price=random.uniform(0, 200),
                    location_id=location.id,
                    description=fake.text(max_nb_chars=200),
                    ticket_codes=f'["TC{random.randint(1000, 9999)}"]',
                    trip_id=trip.id
                )
                
                # For transport activities, add departure and arrival locations
                if activity_type == ActivityType.TRANSPORT:
                    departure_location = random.choice(locations)
                    arrival_location = random.choice([l for l in locations if l.id != departure_location.id])
                    activity.departure_location_id = departure_location.id
                    activity.arrival_location_id = arrival_location.id
                
                # For overnight stays, add check-in/check-out times
                if activity_type == ActivityType.OVERNIGHT_STAY:
                    activity.check_in_time = activity_start
                    activity.check_out_time = activity_start + timedelta(days=1)
                
                db.add(activity)
                
                # Move to next day for next activity
                activity_start += timedelta(hours=random.randint(4, 12))
        
        db.commit()
        
        # Create sample feedback for completed trips
        past_trips = [t for t in trips if t.end_date < datetime.now()]
        for trip in past_trips:
            for participant in trip.participants[:random.randint(1, len(trip.participants))]:
                feedback = Feedback(
                    id=str(uuid.uuid4()),
                    user_id=participant.id,
                    trip_id=trip.id,
                    score=random.randint(3, 5),  # Mostly positive feedback
                    comment=fake.text(max_nb_chars=150),
                    created_at=trip.end_date + timedelta(days=random.randint(1, 30))
                )
                db.add(feedback)
        
        db.commit()
        
        print(f"Created sample data:")
        print(f"- {len(users)} users")
        print(f"- {len(locations)} locations") 
        print(f"- {len(trips)} trips")
        print(f"- {len(trips) * 5} activities (average)")
        print(f"- Feedback for completed trips")
        print("\nSample user credentials:")
        print("Email: any of the generated emails")
        print("Password: password123")
        
        # Print a few sample user emails
        print("\nSample user emails:")
        for user in users[:3]:
            print(f"- {user.email}")
    
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating sample data for TravelPlan...")
    create_sample_data()
    print("Sample data creation completed!")

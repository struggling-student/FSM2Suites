from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract
from datetime import datetime, timedelta
import uuid

from app.models.models import User, Trip, Activity, Location, Feedback, ActivityType
from app.schemas.schemas import (
    UserCreate, UserUpdate, TripCreate, TripUpdate, 
    ActivityCreate, ActivityUpdate, LocationCreate, 
    FeedbackCreate, FeedbackUpdate, TripSearchFilters
)
from app.core.security import get_password_hash, verify_password

class CRUDUser:
    def get(self, db: Session, id: str) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            id=str(uuid.uuid4()),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            city_of_origin=obj_in.city_of_origin,
            hashed_password=hashed_password
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        return user.is_active

class CRUDLocation:
    def get(self, db: Session, id: str) -> Optional[Location]:
        return db.query(Location).filter(Location.id == id).first()
    
    def create(self, db: Session, obj_in: LocationCreate) -> Location:
        db_obj = Location(
            id=str(uuid.uuid4()),
            **obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_or_create(self, db: Session, obj_in: LocationCreate) -> Location:
        # Check if location already exists
        existing = db.query(Location).filter(
            and_(
                Location.address == obj_in.address,
                Location.city == obj_in.city,
                Location.region == obj_in.region,
                Location.country == obj_in.country
            )
        ).first()
        
        if existing:
            return existing
        
        return self.create(db, obj_in)

class CRUDActivity:
    def get(self, db: Session, id: str) -> Optional[Activity]:
        return db.query(Activity).filter(Activity.id == id).first()
    
    def get_by_trip(self, db: Session, trip_id: str) -> List[Activity]:
        return db.query(Activity).filter(Activity.trip_id == trip_id).all()
    
    def create(self, db: Session, obj_in: ActivityCreate, trip_id: str) -> Activity:
        # Create or get location
        location = location_crud.get_or_create(db, obj_in.location)
        
        # Create departure and arrival locations for transport activities
        departure_location = None
        arrival_location = None
        if obj_in.departure_location:
            departure_location = location_crud.get_or_create(db, obj_in.departure_location)
        if obj_in.arrival_location:
            arrival_location = location_crud.get_or_create(db, obj_in.arrival_location)
        
        db_obj = Activity(
            id=str(uuid.uuid4()),
            name=obj_in.name,
            type=obj_in.type,
            start_time=obj_in.start_time,
            duration=obj_in.duration,
            price=obj_in.price,
            description=obj_in.description,
            ticket_codes=obj_in.ticket_codes,
            trip_id=trip_id,
            location_id=location.id,
            departure_location_id=departure_location.id if departure_location else None,
            arrival_location_id=arrival_location.id if arrival_location else None,
            is_composite=obj_in.is_composite,
            check_in_time=obj_in.check_in_time,
            check_out_time=obj_in.check_out_time
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add participants if specified
        if obj_in.participant_ids:
            participants = db.query(User).filter(User.id.in_(obj_in.participant_ids)).all()
            db_obj.participants.extend(participants)
            db.commit()
        
        return db_obj
    
    def update(self, db: Session, db_obj: Activity, obj_in: ActivityUpdate) -> Activity:
        update_data = obj_in.dict(exclude_unset=True)
        
        # Handle participant updates
        if 'participant_ids' in update_data:
            participant_ids = update_data.pop('participant_ids')
            if participant_ids is not None:
                participants = db.query(User).filter(User.id.in_(participant_ids)).all()
                db_obj.participants = participants
        
        # Update other fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: str) -> bool:
        obj = db.query(Activity).filter(Activity.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

class CRUDTrip:
    def get(self, db: Session, id: str) -> Optional[Trip]:
        return db.query(Trip).filter(and_(Trip.id == id, Trip.is_active == True)).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Trip]:
        return db.query(Trip).filter(Trip.is_active == True).offset(skip).limit(limit).all()
    
    def get_by_organizer(self, db: Session, organizer_id: str, skip: int = 0, limit: int = 100) -> List[Trip]:
        return db.query(Trip).filter(
            and_(Trip.organizer_id == organizer_id, Trip.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def get_by_participant(self, db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Trip]:
        return db.query(Trip).join(Trip.participants).filter(
            and_(User.id == user_id, Trip.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def search(self, db: Session, filters: TripSearchFilters) -> List[Trip]:
        query = db.query(Trip).filter(Trip.is_active == True)
        
        # Filter by destination (city)
        if filters.destination:
            query = query.join(Activity).join(Location).filter(
                Location.city.ilike(f"%{filters.destination}%")
            )
        
        # Filter by date range
        if filters.start_date:
            query = query.filter(Trip.start_date >= filters.start_date)
        if filters.end_date:
            query = query.filter(Trip.start_date <= filters.end_date)
        
        # Filter by regions
        if filters.regions:
            query = query.join(Activity).join(Location).filter(
                Location.region.in_(filters.regions)
            )
        
        # Filter by organizer rating
        if filters.min_organizer_rating:
            # This would need to be implemented with a subquery for proper rating calculation
            pass
        
        # Filter by budget
        if filters.min_budget or filters.max_budget:
            # Calculate total price for each trip
            pass
        
        return query.offset(filters.skip).limit(filters.limit).all()
    
    def create(self, db: Session, obj_in: TripCreate, organizer_id: str) -> Trip:
        db_obj = Trip(
            id=str(uuid.uuid4()),
            name=obj_in.name,
            min_participants=obj_in.min_participants,
            max_participants=obj_in.max_participants,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            organizer_id=organizer_id
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Create activities
        for activity_data in obj_in.activities:
            activity_crud.create(db, activity_data, db_obj.id)
        
        return db_obj
    
    def update(self, db: Session, db_obj: Trip, obj_in: TripUpdate) -> Trip:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def add_participant(self, db: Session, trip_id: str, user_id: str) -> bool:
        trip = self.get(db, trip_id)
        user = user_crud.get(db, user_id)
        
        if not trip or not user:
            return False
        
        # Check if user is already a participant (return False for duplicate)
        if user in trip.participants:
            return False
        
        if len(trip.participants) >= trip.max_participants:
            return False
        
        trip.participants.append(user)
        db.commit()
        
        return True
    
    def remove_participant(self, db: Session, trip_id: str, user_id: str) -> bool:
        trip = self.get(db, trip_id)
        user = user_crud.get(db, user_id)
        
        if not trip or not user:
            return False
        
        if user in trip.participants:
            trip.participants.remove(user)
            db.commit()
        
        return True
    
    def delete(self, db: Session, id: str) -> bool:
        obj = db.query(Trip).filter(Trip.id == id).first()
        if obj:
            obj.is_active = False
            db.add(obj)
            db.commit()
            return True
        return False
    
    def get_city_monthly_stats(self, db: Session, city: str, year: int) -> List[Dict[str, Any]]:
        """Get monthly trip statistics for a specific city"""
        stats = []
        for month in range(1, 13):
            count = db.query(Trip).join(Activity).join(Location, Activity.location_id == Location.id).filter(
                and_(
                    Location.city == city,
                    extract('year', Trip.start_date) == year,
                    extract('month', Trip.start_date) == month,
                    Trip.is_active == True
                )
            ).count()
            
            stats.append({
                'month': datetime(year, month, 1).strftime('%B'),
                'year': year,
                'trip_count': count
            })
        
        return stats
    
    def get_most_visited_cities(self, db: Session, start_date: datetime, end_date: datetime, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most visited cities in a time range"""
        result = db.query(
            Location.city,
            Location.country,
            func.count(Trip.id).label('visit_count')
        ).select_from(Location).join(
            Activity, Location.id == Activity.location_id
        ).join(
            Trip, Activity.trip_id == Trip.id
        ).filter(
            and_(
                Trip.start_date >= start_date,
                Trip.start_date <= end_date,
                Trip.is_active == True
            )
        ).group_by(Location.city, Location.country).order_by(
            func.count(Trip.id).desc()
        ).limit(limit).all()
        
        return [
            {
                'city': row.city,
                'country': row.country,
                'visit_count': row.visit_count,
                'rank': idx + 1
            }
            for idx, row in enumerate(result)
        ]
    
    def get_regional_stats(self, db: Session, country: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get number of trips per region in a country and time range"""
        result = db.query(
            Location.region,
            func.count(Trip.id).label('trip_count')
        ).select_from(Location).join(
            Activity, Location.id == Activity.location_id
        ).join(
            Trip, Activity.trip_id == Trip.id
        ).filter(
            and_(
                Location.country == country,
                Trip.start_date >= start_date,
                Trip.start_date <= end_date,
                Trip.is_active == True
            )
        ).group_by(Location.region).order_by(
            func.count(Trip.id).desc()
        ).all()
        
        return [
            {
                'region': row.region,
                'country': country,
                'trip_count': row.trip_count,
                'timeframe': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            }
            for row in result
        ]

class CRUDFeedback:
    def get(self, db: Session, id: str) -> Optional[Feedback]:
        return db.query(Feedback).filter(Feedback.id == id).first()
    
    def get_by_activity(self, db: Session, activity_id: str) -> List[Feedback]:
        return db.query(Feedback).filter(Feedback.activity_id == activity_id).all()
    
    def get_by_user(self, db: Session, user_id: str) -> List[Feedback]:
        return db.query(Feedback).filter(Feedback.user_id == user_id).all()
    
    def create(self, db: Session, obj_in: FeedbackCreate, user_id: str) -> Feedback:
        db_obj = Feedback(
            id=str(uuid.uuid4()),
            user_id=user_id,
            activity_id=obj_in.activity_id,
            score=obj_in.score,
            comment=obj_in.comment
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: Feedback, obj_in: FeedbackUpdate) -> Feedback:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: str) -> bool:
        obj = db.query(Feedback).filter(Feedback.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

# Create instances
user_crud = CRUDUser()
location_crud = CRUDLocation()
activity_crud = CRUDActivity()
trip_crud = CRUDTrip()
feedback_crud = CRUDFeedback()

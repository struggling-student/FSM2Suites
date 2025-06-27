from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
from datetime import datetime

# Association table for trip participants
trip_participants = Table(
    'trip_participants',
    Base.metadata,
    Column('trip_id', String, ForeignKey('trips.id'), primary_key=True),
    Column('user_id', String, ForeignKey('users.id'), primary_key=True)
)

# Association table for activity participants
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', String, ForeignKey('activities.id'), primary_key=True),
    Column('user_id', String, ForeignKey('users.id'), primary_key=True)
)

class ActivityType(enum.Enum):
    VISIT = "visit"
    MEAL = "meal"
    TOUR = "tour"
    TRANSPORT = "transport"
    OVERNIGHT_STAY = "overnight_stay"

class TripStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELED = "canceled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    city_of_origin = Column(String, nullable=False)
    registration_date = Column(DateTime, default=func.now())
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    organized_trips = relationship("Trip", back_populates="organizer", foreign_keys="Trip.organizer_id")
    participated_trips = relationship("Trip", secondary=trip_participants, back_populates="participants")
    feedback_given = relationship("Feedback", back_populates="user")
    
    @property
    def rating(self) -> float:
        """Calculate user rating based on feedback received for activities in organized trips"""
        if not self.organized_trips:
            return 0.0
        
        all_feedback = []
        for trip in self.organized_trips:
            for activity in trip.activities:
                all_feedback.extend(activity.feedback)
        
        if not all_feedback:
            return 0.0
        
        avg_rating = sum(f.score for f in all_feedback) / len(all_feedback)
        
        # Calculate rating according to requirements
        if avg_rating <= 3:
            return 0.0
        else:
            high_scores = sum(1 for f in all_feedback if f.score >= 4)
            return min(5.0, 0.1 * high_scores)

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(String, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)
    country = Column(String, nullable=False)
    
    # Relationships
    activities = relationship("Activity", back_populates="location", foreign_keys="Activity.location_id")
    departure_activities = relationship("Activity", back_populates="departure_location", foreign_keys="Activity.departure_location_id")
    arrival_activities = relationship("Activity", back_populates="arrival_location", foreign_keys="Activity.arrival_location_id")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    min_participants = Column(Integer, nullable=False)
    max_participants = Column(Integer, nullable=False)
    organizer_id = Column(String, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    status = Column(SQLEnum(TripStatus), nullable=False, default=TripStatus.DRAFT)
    
    # Relationships
    organizer = relationship("User", back_populates="organized_trips", foreign_keys=[organizer_id])
    participants = relationship("User", secondary=trip_participants, back_populates="participated_trips")
    activities = relationship("Activity", back_populates="trip", cascade="all, delete-orphan")
    
    @property
    def is_editable(self) -> bool:
        """Check if trip can be edited (only draft trips are editable)"""
        return self.status == TripStatus.DRAFT
    
    @property
    def total_price(self) -> float:
        """Calculate total price of all activities in the trip"""
        return sum(activity.price for activity in self.activities)
    
    @property
    def destinations(self) -> list:
        """Get unique cities from all activities"""
        cities = set()
        for activity in self.activities:
            if activity.location:
                cities.add(activity.location.city)
        return list(cities)
    
    @property
    def regions(self) -> list:
        """Get unique regions from all activities"""
        regions = set()
        for activity in self.activities:
            if activity.location:
                regions.add(activity.location.region)
        return list(regions)

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(ActivityType), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    price = Column(Float, nullable=False, default=0.0)
    location_id = Column(String, ForeignKey("locations.id"), nullable=False)
    description = Column(Text)
    ticket_codes = Column(Text)  # JSON string of ticket codes
    trip_id = Column(String, ForeignKey("trips.id"), nullable=False)
    
    # For composite activities
    is_composite = Column(Boolean, default=False)
    parent_activity_id = Column(String, ForeignKey("activities.id"), nullable=True)
    
    # For transport activities
    departure_location_id = Column(String, ForeignKey("locations.id"), nullable=True)
    arrival_location_id = Column(String, ForeignKey("locations.id"), nullable=True)
    
    # For overnight stays
    check_in_time = Column(DateTime, nullable=True)
    check_out_time = Column(DateTime, nullable=True)
    
    # Relationships
    trip = relationship("Trip", back_populates="activities")
    location = relationship("Location", back_populates="activities", foreign_keys=[location_id])
    departure_location = relationship("Location", back_populates="departure_activities", foreign_keys=[departure_location_id])
    arrival_location = relationship("Location", back_populates="arrival_activities", foreign_keys=[arrival_location_id])
    participants = relationship("User", secondary=activity_participants)
    feedback = relationship("Feedback", back_populates="activity", cascade="all, delete-orphan")
    
    # Self-referential relationship for composite activities
    sub_activities = relationship("Activity", backref="parent_activity", remote_side=[id])

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_id = Column(String, ForeignKey("activities.id"), nullable=False)
    score = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feedback_given")
    activity = relationship("Activity", back_populates="feedback")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure score is between 1 and 5
        if self.score < 1:
            self.score = 1
        elif self.score > 5:
            self.score = 5

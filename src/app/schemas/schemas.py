from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Union
from datetime import datetime
from app.models.models import ActivityType, TripStatus

# Location schemas
class LocationBase(BaseModel):
    address: str
    city: str
    region: str
    country: str

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    pass

class Location(LocationBase):
    id: str
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    city_of_origin: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    city_of_origin: Optional[str] = None

class UserInDB(UserBase):
    id: str
    registration_date: datetime
    is_active: bool
    rating: float
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Activity schemas
class ActivityBase(BaseModel):
    name: str
    type: ActivityType
    start_time: datetime
    duration: int
    price: float
    description: Optional[str] = None
    ticket_codes: Optional[str] = None
    is_composite: bool = False
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None

class ActivityCreate(ActivityBase):
    location: LocationCreate
    departure_location: Optional[LocationCreate] = None
    arrival_location: Optional[LocationCreate] = None
    participant_ids: Optional[List[str]] = None

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ActivityType] = None
    start_time: Optional[datetime] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    ticket_codes: Optional[str] = None
    participant_ids: Optional[List[str]] = None

class Activity(ActivityBase):
    id: str
    location: Location
    departure_location: Optional[Location] = None
    arrival_location: Optional[Location] = None
    participants: List[User] = []
    
    class Config:
        from_attributes = True

# Trip schemas
class TripBase(BaseModel):
    name: str
    min_participants: int
    max_participants: int
    start_date: datetime
    end_date: datetime

class TripCreate(TripBase):
    activities: List[ActivityCreate] = []
    
    @validator('max_participants')
    def validate_max_participants(cls, v, values):
        if 'min_participants' in values and v <= values['min_participants']:
            raise ValueError('max_participants must be greater than min_participants')
        return v
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class TripUpdate(BaseModel):
    name: Optional[str] = None
    min_participants: Optional[int] = None
    max_participants: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Trip(TripBase):
    id: str
    organizer: User
    participants: List[User] = []
    activities: List[Activity] = []
    total_price: float
    destinations: List[str]
    regions: List[str]
    created_at: datetime
    is_active: bool
    status: TripStatus
    is_editable: bool
    
    class Config:
        from_attributes = True

# Feedback schemas
class FeedbackBase(BaseModel):
    score: int
    comment: Optional[str] = None
    
    @validator('score')
    def validate_score(cls, v):
        if v < 1 or v > 5:
            raise ValueError('score must be between 1 and 5')
        return v

class FeedbackCreate(FeedbackBase):
    activity_id: str

class ActivityFeedbackCreate(FeedbackBase):
    """Schema for creating feedback via activity endpoint (activity_id comes from URL)"""
    pass

class FeedbackUpdate(BaseModel):
    score: Optional[int] = None
    comment: Optional[str] = None
    
    @validator('score')
    def validate_score(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('score must be between 1 and 5')
        return v

class Feedback(FeedbackBase):
    id: str
    user: User
    activity_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Feedback summary schemas
class ActivityFeedbackSummary(BaseModel):
    activity_id: str
    activity_name: str
    feedback_count: int
    average_score: Optional[float] = None

class TripFeedbackSummary(BaseModel):
    trip_id: str
    total_feedback_count: int
    average_score: Optional[float] = None
    activities: List[ActivityFeedbackSummary]

# Search and filter schemas
class TripSearchFilters(BaseModel):
    destination: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    regions: Optional[List[str]] = None
    min_organizer_rating: Optional[float] = None
    skip: int = 0
    limit: int = 100

class TripStatistics(BaseModel):
    city: str
    month: str
    year: int
    trip_count: int

class CityMonthlyStats(BaseModel):
    city: str
    country: str
    year: int
    monthly_stats: List[TripStatistics]

class RegionalStats(BaseModel):
    region: str
    country: str
    trip_count: int
    timeframe: str

class PopularDestination(BaseModel):
    city: str
    country: str
    visit_count: int
    rank: int

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response schemas
class TripListResponse(BaseModel):
    trips: List[Trip]
    total: int
    skip: int
    limit: int

class Message(BaseModel):
    message: str

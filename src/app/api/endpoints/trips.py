from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.crud.crud import trip_crud, user_crud
from app.schemas.schemas import (
    Trip, TripCreate, TripUpdate, TripListResponse, 
    TripSearchFilters, Message, User
)
from app.models.models import User as UserModel, Trip as TripModel
from app.api.endpoints.users import get_current_user

router = APIRouter()

@router.post("/", response_model=Trip, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip: TripCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new trip"""
    db_trip = trip_crud.create(db, obj_in=trip, organizer_id=current_user.id)
    return db_trip

@router.get("/", response_model=TripListResponse)
def get_trips(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    destination: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    min_budget: Optional[float] = Query(None),
    max_budget: Optional[float] = Query(None),
    regions: Optional[List[str]] = Query(None),
    min_organizer_rating: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of trips with optional filters"""
    filters = TripSearchFilters(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        min_budget=min_budget,
        max_budget=max_budget,
        regions=regions,
        min_organizer_rating=min_organizer_rating,
        skip=skip,
        limit=limit
    )
    
    if any([destination, start_date, end_date, min_budget, max_budget, regions, min_organizer_rating]):
        trips = trip_crud.search(db, filters)
    else:
        trips = trip_crud.get_multi(db, skip=skip, limit=limit)
    
    total = len(trips)  # In a real implementation, you'd want a separate count query
    
    return TripListResponse(
        trips=trips,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{trip_id}", response_model=Trip)
def get_trip(
    trip_id: str,
    db: Session = Depends(get_db)
):
    """Get trip by ID"""
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    return trip

@router.put("/{trip_id}", response_model=Trip)
def update_trip(
    trip_id: str,
    trip_update: TripUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update trip (only by organizer)"""
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    if trip.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the organizer can update this trip"
        )
    
    updated_trip = trip_crud.update(db, db_obj=trip, obj_in=trip_update)
    return updated_trip

@router.delete("/{trip_id}", response_model=Message)
def delete_trip(
    trip_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete trip (only by organizer)"""
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    if trip.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the organizer can delete this trip"
        )
    
    success = trip_crud.delete(db, id=trip_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete trip"
        )
    
    return Message(message="Trip deleted successfully")

@router.post("/{trip_id}/join", response_model=Message)
def join_trip(
    trip_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a trip"""
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    if current_user.id == trip.organizer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organizer cannot join their own trip"
        )
    
    success = trip_crud.add_participant(db, trip_id=trip_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot join trip (may be full or already joined)"
        )
    
    return Message(message="Successfully joined the trip")

@router.post("/{trip_id}/leave", response_model=Message)
def leave_trip(
    trip_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Leave a trip"""
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    success = trip_crud.remove_participant(db, trip_id=trip_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot leave trip (may not be a participant)"
        )
    
    return Message(message="Successfully left the trip")

@router.get("/my/organized", response_model=List[Trip])
def get_my_organized_trips(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get trips organized by current user"""
    trips = trip_crud.get_by_organizer(db, organizer_id=current_user.id, skip=skip, limit=limit)
    return trips

@router.get("/my/joined", response_model=List[Trip])
def get_my_joined_trips(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get trips joined by current user"""
    trips = trip_crud.get_by_participant(db, user_id=current_user.id, skip=skip, limit=limit)
    return trips

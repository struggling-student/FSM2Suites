from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.crud import activity_crud, trip_crud, feedback_crud
from app.schemas.schemas import Activity, ActivityCreate, ActivityUpdate, Message, Feedback, FeedbackCreate, FeedbackUpdate, ActivityFeedbackCreate
from app.models.models import User as UserModel, Feedback as FeedbackModel
from app.api.endpoints.users import get_current_user

router = APIRouter()

@router.get("/trip/{trip_id}", response_model=List[Activity])
def get_trip_activities(
    trip_id: str,
    db: Session = Depends(get_db)
):
    """Get all activities for a specific trip"""
    # Check if trip exists
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    activities = activity_crud.get_by_trip(db, trip_id=trip_id)
    return activities

@router.post("/trip/{trip_id}", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity(
    trip_id: str,
    activity: ActivityCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new activity for a trip"""
    # Check if trip exists and user is organizer
    trip = trip_crud.get(db, id=trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    if trip.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip organizer can add activities"
        )
    
    db_activity = activity_crud.create(db, obj_in=activity, trip_id=trip_id)
    return db_activity

@router.get("/{activity_id}", response_model=Activity)
def get_activity(
    activity_id: str,
    db: Session = Depends(get_db)
):
    """Get activity by ID"""
    activity = activity_crud.get(db, id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    return activity

@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: str,
    activity_update: ActivityUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update activity (only by trip organizer)"""
    activity = activity_crud.get(db, id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user is the trip organizer
    if activity.trip.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip organizer can update activities"
        )
    
    updated_activity = activity_crud.update(db, db_obj=activity, obj_in=activity_update)
    return updated_activity

@router.delete("/{activity_id}", response_model=Message)
def delete_activity(
    activity_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete activity (only by trip organizer)"""
    activity = activity_crud.get(db, id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user is the trip organizer
    if activity.trip.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip organizer can delete activities"
        )
    
    success = activity_crud.delete(db, id=activity_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete activity"
        )
    
    return Message(message="Activity deleted successfully")

# Feedback endpoints for activities
@router.post("/{activity_id}/feedback", response_model=Feedback, status_code=201)
def create_activity_feedback(
    activity_id: str,
    feedback_data: ActivityFeedbackCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create feedback for an activity"""
    # Check if activity exists
    activity = activity_crud.get(db, id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user is a participant in the trip that contains this activity
    trip = activity.trip
    if current_user not in trip.participants and current_user != trip.organizer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only provide feedback for activities in trips you participated in"
        )
    
    # Check if user already provided feedback for this activity
    existing_feedback = db.query(FeedbackModel).filter(
        FeedbackModel.user_id == current_user.id,
        FeedbackModel.activity_id == activity_id
    ).first()
    
    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already provided feedback for this activity"
        )
    
    # Create feedback with activity_id from URL path
    feedback_create = FeedbackCreate(
        activity_id=activity_id,
        score=feedback_data.score,
        comment=feedback_data.comment
    )
    
    db_feedback = feedback_crud.create(db, obj_in=feedback_create, user_id=current_user.id)
    return db_feedback

@router.get("/{activity_id}/feedback", response_model=List[Feedback])
def get_activity_feedback(
    activity_id: str,
    db: Session = Depends(get_db)
):
    """Get all feedback for an activity"""
    activity = activity_crud.get(db, id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    feedback_list = feedback_crud.get_by_activity(db, activity_id=activity_id)
    return feedback_list

# Additional feedback management endpoints need to be added to the feedback router
# These will be accessible via /api/v1/feedback/ prefix

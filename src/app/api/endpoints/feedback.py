from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.crud import feedback_crud, activity_crud, trip_crud
from app.schemas.schemas import Feedback, FeedbackCreate, FeedbackUpdate, Message, TripFeedbackSummary, ActivityFeedbackSummary
from app.models.models import User as UserModel, Feedback as FeedbackModel, Activity as ActivityModel
from app.api.endpoints.users import get_current_user

router = APIRouter()

@router.get("/my-feedback", response_model=List[Feedback])
def get_my_feedback_history(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's feedback history"""
    feedback = db.query(FeedbackModel).filter(
        FeedbackModel.user_id == current_user.id
    ).all()
    return feedback

@router.post("/activities/{activity_id}/feedback", response_model=Feedback, status_code=201)
def create_activity_feedback(
    activity_id: str,
    feedback: FeedbackCreate,
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already provided feedback for this activity"
        )
    
    # Create feedback with activity_id
    feedback_create = FeedbackCreate(
        activity_id=activity_id,
        score=feedback.score,
        comment=feedback.comment
    )
    
    db_feedback = feedback_crud.create(db, obj_in=feedback_create, user_id=current_user.id)
    return db_feedback

@router.get("/activities/{activity_id}/feedback", response_model=List[Feedback])
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

@router.get("/users/{user_id}/feedback", response_model=List[Feedback])
def get_user_feedback_history(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get feedback history for a user"""
    # Users can only see their own feedback history
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own feedback history"
        )
    
    feedback_list = feedback_crud.get_by_user(db, user_id=user_id)
    return feedback_list

@router.put("/feedback/{feedback_id}", response_model=Feedback)
def update_feedback(
    feedback_id: str,
    feedback_update: FeedbackUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update feedback (only by the user who created it)"""
    feedback = feedback_crud.get(db, id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own feedback"
        )
    
    updated_feedback = feedback_crud.update(db, db_obj=feedback, obj_in=feedback_update)
    return updated_feedback

@router.delete("/feedback/{feedback_id}", response_model=Message)
def delete_feedback(
    feedback_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete feedback (only by the user who created it)"""
    feedback = feedback_crud.get(db, id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own feedback"
        )
    
@router.delete("/{feedback_id}", status_code=204)
def delete_feedback(
    feedback_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete feedback (only by the user who created it)"""
    feedback = feedback_crud.get(db, id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own feedback"
        )
    
    success = feedback_crud.delete(db, id=feedback_id)
    if success:
        return Message(message="Feedback deleted successfully")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete feedback"
        )

@router.get("/trips/{trip_id}", response_model=TripFeedbackSummary)
def get_trip_feedback_summary(
    trip_id: str,
    db: Session = Depends(get_db)
):
    """Get feedback summary for all activities in a trip"""
    # Get all activities for the trip
    activities = db.query(ActivityModel).filter(ActivityModel.trip_id == trip_id).all()
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found or has no activities"
        )
    
    # Build activity summaries
    activity_summaries = []
    total_feedback_count = 0
    total_score = 0
    
    for activity in activities:
        feedback_list = feedback_crud.get_by_activity(db, activity_id=activity.id)
        feedback_count = len(feedback_list)
        
        if feedback_count > 0:
            activity_avg = sum(f.score for f in feedback_list) / feedback_count
            total_score += sum(f.score for f in feedback_list)
            total_feedback_count += feedback_count
        else:
            activity_avg = None
            
        activity_summaries.append(ActivityFeedbackSummary(
            activity_id=activity.id,
            activity_name=activity.name,
            feedback_count=feedback_count,
            average_score=activity_avg
        ))
    
    overall_average = total_score / total_feedback_count if total_feedback_count > 0 else None
    
    return TripFeedbackSummary(
        trip_id=trip_id,
        total_feedback_count=total_feedback_count,
        average_score=overall_average,
        activities=activity_summaries
    )

@router.get("/user/{user_id}", response_model=List[Feedback])
def get_user_feedback(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all feedback given by a specific user"""
    # Users can only see their own feedback, unless they're viewing public feedback
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own feedback"
        )
    
    feedback_list = feedback_crud.get_by_user(db, user_id=user_id)
    return feedback_list

@router.get("/{feedback_id}", response_model=Feedback)
def get_feedback(
    feedback_id: str,
    db: Session = Depends(get_db)
):
    """Get feedback by ID"""
    feedback = feedback_crud.get(db, id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    return feedback

@router.put("/{feedback_id}", response_model=Feedback)
def update_feedback(
    feedback_id: str,
    feedback_update: FeedbackUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update feedback (only by the user who created it)"""
    feedback = feedback_crud.get(db, id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own feedback"
        )
    
    updated_feedback = feedback_crud.update(db, db_obj=feedback, obj_in=feedback_update)
    return updated_feedback

@router.delete("/{feedback_id}", response_model=Message)
def delete_feedback(
    feedback_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete feedback (only by the user who created it)"""
    feedback = feedback_crud.get(db, id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own feedback"
        )
    
    success = feedback_crud.delete(db, id=feedback_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete feedback"
        )
    
    return Message(message="Feedback deleted successfully")

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_token
from app.crud.crud import user_crud, trip_crud
from app.schemas.schemas import User, UserCreate, UserUpdate, UserLogin, Token, Message, Trip
from app.models.models import User as UserModel

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = user_crud.get_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = user_crud.create(db, obj_in=user)
    return db_user

@router.post("/login", response_model=Token)
def login_user(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    user = user_crud.authenticate(
        db, email=user_credentials.email, password=user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> UserModel:
    """Get the current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.split(" ")[1]
    user_id = verify_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    updated_user = user_crud.update(db, db_obj=current_user, obj_in=user_update)
    return updated_user

@router.get("/users", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get list of users (for development purposes)"""
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=User)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get user by ID"""
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/me/trips", response_model=List[Trip])
def get_current_user_trips(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all trips for current user (both organized and participated)"""
    # Get trips organized by the user
    organized_trips = trip_crud.get_by_organizer(db, organizer_id=current_user.id, skip=0, limit=1000)
    
    # Get trips the user is participating in
    participated_trips = trip_crud.get_by_participant(db, user_id=current_user.id, skip=0, limit=1000)
    
    # Combine and deduplicate (in case user organized and participated in same trip)
    all_trips = []
    trip_ids = set()
    
    for trip in organized_trips + participated_trips:
        if trip.id not in trip_ids:
            all_trips.append(trip)
            trip_ids.add(trip.id)
    
    # Apply pagination
    return all_trips[skip:skip + limit]

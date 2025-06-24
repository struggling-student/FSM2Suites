from fastapi import APIRouter
from app.api.endpoints import users, trips, activities, feedback, statistics

api_router = APIRouter()

api_router.include_router(users.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trips.router, prefix="/trips", tags=["trips"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])

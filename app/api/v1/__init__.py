"""
API v1 routes
"""
from fastapi import APIRouter
from app.api.v1 import auth, users, anime, recommendations, watchlist, ratings, search, explain

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(anime.router, prefix="/anime", tags=["anime"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["watchlist"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
api_router.include_router(explain.router, prefix="/explain", tags=["explainability"])

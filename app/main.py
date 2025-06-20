from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from operations.auth import login_user, register_user
from schemas import models
from database.database import init_db
# from operations import register_user, login_user
from operations.user_operations import save_user_interests, save_user_survey, get_user_survey
from operations.tour_operations import save_tour_to_db, get_tour_by_id, get_popular_tours
from operations.recommendations import get_recommended_tours, get_fallback_recommendations
from operations.favorite_operations import add_favorite, remove_favorite, get_user_favorites, get_user_favorite_tour_ids
from parsing import parser
import requests
import os
from dotenv import load_dotenv
from database.redis_client import redis_client
import json

load_dotenv()
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8002/api/v1/search_location')

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Tour generation endpoints
@app.post("/generate_tour", response_model=List[models.Tour])
def generate_tour(request: models.GenerateTourRequest):
    """Generate tours based on user request"""
    try:
        # Call external API for tour generation
        response = requests.post(API_URL, json=request.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to generate tours")
        
        # Parse and save tours
        tours_data = response.json()
        generated_tours = []
        for tour_data in tours_data:
            tour = models.Tour(**tour_data)
            tour_id = save_tour_to_db(tour)
            tour.tour_id = tour_id
            generated_tours.append(tour)
        
        return generated_tours
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_url_tour", response_model=List[models.Tour])
def generate_url_tour(request: models.GenerateUrlTourRequest):
    """Generate tours from URL"""
    try:
        # Parse URL and generate tours
        tours_data = parser.parse_url(request.url)
        generated_tours = []
        for tour_data in tours_data:
            tour = models.Tour(**tour_data)
            tour_id = save_tour_to_db(tour, url=request.url)
            tour.tour_id = tour_id
            generated_tours.append(tour)
        
        return generated_tours
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tour retrieval endpoints
@app.get("/tour/{tour_id}", response_model=models.Tour)
def tour(tour_id: int, current_user_id: Optional[int] = None):
    """Get tour by ID"""
    cache_key = f"tour:{tour_id}"
    cached_tour_json = redis_client.get(cache_key)
    
    tour_obj = None
    if cached_tour_json:
        tour_obj = models.Tour(**json.loads(cached_tour_json))
    else:
        tour_obj = get_tour_by_id(tour_id)
        if not tour_obj:
            raise HTTPException(status_code=404, detail="Tour not found")
        # Cache the original tour object from DB
        redis_client.set(cache_key, tour_obj.json(), ex=600)

    # Check favorite status if user is provided, but don't cache this result
    if current_user_id:
        favorite_tour_ids = get_user_favorite_tour_ids(current_user_id)
        if tour_obj.tour_id in favorite_tour_ids:
            tour_obj.is_favorite = True
            
    return tour_obj

@app.get("/list_popular", response_model=List[models.Tour])
def list_popular(current_user_id: Optional[int] = None):
    """Get list of popular tours"""
    cache_key = "popular_tours"
    cached_tours_json = redis_client.get(cache_key)

    tours = []
    if cached_tours_json:
        tours_data = json.loads(cached_tours_json)
        tours = [models.Tour(**data) for data in tours_data]
    else:
        tours = get_popular_tours()
        # Cache the list of original tour objects
        redis_client.set(cache_key, json.dumps([t.dict() for t in tours]), ex=600)

    # Check favorite status for the list
    if current_user_id:
        favorite_tour_ids = get_user_favorite_tour_ids(current_user_id)
        for tour_item in tours:
            if tour_item.tour_id in favorite_tour_ids:
                tour_item.is_favorite = True

    return tours

# Favorite Endpoints
@app.post("/favorites", status_code=201)
def add_tour_to_favorites(request: models.FavoriteRequest):
    """Add a tour to user's favorites"""
    result = add_favorite(request.user_id, request.tour_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    # Invalidate user-specific favorite list cache
    redis_client.delete(f"user_favorites:{request.user_id}")
    return result

@app.delete("/favorites", status_code=200)
def remove_tour_from_favorites(request: models.FavoriteRequest):
    """Remove a tour from user's favorites"""
    result = remove_favorite(request.user_id, request.tour_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    # Invalidate user-specific favorite list cache
    redis_client.delete(f"user_favorites:{request.user_id}")
    return result

@app.get("/users/{user_id}/favorites", response_model=List[models.Tour])
def get_user_favorite_tours(user_id: int):
    """Get all favorite tours for a user"""
    cache_key = f"user_favorites:{user_id}"
    cached_favorites_json = redis_client.get(cache_key)
    if cached_favorites_json:
        fav_tours_data = json.loads(cached_favorites_json)
        return [models.Tour(**data) for data in fav_tours_data]

    favorite_tours = get_user_favorites(user_id)
    redis_client.set(cache_key, json.dumps([t.dict() for t in favorite_tours]), ex=300)
    return favorite_tours

# Recommendation endpoints
@app.post("/recommend_tours", response_model=models.RecommendationResponse)
def recommend_tours(request: models.TourRecommendationRequest):
    """Get tour recommendations based on request"""
    try:
        recommended_tours = get_recommended_tours(
            request.user_id,
            request.interests,
            request.preferred_locations,
            request.max_results
        )
        return models.RecommendationResponse(tours=recommended_tours)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user_recommendations/{user_id}", response_model=models.RecommendationResponse)
def user_recommendations(user_id: int, max_results: int = Query(5, ge=1, le=20)):
    """Get personalized tour recommendations for user"""
    try:
        # Recommendations are dynamic, so we get them first
        recommended_tours = get_recommended_tours(user_id, max_results=max_results)
        if not recommended_tours:
            recommended_tours = get_fallback_recommendations(max_results)
        
        # Check favorite status for recommended tours
        favorite_tour_ids = get_user_favorite_tour_ids(user_id)
        for tour_item in recommended_tours:
            if tour_item.tour_id in favorite_tour_ids:
                tour_item.is_favorite = True

        return models.RecommendationResponse(tours=recommended_tours, message="OK")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User preferences endpoints
@app.post("/user_interests/{user_id}")
def save_interests(user_id: int, interests: List[str]):
    """Save user interests"""
    result = save_user_interests(user_id, interests)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.post("/user_survey", response_model=models.SurveyResponse)
def save_survey(survey: models.UserSurvey):
    """Save user survey data"""
    result = save_user_survey(survey)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return models.SurveyResponse(**result)

@app.get("/user_survey/{user_id}")
def get_survey(user_id: int):
    """Get user survey data"""
    cache_key = f"user_survey:{user_id}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    result = get_user_survey(user_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    redis_client.set(cache_key, json.dumps(result["data"]), ex=600)
    return result["data"]

# Authentication endpoints
@app.post("/login", response_model=models.LoginResponse)
def login_endpoint(login_data: models.Login):
    """User login"""
    result = login_user(login_data)
    if result["status"] == "error":
        raise HTTPException(status_code=401, detail=result["message"])
    return models.LoginResponse(**result)

@app.post("/register", response_model=models.RegisterResponse)
def register_endpoint(register_data: models.Register):
    """User registration"""
    result = register_user(register_data)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return models.RegisterResponse(**result)

# Test endpoint
@app.get("/tests")
def tests():
    """Test endpoint"""
    return {"status": "ok", "message": "API is working"}

@app.get("/test-redis")
def test_redis():
    try:
        redis_client.set("test_key", "Hello from Backend!")
        value = redis_client.get("test_key")
        return {"status": "success", "value": value}
    except Exception as e:
        return {"status": "error", "message": str(e)}

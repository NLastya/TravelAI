from fastapi import FastAPI, HTTPException, Query
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from operations.auth import login_user, register_user
from schemas import models
from database.database import init_db
# from operations import register_user, login_user
from operations.user_operations import save_user_interests, save_user_survey, get_user_survey
from operations.tour_operations import save_tour_to_db, get_tour_by_id, get_popular_tours
from operations.recommendations import get_recommended_tours, get_fallback_recommendations
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
def tour(tour_id: int):
    """Get tour by ID"""
    cache_key = f"tour:{tour_id}"
    cached = redis_client.get(cache_key)
    if cached:
        return models.Tour(**json.loads(cached))
    tour = get_tour_by_id(tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    redis_client.set(cache_key, tour.json(), ex=600)  # 10 минут
    return tour

@app.get("/list_popular", response_model=List[models.Tour])
def list_popular():
    """Get list of popular tours"""
    cache_key = "popular_tours"
    cached = redis_client.get(cache_key)
    if cached:
        tours = [models.Tour(**item) for item in json.loads(cached)]
        return tours
    tours = get_popular_tours()
    redis_client.set(cache_key, json.dumps([tour.dict() for tour in tours]), ex=600)
    return tours

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
    cache_key = f"user_recommendations:{user_id}:{max_results}"
    cached = redis_client.get(cache_key)
    if cached:
        return models.RecommendationResponse(**json.loads(cached))
    try:
        recommended_tours = get_recommended_tours(user_id, max_results=max_results)
        if not recommended_tours:
            # Fallback to popular tours if no personalized recommendations
            recommended_tours = get_fallback_recommendations(max_results)
        response = models.RecommendationResponse(tours=recommended_tours, message="OK")
        redis_client.set(cache_key, response.json(), ex=300)  # 5 минут
        return response
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

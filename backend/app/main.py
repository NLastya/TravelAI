from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Union
from fastapi.middleware.cors import CORSMiddleware

from operations.auth import login_user, register_user
from schemas import models
from database.database import init_db, get_connection
# from operations import register_user, login_user
from operations.user_operations import save_user_interests, save_user_survey, get_user_survey, update_city_rating, get_city_rating, get_user_city_ratings, get_user_interests, get_visited_cities
from operations.tour_operations import save_tour_to_db, get_tour_by_id, get_popular_tours
from operations.recommendations import get_recommended_tours, get_fallback_recommendations
from operations.favorite_operations import add_favorite, remove_favorite, get_user_favorites, get_user_favorite_tour_ids
from operations.analytics_operations import start_city_view, end_city_view, get_user_city_analytics, get_active_city_views
from operations.city_operations import add_ready_city, get_ready_city
from operations.analytics_operations import save_city_view_event
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

    response = requests.post(API_URL, json=request.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to generate tours")
        
        # Parse and save tours
    tours_data = response.json()
    print(tours_data)
    generated_tours = []
    for tour_data in tours_data:
        tour = models.Tour(**tour_data)
        tour.description = "Увлекательный тур для всей семьи!"
        tour_id = save_tour_to_db(tour)
        tour.tour_id = tour_id
        generated_tours.append(tour)
        
    return generated_tours


@app.post("/generate_url_tour", response_model=List[models.Tour])
def generate_url_tour(request: models.GenerateUrlTourRequest):
    """Generate tours from URL"""
    try:
        # Parse URL and generate tours
        tours_data = parser.parse_url(request.url)
        generated_tours = []
        for tour_data in tours_data:
            tour = models.Tour(**tour_data)
            tour.description = "Увлекательный тур для всей семьи!"
            tour_id = save_tour_to_db(tour, url=request.url)
            tour.tour_id = tour_id
            generated_tours.append(tour)
        
        return generated_tours
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tour retrieval endpoints
@app.get("/tour/{tour_id}", response_model=Union[models.Tour, List[models.Tour]])
def tour(tour_id: str, current_user_id: Optional[int] = None):
    """Get tour by ID or all tours if tour_id == 'all'"""
    if tour_id == 'all':
        # Получить все туры из базы
        from operations.tour_operations import get_popular_tours
        tours = get_popular_tours()
        # Check favorite status for the list
        if current_user_id:
            favorite_tour_ids = get_user_favorite_tour_ids(current_user_id)
            for tour_item in tours:
                if tour_item.tour_id in favorite_tour_ids:
                    tour_item.is_favorite = True
        return tours
    
    tour_id = int(tour_id)
    cache_key = f"tour:{tour_id}"
    try:
        cached_tour_json = redis_client.get(cache_key)
    except Exception:
        cached_tour_json = None
    
    tour_obj = None
    if cached_tour_json:
        tour_obj = models.Tour(**json.loads(cached_tour_json))
    else:
        tour_obj = get_tour_by_id(tour_id)
        if not tour_obj:
            raise HTTPException(status_code=404, detail="Tour not found")
        # Cache the original tour object from DB
        try:
            redis_client.set(cache_key, tour_obj.json(), ex=600)
        except Exception:
            pass

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
    """Get personalized tour recommendations for user via AI_service"""
    interests = get_user_interests(user_id)
    visited_cities = get_visited_cities(user_id)
    survey_result = get_user_survey(user_id)
    if survey_result["status"] != "success":
        raise HTTPException(status_code=404, detail="User survey not found")
    survey = survey_result["data"]
    ai_url = os.getenv('AI_CITIES_URL', 'http://127.0.0.1:8002/api/v1/recommend_cities')
    payload = {
        "user_id": user_id,
        "interests": interests,
        "visited_cities": visited_cities,
        "survey": survey,
        "n": max_results
    }
    response = requests.post(ai_url, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"AI_service error: {response.text}")
    try:
        result = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI_service returned invalid JSON: {e}")
    return result

@app.get("/city_recommendations/{user_id}", response_model=models.RecommendationResponse)
def city_recommendations(user_id: int, max_results: int = Query(5, ge=1, le=20)):
    """Get tour recommendations based on city recommendations from AI_service"""
    interests = get_user_interests(user_id)
    visited_cities = get_visited_cities(user_id)
    survey_result = get_user_survey(user_id)
    if survey_result["status"] != "success":
        raise HTTPException(status_code=404, detail="User survey not found")
    survey = survey_result["data"]
    ai_url = os.getenv('AI_CITIES_URL', 'http://127.0.0.1:8002/api/v1/recommend_cities')
    payload = {
        "user_id": user_id,
        "interests": interests,
        "visited_cities": visited_cities,
        "survey": survey,
        "n": max_results
    }
    response = requests.post(ai_url, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"AI_service error: {response.text}")
    try:
        city_recs = response.json().get("cities", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI_service returned invalid JSON: {e}")
    if not city_recs:
        return models.RecommendationResponse(tours=[], message="No city recommendations")
    if not isinstance(city_recs, list):
        raise HTTPException(status_code=500, detail=f"AI_service returned wrong format: {city_recs}")
    conn = get_connection()
    cursor = conn.cursor()
    query = f"""
        SELECT tour_id FROM tours
        WHERE location IN ({','.join(['?']*len(city_recs))})
        ORDER BY rating DESC, relevance DESC
        LIMIT ?
    """
    params = city_recs + [max_results]
    try:
        cursor.execute(query, params)
        tour_ids = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    conn.close()
    recommended_tours = []
    for tour_id in tour_ids:
        tour = get_tour_by_id(tour_id)
        if tour:
            recommended_tours.append(tour)
    favorite_tour_ids = get_user_favorite_tour_ids(user_id)
    for tour_item in recommended_tours:
        if tour_item.tour_id in favorite_tour_ids:
            tour_item.is_favorite = True
    return models.RecommendationResponse(tours=recommended_tours, message="OK")

# User preferences endpoints
@app.post("/user_interests/{user_id}")
def save_interests(user_id: int, request: models.UserInterestsRequest):
    """Save user interests"""
    result = save_user_interests(user_id, request.interests)
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

@app.get("/user_survey/{user_id}", response_model=models.UserSurvey)
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

# Analytics endpoints
@app.post("/analytics/city-view/start", response_model=models.CityViewResponse)
def start_city_view_tracking(event: models.CityViewEvent):
    """Start tracking city view time"""
    result = start_city_view(event.user_id, event.city_name)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return models.CityViewResponse(**result)


@app.post("/analytics/city-view/end", response_model=models.CityViewResponse)
def end_city_view_tracking(event: models.CityViewEvent):
    """End tracking city view time and update analytics"""
    result = end_city_view(event.user_id, event.city_name)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return models.CityViewResponse(**result)


@app.get("/analytics/city-view/{user_id}", response_model=models.CityAnalyticsResponse)
def get_city_analytics(user_id: int):
    """Get user's city view analytics"""
    result = get_user_city_analytics(user_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result["data"]


@app.get("/analytics/city-view/{user_id}/active", response_model=models.ActiveViewsResponse)
def get_active_views(user_id: int):
    """Get list of cities currently being viewed by user"""
    active_cities = get_active_city_views(user_id)
    return {"active_cities": active_cities}

# City rating endpoints
@app.post("/rate_city", response_model=models.CityRatingResponse)
def rate_city(rating_data: models.CityRating):
    """Rate a city (1-5 stars)"""
    result = update_city_rating(rating_data.user_id, rating_data.city_name, rating_data.rating)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return models.RegisterResponse(**result)


@app.get("/city_rating/{user_id}/{city_name}", response_model=models.CityRatingData)
def get_city_rating_endpoint(user_id: int, city_name: str):
    """Get current rating for a specific city"""
    result = get_city_rating(user_id, city_name)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result["data"]

@app.get("/user_city_ratings/{user_id}", response_model=models.UserCityRatingsResponse)
def get_user_city_ratings_endpoint(user_id: int):
    """Get all city ratings for a user"""
    result = get_user_city_ratings(user_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result["data"]

# Ready cities endpoints
@app.post("/ready_cities", response_model=models.ReadyCityResponse)
def add_city_endpoint(city_data: models.ReadyCity):
    """Add a new city to ready_cities table"""
    result = add_ready_city(city_data)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return models.ReadyCityResponse(**result)


@app.get("/ready_cities/{city_id}")
def get_city_endpoint(city_id: int):
    """Get city by ID"""
    result = get_ready_city(city_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result["data"]

#ручка для ивента 2 минуты
@app.post("/analytics/city-view/event", response_model=models.CityViewEventResponse)
def save_city_view_event_endpoint(event: models.CityViewEventSimple):
    """Save city view event (user viewed city for more than 2 minutes)"""
    result = save_city_view_event(event.user_id, event.city_name)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return models.CityViewEventResponse(**result)
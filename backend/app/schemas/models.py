from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Place(BaseModel):
    name: str
    location: str
    rating: float
    date_start: str  # или используйте datetime.date, если нужно
    date_end: str    # или используйте datetime.date, если нужно
    description: str
    photo: str
    mapgeo_x: float
    mapgeo_y: float
    
    # Опционально: свойство для удобного доступа к координатам как списку
    @property
    def mapgeo(self) -> list[float]:
        return [self.mapgeo_x, self.mapgeo_y]

class Places(BaseModel):
    id_place: int
    name: str
    location: str
    rating: str
    date: str
    description: str = None,
    photo: str
    mapgeo: list

class Tour(BaseModel):
    tour_id: int
    title: str
    date: List[str]
    location: str
    rating: float
    relevance: float
    url: Optional[str] = None
    places: List[Places] = None
    categories: List[str] = None
    description: str = "Увлекательный тур для всей семьи!"
    is_favorite: Optional[bool] = False

class GenerateTourRequest(BaseModel):
    user_id: int
    data_start: str
    data_end: str
    location: str
    hobby: List[str]

class GenerateUrlTourRequest(BaseModel):
    url: str
    user_id: int
    data_start: str
    data_end: str

class TourRecommendationRequest(BaseModel):
    user_id: int
    interests: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    max_results: Optional[int] = 5

class RecommendationResponse(BaseModel):
    tours: List[Tour]
    message: str = None

class Login(BaseModel):
    login: str
    password: str

class LoginResponse(BaseModel):
    status: str
    user_id: Optional[int] = None
    name: Optional[str] = None
    city: Optional[str] = None
    message: Optional[str] = None

class Register(BaseModel):
    name: str
    city: str
    login: str
    password: str

class RegisterResponse(BaseModel):
    status: str
    user_id: Optional[int] = None
    message: Optional[str] = None

class UserSurvey(BaseModel):
    user_id: int
    gender: Optional[str] = None
    age_group: Optional[str] = None
    cities_5: Optional[str] = None
    cities_4: Optional[str] = None
    cities_3: Optional[str] = None
    cities_2: Optional[str] = None
    cities_1: Optional[str] = None
    izbrannoe: Optional[str] = None
    cities_prosmotr_more: Optional[str] = None
    cities_prosmotr_less: Optional[str] = None
    poznavatelnyj_kulturno_razvlekatelnyj: Optional[bool] = None
    delovoy: Optional[bool] = None
    etnicheskiy: Optional[bool] = None
    religioznyj: Optional[bool] = None
    sportivnyj: Optional[bool] = None
    obrazovatelnyj: Optional[bool] = None
    ekzotic: Optional[bool] = None
    ekologicheskiy: Optional[bool] = None
    selskij: Optional[bool] = None
    lechebno_ozdorovitelnyj: Optional[bool] = None
    sobytijnyj: Optional[bool] = None
    gornolyzhnyj: Optional[bool] = None
    morskie_kruizy: Optional[bool] = None
    plyazhnyj_otdykh: Optional[bool] = None
    s_detmi: Optional[bool] = None
    s_kompaniej_15_24: Optional[bool] = None
    s_kompaniej_25_44: Optional[bool] = None
    s_kompaniej_45_66: Optional[bool] = None
    s_semej: Optional[bool] = None
    v_odinochku: Optional[bool] = None
    paroj: Optional[bool] = None
    kuhnya: Optional[str] = None

class SurveyResponse(BaseModel):
    status: str
    message: Optional[str] = None

class CityRating(BaseModel):
    user_id: int
    city_name: str
    rating: int  # 1-5

class CityRatingResponse(BaseModel):
    status: str
    message: Optional[str] = None

class CityViewEvent(BaseModel):
    user_id: int
    city_name: str
    timestamp: str  # ISO
    action: str  # "start" or "end"

class CityViewResponse(BaseModel):
    status: str
    message: Optional[str] = None

class FavoriteRequest(BaseModel):
    user_id: int
    tour_id: int

class ReadyCity(BaseModel):
    id: Optional[int] = None
    city: str
    federal_district: Optional[str] = None
    region: Optional[str] = None
    fias_level: Optional[int] = None
    capital_marker: Optional[int] = None
    population: Optional[int] = None
    foundation_year: Optional[int] = None
    features: Optional[str] = None

class ReadyCityResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[ReadyCity] = None

class UserInterestsRequest(BaseModel):
    interests: str

class CityAnalytics(BaseModel):
    city_name: str
    total_view_time: int
    view_count: int
    last_viewed: Optional[str] = None

class CityAnalyticsResponse(BaseModel):
    cities_prosmotr_more: List[str]
    cities_prosmotr_less: List[str]
    total_cities_viewed: int

class ActiveViewsResponse(BaseModel):
    active_cities: str

class CityRatingData(BaseModel):
    city_name: str
    rating: int
    timestamp: str

class UserCityRatingsResponse(BaseModel):
    ratings: List[CityRatingData]
#для последней фигни
class CityViewEventResponse(BaseModel):
    status: str
    message: Optional[str] = None

class CityViewEventSimple(BaseModel):
    user_id: int
    city_name: str
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Модели данных
class Place(BaseModel):
    id_place: int
    name: str
    location: str
    rating: float
    date_start: str
    date_end: str
    description: Optional[str] = None
    photo: Optional[str] = None
    mapgeo: List[float]  # [latitude, longitude]


class Tour(BaseModel):
    tour_id: int
    title: str
    date: List[str]  # [start, end] в формате 'dd:mm:yyyy'
    location: str
    rating: float
    relevance: float
    places: Optional[List] = None


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
    message: str


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
    gender: str
    age_group: str
    cities_5: Optional[str] = None
    cities_4: Optional[str] = None
    cities_3: Optional[str] = None
    cities_2: Optional[str] = None
    cities_1: Optional[str] = None
    izbrannoe: Optional[str] = None
    cities_prosmotr_more: Optional[str] = None
    cities_prosmotr_less: Optional[str] = None
    poznavatelnyj_kulturno_razvlekatelnyj: bool
    delovoy: bool
    etnicheskiy: bool
    religioznyj: bool
    sportivnyj: bool
    obrazovatelnyj: bool
    ekzotic: bool
    ekologicheskiy: bool
    selskij: bool
    lechebno_ozdorovitelnyj: bool
    sobytijnyj: bool
    gornolyzhnyj: bool
    morskie_kruizy: bool
    plyazhnyj_otdykh: bool
    s_detmi: bool
    s_kompaniej_15_24: bool
    s_kompaniej_25_44: bool
    s_kompaniej_45_66: bool
    s_semej: bool
    v_odinochku: bool
    paroj: bool
    kuhnya: bool


class SurveyResponse(BaseModel):
    status: str
    message: Optional[str] = None


class FavoriteRequest(BaseModel):
    user_id: int
    tour_id: int


class CityViewEvent(BaseModel):
    user_id: int
    city_name: str
    timestamp: str  # ISO format timestamp
    action: str  # "start" or "end"


class CityViewResponse(BaseModel):
    status: str
    message: Optional[str] = None


class CityRating(BaseModel):
    user_id: int
    city_name: str
    rating: int  # 1-5 звезд


class CityRatingResponse(BaseModel):
    status: str
    message: Optional[str] = None


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
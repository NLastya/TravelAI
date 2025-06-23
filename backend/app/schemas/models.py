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
    places: Optional[Places] = None


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
    liked_cities: str
    disliked_cities: str
    poznavatelnyj_kulturno_razvlekatelnyj: bool
    delovoy: bool
    etnicheskiy: bool
    religioznyj: bool
    sportivnyj: bool
    obrazovatelnyj: bool
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


class SurveyResponse(BaseModel):
    status: str
    message: Optional[str] = None


class FavoriteRequest(BaseModel):
    user_id: int
    tour_id: int
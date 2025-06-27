from fastapi import APIRouter, UploadFile, File, Form, Request, Response
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import asyncio
import app.internal.ml.model as llm
import app.internal.parsing.parser_selenium as parser
from pydantic import BaseModel
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import numpy as np
import os
import sqlite3
from app.internal.parsing.overpass import fetch_places_to_sqlite, translit_name
from datetime import datetime, timedelta
from app.internal.recommend_cities import recommend_cities
import threading
import requests

router = APIRouter(
    prefix="/api/v1"
)

load_dotenv()
api_key = os.getenv('API_MISTRAL')
api_key_openai = os.getenv('API_LLAMA_70B')
api_backend = os.getenv('API_BACKEND')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_URI = os.getenv('S3_HOST')
S3_PORT = os.getenv('S3_PORT')

# --- RECOMMEND CITIES MODEL GLOBALS ---
model_lock = threading.Lock()
city_model = None
city_df = None
city_dataset = None
city_user_features = None
city_item_features = None

# --- LIFESPAN EVENT ---
def on_startup():
    global city_model, city_df, city_dataset, city_user_features, city_item_features
    with model_lock:
        city_model, city_df, city_dataset, city_user_features, city_item_features = recommend_cities.train_model(
            'app/internal/recommend_cities/data.xlsx'
        )

from fastapi import Request, BackgroundTasks
from fastapi import status
from fastapi.responses import JSONResponse

@router.on_event("startup")
def startup_event():
    on_startup()

# --- ENDPOINT: TRAIN MODEL MANUALLY ---
@router.post("/train_cities")
def train_cities_endpoint():
    try:
        on_startup()
        return {"status": "ok", "message": "Model trained"}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

# --- ENDPOINT: RECOMMEND CITIES ---
from fastapi import Query

@router.get("/recommend_cities/{user_id}")
def recommend_cities_endpoint(user_id: int, n: int = Query(5, ge=1, le=20)):
    global city_model, city_df, city_dataset, city_user_features, city_item_features
    with model_lock:
        if city_model is None:
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"error": "Model not trained"})
        try:
            recs = recommend_cities.recommend(user_id, city_model, city_df, city_dataset, city_user_features, city_item_features, n=n)
            return {"user_id": user_id, "recommendations": recs}
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

@dataclass
class Generate(BaseModel):
    query: str
    model_type: str
    bucket_name: str
    file_names: list


class GenerateTourRequest(BaseModel):
    user_id: int
    data_start: str
    data_end: str
    location: str
    weather: list = None
    hobby: List[str]


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
    places: List[Places] = None


@router.post("/search_location", response_model=List[Tour])
def generate(data: GenerateTourRequest):
    import sqlite3

    def print_entire_database(db_name="places.db"):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        
        # Получаем список всех таблиц
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        
        print(f"\nСодержимое базы данных '{db_name}':")
        print("=" * 50)
        
        for table in tables:
            table_name = table[0]
            print(f"\nТаблица: {table_name}")
            print("-" * 40)
            
            # Получаем структуру таблицы
            cur.execute(f"PRAGMA table_info({table_name})")
            columns = cur.fetchall()
            column_names = [col[1] for col in columns]
            print("Структура:", ", ".join(column_names))
            
            # Получаем содержимое таблицы
            try:
                cur.execute(f"SELECT * FROM {table_name}")
                rows = cur.fetchall()
                
                if not rows:
                    print("Таблица пуста")
                    continue
                    
                # Выводим первые 5 строк (или все, если их меньше)
                max_rows_to_show = min(5, len(rows))
                print(f"Первые {max_rows_to_show} записей:")
                
                for i, row in enumerate(rows[:max_rows_to_show], 1):
                    print(f"{i}. {row}")
                    
                if len(rows) > max_rows_to_show:
                    print(f"... и еще {len(rows) - max_rows_to_show} записей")
                    
            except sqlite3.Error as e:
                print(f"Ошибка при чтении таблицы {table_name}: {e}")
        
        conn.close()
        print("\n" + "=" * 50 + "\n")

    # Пример использования
    print_entire_database()

    print(data)

    city = data.location
    weather_filters = data.weather or []
    hobbies = [h.lower() for h in data.hobby]
    db_name = "places.db"
    table_name = f"places_{translit_name(city)}"

    # Загружаем данные если таблица не существует
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if not cur.fetchone():
        conn.close()  # Закрываем соединение перед вызовом fetch_places_to_sqlite
        fetch_places_to_sqlite(city, db_name=db_name)
        conn = sqlite3.connect(db_name)  # Открываем новое соединение
    
    # Получаем данные
    cur = conn.cursor()
    cur.execute(f"""
        SELECT id, name, category, rating, opening_hours, latitude, longitude 
        FROM "{table_name}"
    """)

    rows = cur.fetchall()
    print(rows)
    conn.close()

    # --- Фильтрация по погоде и хобби ---

    def match_weather(place_cat: str) -> bool:
        weather_map = {
            'Ресторан': ['rain', 'snow'],
            'Музей': ['rain', 'snow'],
            'Историческое место': ['sun'],
            'Парк': ['sun'],
            'Достопримечательность': ['sun', 'snow']
        }
        allowed = weather_map.get(place_cat, ['sun', 'rain', 'snow'])
        return not weather_filters or any(w in allowed for w in weather_filters)

    def match_hobby(place_cat: str) -> bool:
        hobby_map = {
            'Ресторан': ['еда', 'кухня'],
            'Музей': ['искусство', 'история'],
            'Историческое место': ['история', 'архитектура'],
            'Парк': ['природа', 'отдых'],
            'Достопримечательность': ['фото', 'туризм']
        }
        tags = hobby_map.get(place_cat, [])
        return any(h in tags for h in hobbies)

    def calculate_avg_rating(places: List[Places]) -> float:
        ratings = []
        for p in places:
            try:
                ratings.append(float(p.rating))
            except (ValueError, TypeError):
                continue
        return round(sum(ratings) / len(ratings), 2) if ratings else 4.0

    # --- Фильтрация всех подходящих мест ---
    today = datetime.now().date().isoformat()
    filtered_places = []

    def get_wikimedia_image_url(place_name):
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "titles": place_name,
            "pithumbsize": 400
        }
        try:
            response = requests.get(url, params=params, timeout=2)
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                if "thumbnail" in page:
                    return page["thumbnail"]["source"]
        except Exception as e:
            print("Wiki image error:", e)
        return "https://via.placeholder.com/150"

    for (id_, name, category, rating, hours, lat, lon) in rows:
        '''if not match_weather(category):
            continue
        if not match_hobby(category):
            continue'''

        place = Places(
            id_place=id_,
            name=name,
            location=city,
            rating=rating,
            date=today,
            description=category,
            photo=get_wikimedia_image_url(name),
            mapgeo=[lat, lon]
        )
        filtered_places.append(place)

    # --- Разбиение по дням ---
    start_date = datetime.strptime(data.data_start, "%d.%m.%y")
    end_date = datetime.strptime(data.data_end, "%d.%m.%y")
    total_days = (end_date - start_date).days + 1
    places_per_day = 4
    tours = []
    tour_id = 0

    for day_index in range(total_days):  # Используем total_days вместо фиксированного 5
        tour_date = (start_date + timedelta(days=day_index)).strftime("%Y-%m-%d")
        daily_places = filtered_places[day_index * places_per_day:(day_index + 1) * places_per_day]

        if not daily_places:
            continue

        tour = Tour(
            tour_id=tour_id,
            title=f"Тур по {city} — день {day_index + 1}",
            date=[tour_date],
            location=city,
            rating=calculate_avg_rating(daily_places),
            relevance=1.0,
            places=daily_places
        )
        tours.append(tour)
        tour_id += 1

    print(tours)

    return tours

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

class CityRecommendationRequest(BaseModel):
    user_id: int
    interests: List[str]
    visited_cities: List[str]
    survey: UserSurvey
    n: int = 5

@router.post("/recommend_cities")
def recommend_cities_endpoint(request: CityRecommendationRequest):
    global city_model, city_df, city_dataset, city_user_features, city_item_features
    with model_lock:
        if city_model is None:
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"error": "Model not trained"})
        try:
            # Проверка наличия пользователя в модели
            if str(request.user_id) not in [str(uid) for uid in city_df.index]:
                return JSONResponse(status_code=404, content={"error": "User not found in recommendation model"})
            recs = recommend_cities.recommend(request.user_id, city_model, city_df, city_dataset, city_user_features, city_item_features, n=request.n)
            return {"cities": recs, "message": "OK"}
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})



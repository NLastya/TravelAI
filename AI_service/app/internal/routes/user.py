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
            photo="https://via.placeholder.com/150",
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



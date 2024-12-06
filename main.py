from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
import json
from datetime import datetime

# Путь к базе данных
DB_PATH = "tours.db"

# Инициализация FastAPI
app = FastAPI()

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
    places: Optional[List[Place]] = None


class GenerateTourRequest(BaseModel):
    user_id: int
    data_start: str
    data_end: str
    location: str
    hobby: List[str]


# Соединение с базой данных
def get_connection():
    return sqlite3.connect(DB_PATH)


# Функция для генерации туров
def generate_tours(data: GenerateTourRequest):
    conn = get_connection()
    cursor = conn.cursor()

    # Ищем туры по указанным параметрам
    cursor.execute("""
        SELECT tour_id, title, date_start, date_end, location, rating, relevance
        FROM tours
        WHERE location = ? AND date_start >= ? AND date_end <= ?
    """, (data.location, data.data_start, data.data_end))
    rows = cursor.fetchall()

    # Формируем ответ
    tours = []
    for row in rows:
        tours.append({
            "tour_id": row[0],
            "title": row[1],
            "date": [row[2], row[3]],
            "location": row[4],
            "rating": row[5],
            "relevance": row[6]
        })
    conn.commit()
    conn.close()
    return tours


# Функция для получения информации о туре по ID
def get_tour_by_id(tour_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем информацию о туре
    cursor.execute("""
        SELECT tour_id, title, date_start, date_end, location, rating, relevance
        FROM tours WHERE tour_id = ?
    """, (tour_id,))
    tour_row = cursor.fetchone()

    if not tour_row:
        conn.close()
        return None

    # Получаем места, связанные с туром
    cursor.execute("""
        SELECT id_place, name, location, rating, date_start, date_end, description, photo, mapgeo_x, mapgeo_y
        FROM places WHERE tour_id = ?
    """, (tour_id,))
    places_rows = cursor.fetchall()

    places = []
    for place in places_rows:
        places.append({
            "id_place": place[0],
            "name": place[1],
            "location": place[2],
            "rating": place[3],
            "date_start": place[4],
            "date_end": place[5],
            "description": place[6],
            "photo": place[7],
            "mapgeo": [place[8], place[9]]
        })

    conn.close()
    return {
        "tour_id": tour_row[0],
        "title": tour_row[1],
        "date": [tour_row[2], tour_row[3]],
        "location": tour_row[4],
        "rating": tour_row[5],
        "relevance": tour_row[6],
        "places": places
    }


# Функция для получения популярных туров
def get_popular_tours():
    conn = get_connection()
    cursor = conn.cursor()

    # Ищем популярные туры с рейтингом >= 4.5
    cursor.execute("""
        SELECT tour_id, title, date_start, date_end, location, rating, relevance
        FROM tours
        WHERE rating >= 4.5
    """)
    rows = cursor.fetchall()

    popular_tours = []
    for row in rows:
        popular_tours.append({
            "tour_id": row[0],
            "title": row[1],
            "date": [row[2], row[3]],
            "location": row[4],
            "rating": row[5],
            "relevance": row[6]
        })

    conn.close()
    return popular_tours


# Ручка для генерации туров
@app.post("/generate_tour", response_model=List[Tour])
def generate_tour(request: GenerateTourRequest):
    tours = generate_tours(request)
    return tours


# Ручка для получения информации о туре по ID
@app.get("/tour/{id_tour}", response_model=Tour)
def tour(id_tour: int):
    tour = get_tour_by_id(id_tour)
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour


# Ручка для получения списка популярных туров
@app.get("/list_popular", response_model=List[Tour])
def list_popular():
    popular_tours = get_popular_tours()
    return popular_tours

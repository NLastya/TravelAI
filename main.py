from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
import json
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import parser
import requests
import datetime

# Путь к базе данных
DB_PATH = "tours.db"

# Инициализация FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

list_tour = []
id_tour = []


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

    tours = []

    if rows:

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
    else:
        url = 'http://127.0.0.1:8002/api/v1/search_location'

        ans = parser.main(data.location)

        day_start, m_start, y_start = data.data_start.split(".")
        day_end, m_end, y_end = data.data_end.split(".")

        start_date = datetime.date(int(y_start), int(m_start), int(day_start))  # Замените 2024 на нужный год
        end_date = datetime.date(int(y_end), int(m_end), int(day_end))  # Замените 2024 на нужный год

        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime("%d.%m"))  # Формат даты можно изменить
            current_date += datetime.timedelta(days=1)

        weather = []

        for date in ans:
            if date[0] in dates:
                if "снег" in date[1] or "осадки" in date[1] or "дождь" in date[1]:
                    weather.append([date[0], "плохая"])
                else:
                    weather.append([date[0], "хорошая"])

        data_ = {
            'location': data.location,
            'weather': weather
        }

        print(weather)

        response = requests.post(url, json=data_)

        j = len(list_tour)

        for i in response.json()["tours"]:
            data_ = {
                "tour_id": j,
                "title": data.location,
                "date": [data.data_start, data.data_end],
                "location": data.location,
                "rating": 5,
                "relevance": 5,
                "places": [i]
            }

            list_tour.append(data_)
            tours.append(data_)
            j += 1

        for i in response.json()["places"]:
            id_tour.append({
                "name": i[0],
                "location": i[0],
                "rating": 4.9,
                "date_start": data.data_start,
                "date_end": data.data_end,
                "description": "good place",
                "photo": "",
                "mapgeo_x": "",
                "mapgeo_y": ""
            })

        # for i in range(len(list_tour) - 7, len(list_tour)):
        #     tours.append({
        #         "tour_id": i,
        #         "title": list_tour[i][0],
        #         "date": [data.data_start, data.data_end],
        #         "location": list_tour[i][0],
        #         "rating": 5,
        #         "relevance": 5,
        #         "places": [list_tour[i]]
        #     })

        print(id_tour)

    return tours


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
    return {"data": tours}


# Ручка для получения информации о туре по ID
@app.get("/tour/{id_tours}", response_model=Tour)
def tour(id_tours: int):
    # tour = get_tour_by_id(id_tour)
    # if not tour:
    #     raise HTTPException(status_code=404, detail="Tour not found")
    print()
    return list_tour[id_tours]
    # return id_tour[id_tours]
    # return tour


# Ручка для получения списка популярных туров
@app.get("/list_popular", response_model=List[Tour])
def list_popular():
    popular_tours = get_popular_tours()
    return popular_tours

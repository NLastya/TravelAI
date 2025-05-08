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
import hashlib
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение переменных окружения
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8002/api/v1/search_location')

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


class GenerateUrlTourRequest(BaseModel):
    url: str
    user_id: int
    data_start: str
    data_end: str


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


# Соединение с базой данных
def get_connection():
    return sqlite3.connect(DB_PATH)


# Хэширование пароля
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# Инициализация базы данных
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Создаем таблицу туров, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tours (
        tour_id INTEGER PRIMARY KEY,
        title TEXT,
        date_start TEXT,
        date_end TEXT,
        location TEXT,
        rating REAL,
        relevance REAL,
        url TEXT DEFAULT NULL
    )
    ''')
    
    # Создаем таблицу мест, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS places (
        id_place INTEGER PRIMARY KEY,
        tour_id INTEGER,
        name TEXT,
        location TEXT,
        rating REAL,
        date_start TEXT,
        date_end TEXT,
        description TEXT,
        photo TEXT,
        mapgeo_x REAL,
        mapgeo_y REAL,
        FOREIGN KEY (tour_id) REFERENCES tours(tour_id)
    )
    ''')
    
    # Создаем таблицу пользователей, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()


# Функция регистрации пользователя
def register_user(user_data: Register):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Проверяем, существует ли пользователь с таким логином
        cursor.execute("SELECT user_id FROM users WHERE login = ?", (user_data.login,))
        if cursor.fetchone():
            return {"status": "error", "message": "Пользователь с таким логином уже существует"}
        
        # Хэшируем пароль перед сохранением
        hashed_password = hash_password(user_data.password)
        
        # Добавляем пользователя в базу данных
        cursor.execute('''
        INSERT INTO users (name, city, login, password)
        VALUES (?, ?, ?, ?)
        ''', (
            user_data.name,
            user_data.city,
            user_data.login,
            hashed_password
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


# Функция авторизации пользователя
def login_user(login_data: Login):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Хэшируем введенный пароль
        hashed_password = hash_password(login_data.password)
        
        # Проверяем учетные данные
        cursor.execute('''
        SELECT user_id, name, city FROM users 
        WHERE login = ? AND password = ?
        ''', (login_data.login, hashed_password))
        
        user = cursor.fetchone()
        
        if user:
            return {
                "status": "success", 
                "user_id": user[0],
                "name": user[1],
                "city": user[2]
            }
        else:
            return {"status": "error", "message": "Неверный логин или пароль"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


# Функция для сохранения тура в базу данных
def save_tour_to_db(tour_data, url=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Добавляем тур в базу данных
    cursor.execute('''
    INSERT INTO tours (title, date_start, date_end, location, rating, relevance, url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        tour_data["title"],
        tour_data["date"][0],
        tour_data["date"][1],
        tour_data["location"],
        tour_data["rating"],
        tour_data["relevance"],
        url
    ))
    
    tour_id = cursor.lastrowid
    
    # Добавляем места для тура
    if tour_data.get("places"):
        for place in tour_data["places"]:
            if isinstance(place, dict):
                # Если place - это словарь с данными места
                mapgeo_x = place.get("mapgeo")[0] if place.get("mapgeo") else None
                mapgeo_y = place.get("mapgeo")[1] if place.get("mapgeo") else None
                
                cursor.execute('''
                INSERT INTO places (tour_id, name, location, rating, date_start, date_end, description, photo, mapgeo_x, mapgeo_y)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tour_id,
                    place.get("name"),
                    place.get("location"),
                    place.get("rating"),
                    place.get("date_start"),
                    place.get("date_end"),
                    place.get("description"),
                    place.get("photo"),
                    mapgeo_x,
                    mapgeo_y
                ))
            else:
                # Если place - это список или другой формат данных
                # В данном случае предполагаем, что это строка с названием места
                cursor.execute('''
                INSERT INTO places (tour_id, name, location, rating, date_start, date_end, description, photo, mapgeo_x, mapgeo_y)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tour_id,
                    str(place) if not isinstance(place, list) else place[0],
                    tour_data["location"],
                    4.5,
                    tour_data["date"][0],
                    tour_data["date"][1],
                    "Generated place",
                    "",
                    None,
                    None
                ))
    
    conn.commit()
    conn.close()
    
    return tour_id


# Функция для генерации туров по URL
def generate_tours_from_url(data: GenerateUrlTourRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Проверяем, есть ли уже туры по этому URL
    cursor.execute("""
        SELECT tour_id, title, date_start, date_end, location, rating, relevance
        FROM tours
        WHERE url = ?
    """, (data.url,))
    
    rows = cursor.fetchall()
    tours = []
    
    if rows:
        # Если туры с этим URL уже есть в базе, возвращаем их
        for row in rows:
            tour_id = row[0]
            tour = get_tour_by_id(tour_id)
            if tour:
                tours.append(tour)
                
        conn.close()
        return tours
    else:
        # Здесь код для парсинга URL и генерации тура на его основе
        # В этом примере просто создаем демо-тур
        # В реальном приложении здесь будет логика парсинга данных с URL
        
        # Предположим, что мы получили данные о местах из URL
        generated_places = [
            {
                "name": f"Place from {data.url}",
                "location": "Generated location",
                "rating": 4.8,
                "date_start": data.data_start,
                "date_end": data.data_end,
                "description": f"This place was generated from URL: {data.url}",
                "photo": "",
                "mapgeo": [55.75, 37.61]  # Пример координат
            }
        ]
        
        # Создаем тур на основе полученных данных
        tour_data = {
            "title": f"Tour from URL",
            "date": [data.data_start, data.data_end],
            "location": "Generated from URL",
            "rating": 4.7,
            "relevance": 4.5,
            "places": generated_places
        }
        
        # Сохраняем тур в базу данных
        tour_id = save_tour_to_db(tour_data, data.url)
        
        # Получаем полные данные о сохраненном туре
        tour = get_tour_by_id(tour_id)
        if tour:
            tours.append(tour)
    
    return tours


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
            tour_id = row[0]
            tour = get_tour_by_id(tour_id)
            if tour:
                tours.append(tour)

        conn.close()
    else:
        url = API_URL

        ans = parser.main(data.location)

        day_start, m_start, y_start = data.data_start.split(".")
        day_end, m_end, y_end = data.data_end.split(".")

        start_date = datetime.date(int(y_start), int(m_start), int(day_start))
        end_date = datetime.date(int(y_end), int(m_end), int(day_end))

        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime("%d.%m"))
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

        response = requests.post(url, json=data_)

        j = len(list_tour)

        for i in response.json()["tours"]:
            tour_data = {
                "title": data.location,
                "date": [data.data_start, data.data_end],
                "location": data.location,
                "rating": 5,
                "relevance": 5,
                "places": [i]
            }

            # Сохраняем тур в базу данных
            tour_id = save_tour_to_db(tour_data)
            
            # Получаем полные данные о сохраненном туре
            tour = get_tour_by_id(tour_id)
            if tour:
                tours.append(tour)
                
            # Для обратной совместимости
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

    return tours


def get_tour_by_id(tour_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем информацию о туре
    cursor.execute("""
        SELECT tour_id, title, date_start, date_end, location, rating, relevance, url
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
            "mapgeo": [place[8], place[9]] if place[8] is not None and place[9] is not None else []
        })

    conn.close()
    return {
        "tour_id": tour_row[0],
        "title": tour_row[1],
        "date": [tour_row[2], tour_row[3]],
        "location": tour_row[4],
        "rating": tour_row[5],
        "relevance": tour_row[6],
        "url": tour_row[7],
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
        tour_id = row[0]
        tour = get_tour_by_id(tour_id)
        if tour:
            popular_tours.append(tour)

    conn.close()
    return popular_tours


# Инициализируем базу данных при запуске
init_db()


# Ручка для генерации туров
@app.post("/generate_tour", response_model=List[Tour])
def generate_tour(request: GenerateTourRequest):
    tours = generate_tours(request)
    return tours


# Ручка для генерации туров из URL
@app.post("/generate_url_tour", response_model=List[Tour])
def generate_url_tour(request: GenerateUrlTourRequest):
    tours = generate_tours_from_url(request)
    return tours


# Ручка для получения информации о туре по ID
@app.get("/tour/{tour_id}", response_model=Tour)
def tour(tour_id: int):
    # Пробуем получить тур из базы данных
    tour = get_tour_by_id(tour_id)
    if tour:
        return tour
    
    # Для обратной совместимости
    if tour_id < len(list_tour):
        return list_tour[tour_id]
    
    raise HTTPException(status_code=404, detail="Tour not found")


# Ручка для получения списка популярных туров
@app.get("/list_popular", response_model=List[Tour])
def list_popular():
    popular_tours = get_popular_tours()
    return popular_tours


@app.post("/login", response_model=LoginResponse)
def login_endpoint(login_data: Login):
    result = login_user(login_data)
    return result


@app.post("/register", response_model=RegisterResponse)
def register_endpoint(register_data: Register):
    result = register_user(register_data)
    return result


@app.get("/tests")
def tests():
    return {"ans": "OK"}

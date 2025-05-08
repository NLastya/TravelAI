from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Dict, Any
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
import random

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
    interests: List[str]
    visited_cities: List[str]
    travel_frequency: Optional[str] = None  # например: "редко", "часто", "несколько раз в год"
    preferred_climate: Optional[str] = None  # например: "теплый", "холодный", "умеренный"
    preferred_activities: Optional[List[str]] = None  # например: ["пляжный отдых", "экскурсии", "горные лыжи"]
    travel_budget: Optional[str] = None  # например: "низкий", "средний", "высокий"
    additional_info: Optional[Dict[str, Any]] = None  # любая дополнительная информация


class SurveyResponse(BaseModel):
    status: str
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
    
    # Создаем таблицу интересов пользователей, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_interests (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        interest TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # Создаем таблицу категорий туров, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tour_categories (
        id INTEGER PRIMARY KEY,
        tour_id INTEGER,
        category TEXT NOT NULL,
        FOREIGN KEY (tour_id) REFERENCES tours(tour_id)
    )
    ''')
    
    # Создаем таблицу посещенных городов, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visited_cities (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        city_name TEXT NOT NULL,
        visit_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # Создаем таблицу для анкет пользователей, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_surveys (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        travel_frequency TEXT,
        preferred_climate TEXT,
        travel_budget TEXT,
        additional_info TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # Создаем таблицу для предпочитаемых активностей пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS preferred_activities (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        activity TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    conn.commit()
    conn.close()


# Функция для сохранения анкеты пользователя
def save_user_survey(survey_data: UserSurvey):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Проверяем существование пользователя
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (survey_data.user_id,))
        if not cursor.fetchone():
            return {"status": "error", "message": "Пользователь не найден"}
        
        # Сохраняем интересы пользователя
        save_user_interests(survey_data.user_id, survey_data.interests)
        
        # Сохраняем посещенные города
        # Сначала удаляем старые записи
        cursor.execute("DELETE FROM visited_cities WHERE user_id = ?", (survey_data.user_id,))
        
        # Добавляем новые записи
        for city in survey_data.visited_cities:
            cursor.execute('''
            INSERT INTO visited_cities (user_id, city_name, visit_date)
            VALUES (?, ?, ?)
            ''', (survey_data.user_id, city, datetime.datetime.now().strftime("%Y-%m-%d")))
        
        # Обновляем или добавляем данные анкеты
        cursor.execute("SELECT id FROM user_surveys WHERE user_id = ?", (survey_data.user_id,))
        if cursor.fetchone():
            # Обновляем существующую анкету
            cursor.execute('''
            UPDATE user_surveys
            SET travel_frequency = ?, preferred_climate = ?, travel_budget = ?, additional_info = ?
            WHERE user_id = ?
            ''', (
                survey_data.travel_frequency,
                survey_data.preferred_climate,
                survey_data.travel_budget,
                json.dumps(survey_data.additional_info) if survey_data.additional_info else None,
                survey_data.user_id
            ))
        else:
            # Создаем новую анкету
            cursor.execute('''
            INSERT INTO user_surveys (user_id, travel_frequency, preferred_climate, travel_budget, additional_info)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                survey_data.user_id,
                survey_data.travel_frequency,
                survey_data.preferred_climate,
                survey_data.travel_budget,
                json.dumps(survey_data.additional_info) if survey_data.additional_info else None
            ))
        
        # Обновляем предпочитаемые активности
        if survey_data.preferred_activities:
            # Удаляем старые активности
            cursor.execute("DELETE FROM preferred_activities WHERE user_id = ?", (survey_data.user_id,))
            
            # Добавляем новые активности
            for activity in survey_data.preferred_activities:
                cursor.execute('''
                INSERT INTO preferred_activities (user_id, activity)
                VALUES (?, ?)
                ''', (survey_data.user_id, activity))
        
        conn.commit()
        return {"status": "success", "message": "Анкета успешно сохранена"}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


# Функция для получения анкеты пользователя
def get_user_survey(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Получаем интересы пользователя
        interests = get_user_interests(user_id)
        
        # Получаем посещенные города
        cursor.execute("SELECT city_name FROM visited_cities WHERE user_id = ?", (user_id,))
        visited_cities = [row[0] for row in cursor.fetchall()]
        
        # Получаем данные анкеты
        cursor.execute('''
        SELECT travel_frequency, preferred_climate, travel_budget, additional_info
        FROM user_surveys
        WHERE user_id = ?
        ''', (user_id,))
        
        survey_row = cursor.fetchone()
        
        # Получаем предпочитаемые активности
        cursor.execute("SELECT activity FROM preferred_activities WHERE user_id = ?", (user_id,))
        preferred_activities = [row[0] for row in cursor.fetchall()]
        
        if survey_row:
            survey_data = {
                "user_id": user_id,
                "interests": interests,
                "visited_cities": visited_cities,
                "travel_frequency": survey_row[0],
                "preferred_climate": survey_row[1],
                "travel_budget": survey_row[2],
                "preferred_activities": preferred_activities,
                "additional_info": json.loads(survey_row[3]) if survey_row[3] else None
            }
            return survey_data
        else:
            # Если анкета еще не заполнена, возвращаем только базовые данные
            return {
                "user_id": user_id,
                "interests": interests,
                "visited_cities": visited_cities,
                "preferred_activities": preferred_activities
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


# Функция для получения списка посещенных городов пользователя
def get_visited_cities(user_id: int) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT city_name FROM visited_cities WHERE user_id = ?", (user_id,))
        cities = [row[0] for row in cursor.fetchall()]
        return cities
    except Exception as e:
        return []
    finally:
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


# Функция для сохранения интересов пользователя
def save_user_interests(user_id: int, interests: List[str]):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Удаляем старые интересы пользователя
        cursor.execute("DELETE FROM user_interests WHERE user_id = ?", (user_id,))
        
        # Добавляем новые интересы
        for interest in interests:
            cursor.execute('''
            INSERT INTO user_interests (user_id, interest)
            VALUES (?, ?)
            ''', (user_id, interest))
            
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


# Функция для получения интересов пользователя
def get_user_interests(user_id: int) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT interest FROM user_interests WHERE user_id = ?", (user_id,))
        interests = [row[0] for row in cursor.fetchall()]
        return interests
    except Exception as e:
        return []
    finally:
        conn.close()


# Функция для сохранения категорий тура
def save_tour_categories(tour_id: int, categories: List[str]):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Удаляем старые категории
        cursor.execute("DELETE FROM tour_categories WHERE tour_id = ?", (tour_id,))
        
        # Добавляем новые категории
        for category in categories:
            cursor.execute('''
            INSERT INTO tour_categories (tour_id, category)
            VALUES (?, ?)
            ''', (tour_id, category))
            
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


# Функция для получения категорий тура
def get_tour_categories(tour_id: int) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT category FROM tour_categories WHERE tour_id = ?", (tour_id,))
        categories = [row[0] for row in cursor.fetchall()]
        return categories
    except Exception as e:
        return []
    finally:
        conn.close()


# Функция для получения рекомендаций туров с учетом анкеты пользователя
def get_recommended_tours(user_id: int, interests: List[str] = None, 
                          preferred_locations: List[str] = None, max_results: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    
    recommended_tours = []
    
    try:
        # Если интересы не указаны, получаем их из БД
        if not interests:
            interests = get_user_interests(user_id)
        
        # Если предпочтительные локации не указаны, используем все доступные
        if not preferred_locations:
            # Получаем список локаций из предыдущих туров пользователя
            cursor.execute('''
            SELECT DISTINCT t.location FROM tours t
            JOIN tour_categories tc ON t.tour_id = tc.tour_id
            JOIN user_interests ui ON tc.category = ui.interest
            WHERE ui.user_id = ?
            ''', (user_id,))
            
            preferred_locations = [row[0] for row in cursor.fetchall()]
            
            # Если локаций нет, добавляем популярные локации
            if not preferred_locations:
                cursor.execute('''
                SELECT location, COUNT(*) as cnt 
                FROM tours 
                GROUP BY location 
                ORDER BY cnt DESC
                LIMIT 5
                ''')
                preferred_locations = [row[0] for row in cursor.fetchall()]
        
        # Получаем список городов, которые пользователь уже посетил
        visited_cities = get_visited_cities(user_id)
        
        # Строим запрос с учетом интересов и локаций
        # Исключаем города, которые пользователь уже посетил
        query = '''
        SELECT DISTINCT t.tour_id, t.title, t.date_start, t.date_end, t.location, t.rating, t.relevance,
               (CASE WHEN tc.category IS NOT NULL THEN 1 ELSE 0 END) as interest_match,
               (CASE WHEN t.location IN ({}) THEN 1 ELSE 0 END) as location_match,
               t.rating * 0.5 + (CASE WHEN tc.category IS NOT NULL THEN 1 ELSE 0 END) * 0.3 + 
               (CASE WHEN t.location IN ({}) THEN 1 ELSE 0 END) * 0.2 as score
        FROM tours t
        LEFT JOIN tour_categories tc ON t.tour_id = tc.tour_id AND tc.category IN ({})
        WHERE t.location NOT IN ({})
        ORDER BY score DESC
        LIMIT ?
        '''
        
        # Подготавливаем параметры для запроса
        placeholders_interests = ', '.join(['?' for _ in interests]) if interests else "''"
        placeholders_locations = ', '.join(['?' for _ in preferred_locations]) if preferred_locations else "''"
        placeholders_visited = ', '.join(['?' for _ in visited_cities]) if visited_cities else "''"
        
        query = query.format(placeholders_locations, placeholders_locations, placeholders_interests, placeholders_visited if visited_cities else "''")
        
        # Параметры запроса
        params = []
        if preferred_locations:
            params.extend(preferred_locations)
            params.extend(preferred_locations)
        if interests:
            params.extend(interests)
        if visited_cities:
            params.extend(visited_cities)
        params.append(max_results)
        
        if not interests and not preferred_locations:
            # Если нет интересов и предпочтительных локаций, возвращаем топ рейтинговые туры
            query = '''
            SELECT tour_id, title, date_start, date_end, location, rating, relevance
            FROM tours
            WHERE location NOT IN ({})
            ORDER BY rating DESC, relevance DESC
            LIMIT ?
            '''.format(placeholders_visited if visited_cities else "''")
            params = []
            if visited_cities:
                params.extend(visited_cities)
            params.append(max_results)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        for row in rows:
            tour_id = row[0]
            tour = get_tour_by_id(tour_id)
            if tour:
                recommended_tours.append(tour)
        
        # Если рекомендаций мало, добавляем популярные туры
        if len(recommended_tours) < max_results:
            remaining = max_results - len(recommended_tours)
            
            # Исключаем уже выбранные и посещенные города
            exclude_conditions = []
            exclude_params = []
            
            if recommended_tours:
                exclude_conditions.append("tour_id NOT IN ({})".format(', '.join([str(t['tour_id']) for t in recommended_tours])))
            
            if visited_cities:
                exclude_conditions.append("location NOT IN ({})".format(', '.join(['?' for _ in visited_cities])))
                exclude_params.extend(visited_cities)
            
            where_clause = " WHERE " + " AND ".join(exclude_conditions) if exclude_conditions else ""
            
            query = f'''
            SELECT tour_id FROM tours 
            {where_clause}
            ORDER BY rating DESC, relevance DESC
            LIMIT ?
            '''
            
            exclude_params.append(remaining)
            
            cursor.execute(query, exclude_params)
            
            additional_ids = cursor.fetchall()
            for row in additional_ids:
                tour_id = row[0]
                tour = get_tour_by_id(tour_id)
                if tour:
                    recommended_tours.append(tour)
        
        survey_message = "на основе вашей анкеты" if visited_cities or interests else ""
        
        return {
            "tours": recommended_tours,
            "message": f"Рекомендации сформированы {survey_message} с учетом ваших интересов и предпочтений." if interests or preferred_locations else "Рекомендованы популярные туры."
        }
    except Exception as e:
        return {
            "tours": get_fallback_recommendations(max_results, visited_cities),
            "message": f"Используем стандартные рекомендации. Ошибка: {str(e)}"
        }
    finally:
        conn.close()


# Функция для получения резервных рекомендаций в случае ошибки
def get_fallback_recommendations(max_results: int = 5, visited_cities: List[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        where_clause = ""
        params = []
        
        if visited_cities:
            where_clause = "WHERE location NOT IN ({})".format(', '.join(['?' for _ in visited_cities]))
            params.extend(visited_cities)
        
        query = f'''
        SELECT tour_id FROM tours 
        {where_clause}
        ORDER BY rating DESC, relevance DESC
        LIMIT ?
        '''
        
        params.append(max_results)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        recommendations = []
        
        for row in rows:
            tour_id = row[0]
            tour = get_tour_by_id(tour_id)
            if tour:
                recommendations.append(tour)
        
        # Если и здесь ничего не нашли, возвращаем пустой список
        return recommendations
    except:
        return []
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
            
            # Если у пользователя есть хобби, сохраняем их как категории тура
            if data.hobby:
                save_tour_categories(tour_id, data.hobby)
            
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


# Ручка для получения рекомендаций туров
@app.post("/recommend_tours", response_model=RecommendationResponse)
def recommend_tours(request: TourRecommendationRequest):
    recommendations = get_recommended_tours(
        user_id=request.user_id,
        interests=request.interests,
        preferred_locations=request.preferred_locations,
        max_results=request.max_results or 5
    )
    return recommendations


# Ручка для получения рекомендаций по интересам пользователя
@app.get("/user_recommendations/{user_id}", response_model=RecommendationResponse)
def user_recommendations(user_id: int, max_results: int = Query(5, ge=1, le=20)):
    # Получаем интересы пользователя из базы данных
    interests = get_user_interests(user_id)
    
    # Получаем рекомендации на основе интересов
    recommendations = get_recommended_tours(
        user_id=user_id,
        interests=interests,
        max_results=max_results
    )
    return recommendations


# Ручка для сохранения интересов пользователя
@app.post("/user_interests/{user_id}")
def save_interests(user_id: int, interests: List[str]):
    success = save_user_interests(user_id, interests)
    if success:
        return {"status": "success", "message": "Интересы пользователя сохранены"}
    else:
        raise HTTPException(status_code=500, detail="Ошибка при сохранении интересов")


# Ручка для сохранения анкеты пользователя
@app.post("/user_survey", response_model=SurveyResponse)
def save_survey(survey: UserSurvey):
    result = save_user_survey(survey)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


# Ручка для получения анкеты пользователя
@app.get("/user_survey/{user_id}")
def get_survey(user_id: int):
    survey = get_user_survey(user_id)
    if isinstance(survey, dict) and survey.get("status") == "error":
        raise HTTPException(status_code=400, detail=survey["message"])
    return survey


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

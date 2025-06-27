#!/usr/bin/env python3
"""
Скрипт для загрузки тестовых данных в базу через API endpoints
"""

import requests
import json
import time
from typing import List, Dict, Any

# Конфигурация
BASE_URL = "http://127.0.0.1:5173"  # URL вашего FastAPI сервера

def make_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """Выполнить HTTP запрос к API"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, json=data, headers=headers)
        else:
            raise ValueError(f"Неподдерживаемый метод: {method}")
        
        if response.status_code in [200, 201]:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "code": response.status_code, "message": response.text}
    
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Ошибка запроса: {str(e)}"}

def register_test_users() -> List[int]:
    """Регистрация тестовых пользователей"""
    print("=== Регистрация тестовых пользователей ===")
    
    test_users = [
        {
            "name": "Иван Петров",
            "city": "Москва",
            "login": "ivan_test",
            "password": "password123"
        },
        {
            "name": "Мария Сидорова",
            "city": "Санкт-Петербург",
            "login": "maria_test",
            "password": "password123"
        },
        {
            "name": "Алексей Козлов",
            "city": "Казань",
            "login": "alex_test",
            "password": "password123"
        }
    ]
    
    user_ids = []
    for user in test_users:
        result = make_request("POST", "/register", user)
        if result["status"] == "success":
            user_id = result["data"].get("user_id")
            if user_id:
                user_ids.append(user_id)
                print(f"✅ Пользователь {user['name']} зарегистрирован с ID: {user_id}")
            else:
                print(f"❌ Ошибка получения ID для пользователя {user['name']}")
        else:
            print(f"❌ Ошибка регистрации пользователя {user['name']}: {result.get('message', 'Неизвестная ошибка')}")
    
    return user_ids

def save_user_surveys(user_ids: List[int]):
    """Сохранение опросов пользователей"""
    print("\n=== Сохранение опросов пользователей ===")
    
    surveys = [
        {
            "user_id": user_ids[0],
            "gender": "male",
            "age_group": "25-34",
            "cities_5": "Москва,Санкт-Петербург",
            "cities_4": "Казань,Екатеринбург",
            "cities_3": "Новосибирск,Краснодар",
            "cities_2": "Волгоград,Самара",
            "cities_1": "Омск,Челябинск",
            "izbrannoe": "Москва,Санкт-Петербург",
            "cities_prosmotr_more": "Москва,Санкт-Петербург,Казань",
            "cities_prosmotr_less": "Омск,Челябинск",
            "poznavatelnyj_kulturno_razvlekatelnyj": True,
            "delovoy": False,
            "etnicheskiy": True,
            "religioznyj": False,
            "sportivnyj": False,
            "obrazovatelnyj": True,
            "ekzotic": False,
            "ekologicheskiy": True,
            "selskij": False,
            "lechebno_ozdorovitelnyj": False,
            "sobytijnyj": True,
            "gornolyzhnyj": False,
            "morskie_kruizy": False,
            "plyazhnyj_otdykh": False,
            "s_detmi": False,
            "s_kompaniej_15_24": False,
            "s_kompaniej_25_44": True,
            "s_kompaniej_45_66": False,
            "s_semej": False,
            "v_odinochku": False,
            "paroj": True,
            "kuhnya": "Русская,Итальянская"
        },
        {
            "user_id": user_ids[1],
            "gender": "female",
            "age_group": "18-24",
            "cities_5": "Санкт-Петербург,Москва",
            "cities_4": "Казань,Сочи",
            "cities_3": "Екатеринбург,Новосибирск",
            "cities_2": "Краснодар,Самара",
            "cities_1": "Волгоград,Омск",
            "izbrannoe": "Санкт-Петербург,Москва,Казань",
            "cities_prosmotr_more": "Санкт-Петербург,Москва,Казань,Сочи",
            "cities_prosmotr_less": "Волгоград,Омск",
            "poznavatelnyj_kulturno_razvlekatelnyj": True,
            "delovoy": False,
            "etnicheskiy": False,
            "religioznyj": False,
            "sportivnyj": True,
            "obrazovatelnyj": True,
            "ekzotic": True,
            "ekologicheskiy": False,
            "selskij": False,
            "lechebno_ozdorovitelnyj": False,
            "sobytijnyj": True,
            "gornolyzhnyj": True,
            "morskie_kruizy": True,
            "plyazhnyj_otdykh": True,
            "s_detmi": False,
            "s_kompaniej_15_24": True,
            "s_kompaniej_25_44": False,
            "s_kompaniej_45_66": False,
            "s_semej": False,
            "v_odinochku": True,
            "paroj": False,
            "kuhnya": "Японская,Итальянская,Мексиканская"
        }
    ]
    
    for survey in surveys:
        result = make_request("POST", "/user_survey", survey)
        if result["status"] == "success":
            print(f"✅ Опрос сохранен для пользователя {survey['user_id']}")
        else:
            print(f"❌ Ошибка сохранения опроса для пользователя {survey['user_id']}: {result.get('message', 'Неизвестная ошибка')}")

def save_user_interests(user_ids: List[int]):
    """Сохранение интересов пользователей"""
    print("\n=== Сохранение интересов пользователей ===")
    
    interests_data = [
        {
            "user_id": user_ids[0],
            "interests": "музеи,история,архитектура,театры,галереи"
        },
        {
            "user_id": user_ids[1],
            "interests": "спорт,горы,море,экстрим,путешествия"
        },
        {
            "user_id": user_ids[2],
            "interests": "кухня,культура,традиции,фото,блог"
        }
    ]
    
    for interest_data in interests_data:
        result = make_request("POST", f"/user_interests/{interest_data['user_id']}", {"interests": interest_data["interests"]})
        if result["status"] == "success":
            print(f"✅ Интересы сохранены для пользователя {interest_data['user_id']}")
        else:
            print(f"❌ Ошибка сохранения интересов для пользователя {interest_data['user_id']}: {result.get('message', 'Неизвестная ошибка')}")

def add_ready_cities():
    """Добавление готовых городов"""
    print("\n=== Добавление готовых городов ===")
    
    cities = [
        {
            "city": "Москва",
            "federal_district": "Центральный",
            "region": "Москва",
            "fias_level": 1,
            "capital_marker": 0,
            "population": 12506468,
            "foundation_year": 1147,
            "features": "Столица России, культурный центр"
        },
        {
            "city": "Санкт-Петербург",
            "federal_district": "Северо-Западный",
            "region": "Санкт-Петербург",
            "fias_level": 1,
            "capital_marker": 0,
            "population": 5384342,
            "foundation_year": 1703,
            "features": "Культурная столица России"
        },
        {
            "city": "Казань",
            "federal_district": "Приволжский",
            "region": "Татарстан",
            "fias_level": 1,
            "capital_marker": 1,
            "population": 1257391,
            "foundation_year": 1005,
            "features": "Столица Татарстана, исторический центр"
        },
        {
            "city": "Сочи",
            "federal_district": "Южный",
            "region": "Краснодарский край",
            "fias_level": 1,
            "capital_marker": 0,
            "population": 411524,
            "foundation_year": 1838,
            "features": "Курортный город, Олимпийская столица"
        },
        {
            "city": "Екатеринбург",
            "federal_district": "Уральский",
            "region": "Свердловская область",
            "fias_level": 1,
            "capital_marker": 1,
            "population": 1544376,
            "foundation_year": 1723,
            "features": "Столица Урала, промышленный центр"
        }
    ]
    
    for city in cities:
        result = make_request("POST", "/ready_cities", city)
        if result["status"] == "success":
            print(f"✅ Город {city['city']} добавлен")
        else:
            print(f"❌ Ошибка добавления города {city['city']}: {result.get('message', 'Неизвестная ошибка')}")

def add_city_ratings(user_ids: List[int]):
    """Добавление рейтингов городов"""
    print("\n=== Добавление рейтингов городов ===")
    
    ratings = [
        {"user_id": user_ids[0], "city_name": "Москва", "rating": 5},
        {"user_id": user_ids[0], "city_name": "Санкт-Петербург", "rating": 4},
        {"user_id": user_ids[0], "city_name": "Казань", "rating": 4},
        {"user_id": user_ids[1], "city_name": "Санкт-Петербург", "rating": 5},
        {"user_id": user_ids[1], "city_name": "Сочи", "rating": 4},
        {"user_id": user_ids[1], "city_name": "Москва", "rating": 3},
        {"user_id": user_ids[2], "city_name": "Казань", "rating": 5},
        {"user_id": user_ids[2], "city_name": "Екатеринбург", "rating": 3}
    ]
    
    for rating in ratings:
        result = make_request("POST", "/rate_city", rating)
        if result["status"] == "success":
            print(f"✅ Рейтинг {rating['rating']} для города {rating['city_name']} пользователя {rating['user_id']} добавлен")
        else:
            print(f"❌ Ошибка добавления рейтинга для города {rating['city_name']}: {result.get('message', 'Неизвестная ошибка')}")

def add_city_view_events(user_ids: List[int]):
    """Добавление событий просмотра городов"""
    print("\n=== Добавление событий просмотра городов ===")
    
    import datetime
    
    # События начала просмотра
    start_events = [
        {"user_id": user_ids[0], "city_name": "Москва", "timestamp": datetime.datetime.now().isoformat(), "action": "start"},
        {"user_id": user_ids[0], "city_name": "Санкт-Петербург", "timestamp": datetime.datetime.now().isoformat(), "action": "start"},
        {"user_id": user_ids[1], "city_name": "Сочи", "timestamp": datetime.datetime.now().isoformat(), "action": "start"}
    ]
    
    for event in start_events:
        result = make_request("POST", "/analytics/city-view/start", event)
        if result["status"] == "success":
            print(f"✅ Событие начала просмотра города {event['city_name']} пользователем {event['user_id']} добавлено")
        else:
            print(f"❌ Ошибка добавления события начала просмотра: {result.get('message', 'Неизвестная ошибка')}")
    
    # События просмотра более 2 минут
    view_events = [
        {"user_id": user_ids[0], "city_name": "Москва"},
        {"user_id": user_ids[0], "city_name": "Казань"},
        {"user_id": user_ids[1], "city_name": "Санкт-Петербург"}
    ]
    
    for event in view_events:
        result = make_request("POST", "/analytics/city-view/event", event)
        if result["status"] == "success":
            print(f"✅ Событие просмотра города {event['city_name']} пользователем {event['user_id']} добавлено")
        else:
            print(f"❌ Ошибка добавления события просмотра: {result.get('message', 'Неизвестная ошибка')}")

def test_api_endpoints(user_ids: List[int]):
    """Тестирование API endpoints"""
    print("\n=== Тестирование API endpoints ===")
    
    # Тест получения всех туров
    result = make_request("GET", "/tour/all")
    if result["status"] == "success":
        tours = result["data"]
        print(f"✅ Получено {len(tours)} туров")
    else:
        print(f"❌ Ошибка получения туров: {result.get('message', 'Неизвестная ошибка')}")
    
    # Тест получения популярных туров
    result = make_request("GET", "/list_popular")
    if result["status"] == "success":
        popular_tours = result["data"]
        print(f"✅ Получено {len(popular_tours)} популярных туров")
    else:
        print(f"❌ Ошибка получения популярных туров: {result.get('message', 'Неизвестная ошибка')}")
    
    # Тест получения опроса пользователя
    if user_ids:
        result = make_request("GET", f"/user_survey/{user_ids[0]}")
        if result["status"] == "success":
            print(f"✅ Опрос пользователя {user_ids[0]} получен")
        else:
            print(f"❌ Ошибка получения опроса: {result.get('message', 'Неизвестная ошибка')}")
    
    # Тест получения рекомендаций
    if user_ids:
        result = make_request("GET", f"/user_recommendations/{user_ids[0]}?max_results=3")
        if result["status"] == "success":
            print(f"✅ Рекомендации для пользователя {user_ids[0]} получены")
        else:
            print(f"❌ Ошибка получения рекомендаций: {result.get('message', 'Неизвестная ошибка')}")

def main():
    """Основная функция"""
    print("🚀 Начинаем загрузку тестовых данных...")
    
    # Проверяем доступность сервера
    result = make_request("GET", "/tests")
    if result["status"] != "success":
        print("❌ Сервер недоступен. Убедитесь, что FastAPI сервер запущен на http://127.0.0.1:5173")
        return
    
    print("✅ Сервер доступен")
    
    # Регистрируем пользователей
    user_ids = register_test_users()
    if not user_ids:
        print("❌ Не удалось зарегистрировать пользователей. Прерываем выполнение.")
        return
    
    # Добавляем данные
    save_user_surveys(user_ids)
    save_user_interests(user_ids)
    add_ready_cities()
    add_city_ratings(user_ids)
    add_city_view_events(user_ids)
    
    # Тестируем endpoints
    test_api_endpoints(user_ids)
    
    print("\n🎉 Загрузка тестовых данных завершена!")
    print(f"📊 Создано пользователей: {len(user_ids)}")
    print("📝 Для тестирования используйте следующие данные:")
    for i, user_id in enumerate(user_ids):
        print(f"   Пользователь {i+1}: ID={user_id}")

if __name__ == "__main__":
    main() 
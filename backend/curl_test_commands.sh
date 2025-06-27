#!/bin/bash

# Скрипт с curl командами для тестирования API
# Убедитесь, что сервер запущен на http://127.0.0.1:5173

BASE_URL="http://127.0.0.1:5173"

echo "🚀 Начинаем тестирование API с помощью curl..."

# 1. Тест доступности сервера
echo "=== Тест доступности сервера ==="
curl -X GET "$BASE_URL/tests" -H "Content-Type: application/json"

echo -e "\n\n"

# 2. Регистрация пользователей
echo "=== Регистрация пользователей ==="

echo "Регистрация пользователя 1:"
curl -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "city": "Москва",
    "login": "ivan_test",
    "password": "password123"
  }'

echo -e "\n\n"

echo "Регистрация пользователя 2:"
curl -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мария Сидорова",
    "city": "Санкт-Петербург",
    "login": "maria_test",
    "password": "password123"
  }'

echo -e "\n\n"

echo "Регистрация пользователя 3:"
curl -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Алексей Козлов",
    "city": "Казань",
    "login": "alex_test",
    "password": "password123"
  }'

echo -e "\n\n"

# 3. Вход пользователей (получение user_id)
echo "=== Вход пользователей ==="

echo "Вход пользователя 1:"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "ivan_test",
    "password": "password123"
  }'

echo -e "\n\n"

echo "Вход пользователя 2:"
curl -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "maria_test",
    "password": "password123"
  }'

echo -e "\n\n"

# 4. Сохранение опросов (замените USER_ID на реальные ID)
echo "=== Сохранение опросов ==="

echo "Опрос для пользователя 1:"
curl -X POST "$BASE_URL/user_survey" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
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
    "poznavatelnyj_kulturno_razvlekatelnyj": true,
    "delovoy": false,
    "etnicheskiy": true,
    "religioznyj": false,
    "sportivnyj": false,
    "obrazovatelnyj": true,
    "ekzotic": false,
    "ekologicheskiy": true,
    "selskij": false,
    "lechebno_ozdorovitelnyj": false,
    "sobytijnyj": true,
    "gornolyzhnyj": false,
    "morskie_kruizy": false,
    "plyazhnyj_otdykh": false,
    "s_detmi": false,
    "s_kompaniej_15_24": false,
    "s_kompaniej_25_44": true,
    "s_kompaniej_45_66": false,
    "s_semej": false,
    "v_odinochku": false,
    "paroj": true,
    "kuhnya": "Русская,Итальянская"
  }'

echo -e "\n\n"

echo "Опрос для пользователя 2:"
curl -X POST "$BASE_URL/user_survey" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
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
    "poznavatelnyj_kulturno_razvlekatelnyj": true,
    "delovoy": false,
    "etnicheskiy": false,
    "religioznyj": false,
    "sportivnyj": true,
    "obrazovatelnyj": true,
    "ekzotic": true,
    "ekologicheskiy": false,
    "selskij": false,
    "lechebno_ozdorovitelnyj": false,
    "sobytijnyj": true,
    "gornolyzhnyj": true,
    "morskie_kruizy": true,
    "plyazhnyj_otdykh": true,
    "s_detmi": false,
    "s_kompaniej_15_24": true,
    "s_kompaniej_25_44": false,
    "s_kompaniej_45_66": false,
    "s_semej": false,
    "v_odinochku": true,
    "paroj": false,
    "kuhnya": "Японская,Итальянская,Мексиканская"
  }'

echo -e "\n\n"

# 5. Сохранение интересов
echo "=== Сохранение интересов ==="

echo "Интересы пользователя 1:"
curl -X POST "$BASE_URL/user_interests/1" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "музеи,история,архитектура,театры,галереи"
  }'

echo -e "\n\n"

echo "Интересы пользователя 2:"
curl -X POST "$BASE_URL/user_interests/2" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "спорт,горы,море,экстрим,путешествия"
  }'

echo -e "\n\n"

echo "Интересы пользователя 3:"
curl -X POST "$BASE_URL/user_interests/3" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "кухня,культура,традиции,фото,блог"
  }'

echo -e "\n\n"

# 6. Добавление готовых городов
echo "=== Добавление готовых городов ==="

echo "Добавление Москвы:"
curl -X POST "$BASE_URL/ready_cities" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Москва",
    "federal_district": "Центральный",
    "region": "Москва",
    "fias_level": 1,
    "capital_marker": 0,
    "population": 12506468,
    "foundation_year": 1147,
    "features": "Столица России, культурный центр"
  }'

echo -e "\n\n"

echo "Добавление Санкт-Петербурга:"
curl -X POST "$BASE_URL/ready_cities" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Санкт-Петербург",
    "federal_district": "Северо-Западный",
    "region": "Санкт-Петербург",
    "fias_level": 1,
    "capital_marker": 0,
    "population": 5384342,
    "foundation_year": 1703,
    "features": "Культурная столица России"
  }'

echo -e "\n\n"

echo "Добавление Казани:"
curl -X POST "$BASE_URL/ready_cities" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Казань",
    "federal_district": "Приволжский",
    "region": "Татарстан",
    "fias_level": 1,
    "capital_marker": 1,
    "population": 1257391,
    "foundation_year": 1005,
    "features": "Столица Татарстана, исторический центр"
  }'

echo -e "\n\n"

# 7. Добавление рейтингов городов
echo "=== Добавление рейтингов городов ==="

echo "Рейтинг Москвы от пользователя 1:"
curl -X POST "$BASE_URL/rate_city" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Москва",
    "rating": 5
  }'

echo -e "\n\n"

echo "Рейтинг Санкт-Петербурга от пользователя 1:"
curl -X POST "$BASE_URL/rate_city" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Санкт-Петербург",
    "rating": 4
  }'

echo -e "\n\n"

echo "Рейтинг Казани от пользователя 2:"
curl -X POST "$BASE_URL/rate_city" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "city_name": "Казань",
    "rating": 5
  }'

echo -e "\n\n"

# 8. Добавление событий просмотра городов
echo "=== Добавление событий просмотра городов ==="

echo "Событие начала просмотра Москвы:"
curl -X POST "$BASE_URL/analytics/city-view/start" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Москва",
    "timestamp": "2024-01-15T10:00:00",
    "action": "start"
  }'

echo -e "\n\n"

echo "Событие просмотра Москвы более 2 минут:"
curl -X POST "$BASE_URL/analytics/city-view/event" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Москва"
  }'

echo -e "\n\n"

# 9. Тестирование получения данных
echo "=== Тестирование получения данных ==="

echo "Получение всех туров:"
curl -X GET "$BASE_URL/tour/all" -H "Content-Type: application/json"

echo -e "\n\n"

echo "Получение популярных туров:"
curl -X GET "$BASE_URL/list_popular" -H "Content-Type: application/json"

echo -e "\n\n"

echo "Получение опроса пользователя 1:"
curl -X GET "$BASE_URL/user_survey/1" -H "Content-Type: application/json"

echo -e "\n\n"

echo "Получение рекомендаций для пользователя 1:"
curl -X GET "$BASE_URL/user_recommendations/1?max_results=3" -H "Content-Type: application/json"

echo -e "\n\n"

echo "Получение рейтингов пользователя 1:"
curl -X GET "$BASE_URL/user_city_ratings/1" -H "Content-Type: application/json"

echo -e "\n\n"

echo "Получение аналитики пользователя 1:"
curl -X GET "$BASE_URL/analytics/city-view/1" -H "Content-Type: application/json"

echo -e "\n\n"

echo "🎉 Тестирование завершено!" 
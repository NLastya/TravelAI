# Быстрые команды curl для тестирования API

## Предварительные требования
Убедитесь, что FastAPI сервер запущен на `http://127.0.0.1:5173`

## 1. Тест доступности сервера
```bash
curl -X GET "http://127.0.0.1:5173/tests"
```

## 2. Регистрация пользователей

### Пользователь 1
```bash
curl -X POST "http://127.0.0.1:5173/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "city": "Москва",
    "login": "ivan_test",
    "password": "password123"
  }'
```

### Пользователь 2
```bash
curl -X POST "http://127.0.0.1:5173/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мария Сидорова",
    "city": "Санкт-Петербург",
    "login": "maria_test",
    "password": "password123"
  }'
```

### Пользователь 3
```bash
curl -X POST "http://127.0.0.1:5173/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Алексей Козлов",
    "city": "Казань",
    "login": "alex_test",
    "password": "password123"
  }'
```

## 3. Вход пользователей (для получения user_id)

### Вход пользователя 1
```bash
curl -X POST "http://127.0.0.1:5173/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "ivan_test",
    "password": "password123"
  }'
```

### Вход пользователя 2
```bash
curl -X POST "http://127.0.0.1:5173/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "maria_test",
    "password": "password123"
  }'
```

## 4. Сохранение опросов

### Опрос для пользователя 1
```bash
curl -X POST "http://127.0.0.1:5173/user_survey" \
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
```

### Опрос для пользователя 2
```bash
curl -X POST "http://127.0.0.1:5173/user_survey" \
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
```

## 5. Сохранение интересов

### Интересы пользователя 1
```bash
curl -X POST "http://127.0.0.1:5173/user_interests/1" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "музеи,история,архитектура,театры,галереи"
  }'
```

### Интересы пользователя 2
```bash
curl -X POST "http://127.0.0.1:5173/user_interests/2" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "спорт,горы,море,экстрим,путешествия"
  }'
```

### Интересы пользователя 3
```bash
curl -X POST "http://127.0.0.1:5173/user_interests/3" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "кухня,культура,традиции,фото,блог"
  }'
```

## 6. Добавление готовых городов

### Москва
```bash
curl -X POST "http://127.0.0.1:5173/ready_cities" \
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
```

### Санкт-Петербург
```bash
curl -X POST "http://127.0.0.1:5173/ready_cities" \
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
```

### Казань
```bash
curl -X POST "http://127.0.0.1:5173/ready_cities" \
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
```

## 7. Добавление рейтингов городов

### Рейтинг Москвы от пользователя 1
```bash
curl -X POST "http://127.0.0.1:5173/rate_city" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Москва",
    "rating": 5
  }'
```

### Рейтинг Санкт-Петербурга от пользователя 1
```bash
curl -X POST "http://127.0.0.1:5173/rate_city" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Санкт-Петербург",
    "rating": 4
  }'
```

### Рейтинг Казани от пользователя 2
```bash
curl -X POST "http://127.0.0.1:5173/rate_city" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "city_name": "Казань",
    "rating": 5
  }'
```

## 8. Добавление событий просмотра городов

### Событие начала просмотра Москвы
```bash
curl -X POST "http://127.0.0.1:5173/analytics/city-view/start" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Москва",
    "timestamp": "2024-01-15T10:00:00",
    "action": "start"
  }'
```

### Событие просмотра Москвы более 2 минут
```bash
curl -X POST "http://127.0.0.1:5173/analytics/city-view/event" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "city_name": "Москва"
  }'
```

## 9. Тестирование получения данных

### Получение всех туров
```bash
curl -X GET "http://127.0.0.1:5173/tour/all"
```

### Получение популярных туров
```bash
curl -X GET "http://127.0.0.1:5173/list_popular"
```

### Получение опроса пользователя 1
```bash
curl -X GET "http://127.0.0.1:5173/user_survey/1"
```

### Получение рекомендаций для пользователя 1
```bash
curl -X GET "http://127.0.0.1:5173/user_recommendations/1?max_results=3"
```

### Получение рейтингов пользователя 1
```bash
curl -X GET "http://127.0.0.1:5173/user_city_ratings/1"
```

### Получение аналитики пользователя 1
```bash
curl -X GET "http://127.0.0.1:5173/analytics/city-view/1"
```

### Получение активных просмотров пользователя 1
```bash
curl -X GET "http://127.0.0.1:5173/analytics/city-view/1/active"
```

## 10. Тестирование избранного

### Добавление тура в избранное
```bash
curl -X POST "http://127.0.0.1:5173/favorites" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "tour_id": 1
  }'
```

### Получение избранных туров пользователя
```bash
curl -X GET "http://127.0.0.1:5173/users/1/favorites"
```

### Удаление тура из избранного
```bash
curl -X DELETE "http://127.0.0.1:5173/favorites" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "tour_id": 1
  }'
```

## 11. Тестирование Redis
```bash
curl -X GET "http://127.0.0.1:5173/test-redis"
```

## Примечания

1. **Замените user_id** в командах на реальные ID, полученные при регистрации
2. **Замените tour_id** в командах на реальные ID туров из базы данных
3. Убедитесь, что все сервисы (FastAPI, Redis) запущены
4. Для Windows используйте Git Bash или WSL для выполнения curl команд 
# TravelAI Backend

## Запуск

```bash
  python -m venv venv
```

Включаем среду:

```bash
  source venv/bin/activate
```

Устанавливаем зависимости:

```bash
  pip install -r requirements.txt
```

Переходим в папку с проектом: 

```bash
  cd app
```

Запускаем проект:

```bash
  uvicorn main:app --port 8000 --reload
```

Redis
```bash
  docker run --name my-redis -d -p 6379:6379 redis
```

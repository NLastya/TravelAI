# TravelAI

##Запуск 

```bash
  cd AI_service
```

Создание виртуального окружения

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

Запуску проекта

```bash
  uvicorn app:create_app --port 8002
```


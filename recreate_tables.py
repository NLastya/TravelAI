import os
from database import init_db, DB_PATH

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Удалён файл базы данных: {DB_PATH}")
else:
    print(f"Файл базы данных не найден: {DB_PATH}")

init_db()
print("База данных успешно пересоздана!")

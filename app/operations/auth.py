import hashlib
from app.database.database import get_connection
from app.database import models


def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(user_data: models.Register):
    """Register a new user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT user_id FROM users WHERE login = ?", (user_data.login,))
        if cursor.fetchone():
            return {"status": "error", "message": "Пользователь с таким логином уже существует"}
        
        # Insert new user
        cursor.execute('''
        INSERT INTO users (name, city, login, password)
        VALUES (?, ?, ?, ?)
        ''', (
            user_data.name,
            user_data.city,
            user_data.login,
            hash_password(user_data.password)
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        return {
            "status": "success",
            "message": "Пользователь успешно зарегистрирован",
            "user_id": user_id
        }
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def login_user(login_data: models.Login):
    """Authenticate a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Find user by login
        cursor.execute('''
        SELECT user_id, name, city, password
        FROM users
        WHERE login = ?
        ''', (login_data.login,))
        
        user = cursor.fetchone()
        
        if not user:
            return {"status": "error", "message": "Пользователь не найден"}
        
        user_id, name, city, stored_password = user
        
        # Verify password
        if hash_password(login_data.password) != stored_password:
            return {"status": "error", "message": "Неверный пароль"}
        
        return {
            "status": "success",
            "message": "Успешный вход",
            "user_id": user_id,
            "name": name,
            "city": city
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close() 
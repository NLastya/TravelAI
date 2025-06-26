import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database.database import get_connection
from database.redis_client import redis_client
import json


def start_city_view(user_id: int, city_name: str) -> Dict:
    """Start tracking city view time"""
    try:
        # Store start time in Redis with expiration (24 hours)
        key = f"city_view:{user_id}:{city_name}"
        start_time = datetime.now().isoformat()
        redis_client.setex(key, 86400, start_time)  # 24 hours expiration
        
        return {"status": "success", "message": f"Started tracking view for {city_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def end_city_view(user_id: int, city_name: str) -> Dict:
    """End tracking city view time and update analytics"""
    try:
        # Get start time from Redis
        key = f"city_view:{user_id}:{city_name}"
        start_time_str = redis_client.get(key)
        
        if not start_time_str:
            return {"status": "error", "message": "No active view session found"}
        
        # Calculate view duration
        start_time = datetime.fromisoformat(start_time_str.decode())
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Remove from Redis
        redis_client.delete(key)
        
        # Update user survey with view data
        update_city_view_analytics(user_id, city_name, duration)
        
        return {
            "status": "success", 
            "message": f"View ended for {city_name}. Duration: {duration.total_seconds():.1f} seconds"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_city_view_analytics(user_id: int, city_name: str, duration: timedelta) -> None:
    """Update user survey with city view analytics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get current survey data
        cursor.execute('''
        SELECT cities_prosmotr_more, cities_prosmotr_less 
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if not row:
            # Create new survey record if doesn't exist
            cursor.execute('''
            INSERT INTO user_surveys (user_id, cities_prosmotr_more, cities_prosmotr_less)
            VALUES (?, '', '')
            ''', (user_id,))
            cities_more = ""
            cities_less = ""
        else:
            cities_more = row[0] or ""
            cities_less = row[1] or ""
        
        # Parse existing cities
        more_cities = set(cities_more.split(',')) if cities_more else set()
        less_cities = set(cities_less.split(',')) if cities_less else set()
        
        # Remove city from both lists if it exists
        more_cities.discard(city_name)
        less_cities.discard(city_name)
        
        # Add city to appropriate list based on duration
        if duration.total_seconds() > 120:  # > 2 minutes
            more_cities.add(city_name)
        else:
            less_cities.add(city_name)
        
        # Update database
        cursor.execute('''
        UPDATE user_surveys 
        SET cities_prosmotr_more = ?, cities_prosmotr_less = ?
        WHERE user_id = ?
        ''', (','.join(more_cities), ','.join(less_cities), user_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_user_city_analytics(user_id: int) -> Dict:
    """Get user's city view analytics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT cities_prosmotr_more, cities_prosmotr_less
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if not row:
            return {
                "status": "error",
                "message": "User survey not found"
            }
        
        cities_more = row[0] or ""
        cities_less = row[1] or ""
        
        return {
            "status": "success",
            "data": {
                "cities_prosmotr_more": cities_more.split(',') if cities_more else [],
                "cities_prosmotr_less": cities_less.split(',') if cities_less else [],
                "total_cities_viewed": len(cities_more.split(',')) + len(cities_less.split(',')) if cities_more or cities_less else 0
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


def get_active_city_views(user_id: int) -> List[str]:
    """Get list of cities currently being viewed by user"""
    try:
        pattern = f"city_view:{user_id}:*"
        keys = redis_client.keys(pattern)
        cities = []
        for key in keys:
            city_name = key.decode().split(':')[2]
            cities.append(city_name)
        return cities
    except Exception as e:
        return []


def cleanup_expired_views() -> None:
    """Clean up expired city view sessions (called periodically)"""
    try:
        # Redis automatically expires keys, but we can also clean up manually
        # This function can be called by a scheduled task
        pass
    except Exception as e:
        print(f"Error cleaning up expired views: {e}")
        
#для последней ручки
def save_city_view_event(user_id: int, city_name: str) -> Dict:
    """Save city view event (user viewed city for more than 2 minutes)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Get current survey data
        cursor.execute('''
        SELECT cities_prosmotr_more, cities_prosmotr_less 
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))

        row = cursor.fetchone()
        if not row:
            # Create new survey record if doesn't exist
            cursor.execute('''
            INSERT INTO user_surveys (user_id, cities_prosmotr_more, cities_prosmotr_less)
            VALUES (?, '', '')
            ''', (user_id,))
            cities_more = ""
            cities_less = ""
        else:
            cities_more = row[0] or ""
            cities_less = row[1] or ""

        # Parse existing cities
        more_cities = set(cities_more.split(',')) if cities_more else set()
        less_cities = set(cities_less.split(',')) if cities_less else set()

        # Remove city from both lists if it exists
        more_cities.discard(city_name)
        less_cities.discard(city_name)

        # Add city to "more" list since user viewed it for more than 2 minutes
        more_cities.add(city_name)

        # Update database
        cursor.execute('''
        UPDATE user_surveys 
        SET cities_prosmotr_more = ?, cities_prosmotr_less = ?
        WHERE user_id = ?
        ''', (','.join(more_cities), ','.join(less_cities), user_id))

        conn.commit()

        return {
            "status": "success",
            "message": f"Saved city view event for {city_name}"
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()
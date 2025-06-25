import sqlite3
from typing import Dict
from database.database import get_connection
from database.redis_client import redis_client
from schemas import models
import json


def add_ready_city(city_data: models.UserSurvey) -> Dict:
    """Add a new city to ready_cities table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO ready_cities (city, federal_district, region, fias_level, 
                                 capital_marker, population, foundation_year, features)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            city_data.city,
            city_data.federal_district,
            city_data.region,
            city_data.fias_level,
            city_data.capital_marker,
            city_data.population,
            city_data.foundation_year,
            city_data.features
        ))
        
        city_id = cursor.lastrowid
        conn.commit()
        
        # Invalidate cache for this city
        redis_client.delete(f"city:{city_id}")
        
        return {
            "status": "success",
            "message": f"City {city_data.city} added successfully",
            "data": {"id": city_id}
        }
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


def get_ready_city(city_id: int) -> Dict:
    """Get city by ID with Redis caching"""
    # Try to get from cache first
    cache_key = f"city:{city_id}"
    cached_city = redis_client.get(cache_key)
    
    if cached_city:
        city_data = json.loads(cached_city)
        return {"status": "success", "data": city_data}
    
    # If not in cache, get from database
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT id, city, federal_district, region, fias_level, 
               capital_marker, population, foundation_year, features
        FROM ready_cities WHERE id = ?
        ''', (city_id,))
        
        row = cursor.fetchone()
        if row:
            city_data = {
                "id": row[0],
                "city": row[1],
                "federal_district": row[2],
                "region": row[3],
                "fias_level": row[4],
                "capital_marker": row[5],
                "population": row[6],
                "foundation_year": row[7],
                "features": row[8]
            }
            
            # Cache the result for 10 minutes
            redis_client.setex(cache_key, 600, json.dumps(city_data))
            
            return {"status": "success", "data": city_data}
        else:
            return {"status": "error", "message": "City not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close() 
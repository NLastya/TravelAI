from typing import List
from database.database import get_connection
from schemas import models
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8002/api/v1/search_location')

def save_tour_categories(tour_id: int, categories: List[str]):
    """Save tour categories to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Delete existing categories
        cursor.execute("DELETE FROM tour_categories WHERE tour_id = ?", (tour_id,))
        
        # Insert new categories
        for category in categories:
            cursor.execute('''
            INSERT INTO tour_categories (tour_id, category)
            VALUES (?, ?)
            ''', (tour_id, category))
        
        conn.commit()
        return {"status": "success", "message": "Категории успешно сохранены"}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def get_tour_categories(tour_id: int) -> List[str]:
    """Get tour categories from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # cursor.execute("SELECT category FROM tour_categories WHERE tour_id = ?", (tour_id,))
        # return [row[0] for row in cursor.fetchall()]
        return []
    finally:
        conn.close()

def save_tour_to_db(tour_data, url=None):
    """Save tour data to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert tour
        cursor.execute('''
        INSERT INTO tours (title, date_start, date_end, location, rating, relevance, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tour_data.title,
            tour_data.date[0] if hasattr(tour_data, 'date') and len(tour_data.date) > 0 else None,
            tour_data.date[1] if hasattr(tour_data, 'date') and len(tour_data.date) > 1 else None,
            tour_data.location,
            tour_data.rating,
            tour_data.relevance,
            url
        ))
        
        tour_id = cursor.lastrowid
        
        # Insert places
        for place in tour_data.places:
            cursor.execute('''
            INSERT INTO places (tour_id, name, location, rating, date_start, date_end, 
                              description, photo, mapgeo_x, mapgeo_y)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tour_id,
                place.name,
                place.location,
                place.rating,
                getattr(place, 'date_start', None) if hasattr(place, 'date_start') else None,
                getattr(place, 'date_end', None) if hasattr(place, 'date_end') else None,
                place.description,
                place.photo,
                place.mapgeo[0],
                place.mapgeo[1]
            ))
        
        
        
        conn.commit()
        return tour_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_tour_by_id(tour_id: int):
    """Get tour data by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get tour data
        cursor.execute('''
        SELECT title, date_start, date_end, location, rating, relevance, url
        FROM tours
        WHERE tour_id = ?
        ''', (tour_id,))
        
        tour_row = cursor.fetchone()
        if not tour_row:
            return None
        
        # Get places
        cursor.execute('''
        SELECT name, location, rating, date_start, date_end, description, photo, mapgeo_x, mapgeo_y
        FROM places
        WHERE tour_id = ?
        ''', (tour_id,))
        
        places = []
        
        for place_row in cursor.fetchall():
            place_row = [0] + list(place_row)
            places.append(models.Places(
                id_place=place_row[0],
                name=place_row[1],
                location=place_row[2],
                rating=place_row[3],
                date=f"{place_row[4]} - {place_row[5]}" if place_row[4] and place_row[5] else str(place_row[4] or place_row[5]),
                description=place_row[6],
                photo=place_row[7],
                mapgeo=[place_row[8], place_row[9]]
            ))
        
        # Get categories
        categories = get_tour_categories(tour_id)
        
        return models.Tour(
            tour_id=tour_id,
            title=tour_row[0],
            date=[tour_row[1], tour_row[2]],
            location=tour_row[3],
            rating=tour_row[4],
            relevance=tour_row[5],
            url=tour_row[6],
            places=places,
            categories=categories
        )
    finally:
        conn.close()

def get_popular_tours():
    """Get popular tours from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT tour_id, title, date_start, date_end, location, rating, relevance, url
        FROM tours
        ORDER BY rating DESC, relevance DESC
        LIMIT 10
        ''')
        
        tours = []
        for row in cursor.fetchall():
            tour_id = row[0]
            tour = get_tour_by_id(tour_id)
            if tour:
                tours.append(tour)
        
        return tours
    finally:
        conn.close() 
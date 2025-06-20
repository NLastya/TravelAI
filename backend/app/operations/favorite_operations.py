import sqlite3
from typing import List
from database.database import get_connection
from operations.tour_operations import get_tour_by_id
from schemas import models

def add_favorite(user_id: int, tour_id: int):
    """Add a tour to user's favorites."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_favorites (user_id, tour_id) VALUES (?, ?)", (user_id, tour_id))
        conn.commit()
        return {"status": "success", "message": "Tour added to favorites"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Tour already in favorites or invalid IDs"}
    finally:
        conn.close()

def remove_favorite(user_id: int, tour_id: int):
    """Remove a tour from user's favorites."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM user_favorites WHERE user_id = ? AND tour_id = ?", (user_id, tour_id))
        conn.commit()
        if cursor.rowcount == 0:
            return {"status": "error", "message": "Favorite not found"}
        return {"status": "success", "message": "Tour removed from favorites"}
    finally:
        conn.close()

def get_user_favorite_tour_ids(user_id: int) -> List[int]:
    """Get a list of favorite tour IDs for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT tour_id FROM user_favorites WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()

def get_user_favorites(user_id: int) -> List[models.Tour]:
    """Get a list of favorite tours for a user."""
    favorite_tour_ids = get_user_favorite_tour_ids(user_id)
    if not favorite_tour_ids:
        return []
    
    tours = []
    for tour_id in favorite_tour_ids:
        tour = get_tour_by_id(tour_id)
        if tour:
            tour.is_favorite = True # Mark as favorite
            tours.append(tour)
            
    return tours 
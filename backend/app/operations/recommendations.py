from typing import List
from database.database import get_connection
from operations.tour_operations import get_tour_by_id

def get_recommended_tours(user_id: int, interests: List[str] = None, 
                         preferred_locations: List[str] = None, max_results: int = 5):
    """Get recommended tours based on user preferences"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get user interests if not provided
        if not interests:
            cursor.execute("SELECT interest FROM user_interests WHERE user_id = ?", (user_id,))
            interests = [row[0] for row in cursor.fetchall()]
        
        # Get visited cities
        cursor.execute("SELECT city_name FROM visited_cities WHERE user_id = ?", (user_id,))
        visited_cities = [row[0] for row in cursor.fetchall()]
        
        # Get user survey data (только существующие поля)
        cursor.execute('''
        SELECT gender, age_group, cities_5, cities_4, cities_3, cities_2, cities_1, izbrannoe, cities_prosmotr_more, cities_prosmotr_less,
               poznavatelnyj_kulturno_razvlekatelnyj, delovoy, etnicheskiy, religioznyj, sportivnyj, obrazovatelnyj, ekzotic, ekologicheskiy, selskij, lechebno_ozdorovitelnyj,
               sobytijnyj, gornolyzhnyj, morskie_kruizy, plyazhnyj_otdykh, s_detmi, s_kompaniej_15_24, s_kompaniej_25_44, s_kompaniej_45_66, s_semej, v_odinochku, paroj, kuhnya
        FROM user_surveys
        WHERE user_id = ?
        ''', (user_id,))
        survey_data = cursor.fetchone()
        # (survey_data не используется далее, но если нужно — используйте только эти поля)
        
        # Build query based on preferences
        query = '''
        SELECT DISTINCT t.tour_id
        FROM tours t
        WHERE 1=1
        '''
        params = []
        
        # Filter by interests (замокать: фильтровать по title если interests заданы)
        if interests:
            query += " AND (" + " OR ".join(["t.title LIKE ?" for _ in interests]) + ")"
            params.extend([f"%{interest}%" for interest in interests])
        
        # Filter by preferred locations
        if preferred_locations:
            query += " AND t.location IN ({})".format(','.join(['?'] * len(preferred_locations)))
            params.extend(preferred_locations)
        
        # Filter out visited cities
        if visited_cities:
            query += " AND t.location NOT IN ({})".format(','.join(['?'] * len(visited_cities)))
            params.extend(visited_cities)
        
        # Add ordering
        query += " ORDER BY t.rating DESC, t.relevance DESC LIMIT ?"
        params.append(max_results)
        
        # Execute query
        cursor.execute(query, params)
        tour_ids = [row[0] for row in cursor.fetchall()]
        
        # Get full tour data
        recommended_tours = []
        for tour_id in tour_ids:
            tour = get_tour_by_id(tour_id)
            if tour:
                recommended_tours.append(tour)
        
        return recommended_tours
    finally:
        conn.close()

def get_fallback_recommendations(max_results: int = 5, visited_cities: List[str] = None):
    """Get fallback recommendations when user preferences are not available"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = '''
        SELECT tour_id
        FROM tours
        WHERE 1=1
        '''
        params = []
        
        # Filter out visited cities if provided
        if visited_cities:
            query += " AND location NOT IN ({})".format(','.join(['?'] * len(visited_cities)))
            params.extend(visited_cities)
        
        # Add ordering and limit
        query += " ORDER BY rating DESC, relevance DESC LIMIT ?"
        params.append(max_results)
        
        cursor.execute(query, params)
        tour_ids = [row[0] for row in cursor.fetchall()]
        
        # Get full tour data
        recommended_tours = []
        for tour_id in tour_ids:
            tour = get_tour_by_id(tour_id)
            if tour:
                recommended_tours.append(tour)
        
        return recommended_tours
    finally:
        conn.close() 
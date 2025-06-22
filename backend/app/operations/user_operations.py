from typing import List, Dict
from database.database import get_connection
from database.redis_client import redis_client
from schemas import models


def save_user_interests(user_id: int, interests: List[str]):
    """Save user interests to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Delete existing interests
        cursor.execute("DELETE FROM user_interests WHERE user_id = ?", (user_id,))
        
        # Insert new interests
        for interest in interests:
            cursor.execute('''
            INSERT INTO user_interests (user_id, interest)
            VALUES (?, ?)
            ''', (user_id, interest))
        
        conn.commit()
        return {"status": "success", "message": "Интересы успешно сохранены"}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def get_user_interests(user_id: int) -> List[str]:
    """Get user interests from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT interest FROM user_interests WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()

def get_visited_cities(user_id: int) -> List[str]:
    """Get list of cities visited by user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT city_name FROM visited_cities WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()

def save_user_survey(survey_data: models.UserSurvey):
    """Save user survey data (new structure)"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Prepare values for insert/update
        values = (
            survey_data.user_id,
            survey_data.gender,
            survey_data.age_group,
            survey_data.cities_5,
            survey_data.cities_4,
            survey_data.cities_3,
            survey_data.cities_2,
            survey_data.cities_1,
            survey_data.izbrannoe,
            survey_data.cities_prosmotr_more,
            survey_data.cities_prosmotr_less,
            survey_data.poznavatelnyj_kulturno_razvlekatelnyj,
            survey_data.delovoy,
            survey_data.etnicheskiy,
            survey_data.religioznyj,
            survey_data.sportivnyj,
            survey_data.obrazovatelnyj,
            survey_data.ekzotic,
            survey_data.ekologicheskiy,
            survey_data.selskij,
            survey_data.lechebno_ozdorovitelnyj,
            survey_data.sobytijnyj,
            survey_data.gornolyzhnyj,
            survey_data.morskie_kruizy,
            survey_data.plyazhnyj_otdykh,
            survey_data.s_detmi,
            survey_data.s_kompaniej_15_24,
            survey_data.s_kompaniej_25_44,
            survey_data.s_kompaniej_45_66,
            survey_data.s_semej,
            survey_data.v_odinochku,
            survey_data.paroj,
            survey_data.kuhnya
        )
        # Check if survey exists
        cursor.execute("SELECT user_id FROM user_surveys WHERE user_id = ?", (survey_data.user_id,))
        if cursor.fetchone():
            cursor.execute('''
            UPDATE user_surveys SET
                gender=?, age_group=?, cities_5=?, cities_4=?, cities_3=?, cities_2=?, cities_1=?,
                izbrannoe=?, cities_prosmotr_more=?, cities_prosmotr_less=?,
                poznavatelnyj_kulturno_razvlekatelnyj=?, delovoy=?, etnicheskiy=?, religioznyj=?,
                sportivnyj=?, obrazovatelnyj=?, ekzotic=?, ekologicheskiy=?, selskij=?, lechebno_ozdorovitelnyj=?,
                sobytijnyj=?, gornolyzhnyj=?, morskie_kruizy=?, plyazhnyj_otdykh=?,
                s_detmi=?, s_kompaniej_15_24=?, s_kompaniej_25_44=?, s_kompaniej_45_66=?,
                s_semej=?, v_odinochku=?, paroj=?, kuhnya=?
            WHERE user_id = ?
            ''', values[1:] + (survey_data.user_id,))
        else:
            cursor.execute('''
            INSERT INTO user_surveys (
                user_id, gender, age_group, cities_5, cities_4, cities_3, cities_2, cities_1,
                izbrannoe, cities_prosmotr_more, cities_prosmotr_less,
                poznavatelnyj_kulturno_razvlekatelnyj, delovoy, etnicheskiy, religioznyj,
                sportivnyj, obrazovatelnyj, ekzotic, ekologicheskiy, selskij, lechebno_ozdorovitelnyj,
                sobytijnyj, gornolyzhnyj, morskie_kruizy, plyazhnyj_otdykh,
                s_detmi, s_kompaniej_15_24, s_kompaniej_25_44, s_kompaniej_45_66,
                s_semej, v_odinochku, paroj, kuhnya
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
        conn.commit()
        return {"status": "success", "message": "Анкета успешно сохранена"}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def get_user_survey(user_id: int):
    """Get user survey data (new structure)"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT gender, age_group, cities_5, cities_4, cities_3, cities_2, cities_1,
               izbrannoe, cities_prosmotr_more, cities_prosmotr_less,
               poznavatelnyj_kulturno_razvlekatelnyj, delovoy, etnicheskiy, religioznyj,
               sportivnyj, obrazovatelnyj, ekzotic, ekologicheskiy, selskij, lechebno_ozdorovitelnyj,
               sobytijnyj, gornolyzhnyj, morskie_kruizy, plyazhnyj_otdykh,
               s_detmi, s_kompaniej_15_24, s_kompaniej_25_44, s_kompaniej_45_66,
               s_semej, v_odinochku, paroj, kuhnya
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))
        row = cursor.fetchone()
        if row:
            survey_data = {
                "user_id": user_id,
                "gender": row[0],
                "age_group": row[1],
                "cities_5": row[2],
                "cities_4": row[3],
                "cities_3": row[4],
                "cities_2": row[5],
                "cities_1": row[6],
                "izbrannoe": row[7],
                "cities_prosmotr_more": row[8],
                "cities_prosmotr_less": row[9],
                "poznavatelnyj_kulturno_razvlekatelnyj": bool(row[10]),
                "delovoy": bool(row[11]),
                "etnicheskiy": bool(row[12]),
                "religioznyj": bool(row[13]),
                "sportivnyj": bool(row[14]),
                "obrazovatelnyj": bool(row[15]),
                "ekzotic": bool(row[16]),
                "ekologicheskiy": bool(row[17]),
                "selskij": bool(row[18]),
                "lechebno_ozdorovitelnyj": bool(row[19]),
                "sobytijnyj": bool(row[20]),
                "gornolyzhnyj": bool(row[21]),
                "morskie_kruizy": bool(row[22]),
                "plyazhnyj_otdykh": bool(row[23]),
                "s_detmi": bool(row[24]),
                "s_kompaniej_15_24": bool(row[25]),
                "s_kompaniej_25_44": bool(row[26]),
                "s_kompaniej_45_66": bool(row[27]),
                "s_semej": bool(row[28]),
                "v_odinochku": bool(row[29]),
                "paroj": bool(row[30]),
                "kuhnya": bool(row[31])
            }
            return {"status": "success", "data": survey_data}
        else:
            return {"status": "error", "message": "Анкета не найдена"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def update_city_rating(user_id: int, city_name: str, rating: int) -> Dict:
    """Update city rating in user survey"""
    if rating < 1 or rating > 5:
        return {"status": "error", "message": "Rating must be between 1 and 5"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user survey exists
        cursor.execute('''
        SELECT cities_1, cities_2, cities_3, cities_4, cities_5 
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if not row:
            # Create new survey record if doesn't exist
            cursor.execute('''
            INSERT INTO user_surveys (user_id, cities_1, cities_2, cities_3, cities_4, cities_5)
            VALUES (?, '', '', '', '', '')
            ''', (user_id,))
            cities_1, cities_2, cities_3, cities_4, cities_5 = "", "", "", "", ""
        else:
            cities_1, cities_2, cities_3, cities_4, cities_5 = row[0] or "", row[1] or "", row[2] or "", row[3] or "", row[4] or ""
        
        # Parse existing cities into sets
        cities_sets = {
            1: set(cities_1.split(',')) if cities_1 else set(),
            2: set(cities_2.split(',')) if cities_2 else set(),
            3: set(cities_3.split(',')) if cities_3 else set(),
            4: set(cities_4.split(',')) if cities_4 else set(),
            5: set(cities_5.split(',')) if cities_5 else set()
        }
        
        # Remove city from all rating lists
        for rating_list in cities_sets.values():
            rating_list.discard(city_name)
        
        # Add city to the appropriate rating list
        cities_sets[rating].add(city_name)
        
        # Convert sets back to comma-separated strings
        cities_1_str = ','.join(cities_sets[1])
        cities_2_str = ','.join(cities_sets[2])
        cities_3_str = ','.join(cities_sets[3])
        cities_4_str = ','.join(cities_sets[4])
        cities_5_str = ','.join(cities_sets[5])
        
        # Update database
        cursor.execute('''
        UPDATE user_surveys 
        SET cities_1 = ?, cities_2 = ?, cities_3 = ?, cities_4 = ?, cities_5 = ?
        WHERE user_id = ?
        ''', (cities_1_str, cities_2_str, cities_3_str, cities_4_str, cities_5_str, user_id))
        
        conn.commit()
        
        # Invalidate cache
        redis_client.delete(f"user_survey:{user_id}")
        
        return {
            "status": "success", 
            "message": f"City {city_name} rated with {rating} stars"
        }
        
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def get_city_rating(user_id: int, city_name: str) -> Dict:
    """Get current rating for a specific city"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT cities_1, cities_2, cities_3, cities_4, cities_5 
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if not row:
            return {"status": "error", "message": "User survey not found"}
        
        cities_1, cities_2, cities_3, cities_4, cities_5 = row[0] or "", row[1] or "", row[2] or "", row[3] or "", row[4] or ""
        
        # Check which rating list contains the city
        cities_lists = {
            1: cities_1.split(',') if cities_1 else [],
            2: cities_2.split(',') if cities_2 else [],
            3: cities_3.split(',') if cities_3 else [],
            4: cities_4.split(',') if cities_4 else [],
            5: cities_5.split(',') if cities_5 else []
        }
        
        for rating, cities in cities_lists.items():
            if city_name in cities:
                return {
                    "status": "success",
                    "data": {
                        "city_name": city_name,
                        "rating": rating
                    }
                }
        
        return {
            "status": "success",
            "data": {
                "city_name": city_name,
                "rating": 0  # No rating yet
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def get_user_city_ratings(user_id: int) -> Dict:
    """Get all city ratings for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT cities_1, cities_2, cities_3, cities_4, cities_5 
        FROM user_surveys WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if not row:
            return {"status": "error", "message": "User survey not found"}
        
        cities_1, cities_2, cities_3, cities_4, cities_5 = row[0] or "", row[1] or "", row[2] or "", row[3] or "", row[4] or ""
        
        return {
            "status": "success",
            "data": {
                "cities_1": cities_1.split(',') if cities_1 else [],
                "cities_2": cities_2.split(',') if cities_2 else [],
                "cities_3": cities_3.split(',') if cities_3 else [],
                "cities_4": cities_4.split(',') if cities_4 else [],
                "cities_5": cities_5.split(',') if cities_5 else [],
                "total_rated_cities": len(cities_1.split(',')) + len(cities_2.split(',')) + 
                                    len(cities_3.split(',')) + len(cities_4.split(',')) + 
                                    len(cities_5.split(',')) if any([cities_1, cities_2, cities_3, cities_4, cities_5]) else 0
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close() 
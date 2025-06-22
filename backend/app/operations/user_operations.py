from typing import List
from database.database import get_connection
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
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (survey_data.user_id,))
        if not cursor.fetchone():
            return {"status": "error", "message": "Пользователь не найден"}

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
        cursor.execute("SELECT id FROM user_surveys WHERE user_id = ?", (survey_data.user_id,))
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
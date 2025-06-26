import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = "../tours.db"

def get_connection():
    """Create and return a database connection"""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database with required tables (only users, tours, places, user_surveys)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tours table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tours (
        tour_id INTEGER PRIMARY KEY,
        title TEXT,
        date_start TEXT,
        date_end TEXT,
        location TEXT,
        rating REAL,
        relevance REAL,
        url TEXT DEFAULT NULL
    )
    ''')
    
    # Create places table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS places (
        id_place INTEGER PRIMARY KEY,
        tour_id INTEGER,
        name TEXT,
        location TEXT,
        rating REAL,
        date_start TEXT,
        date_end TEXT,
        description TEXT,
        photo TEXT,
        mapgeo_x REAL,
        mapgeo_y REAL,
        FOREIGN KEY (tour_id) REFERENCES tours(tour_id)
    )
    ''')
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Create user_favorites table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tour_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (tour_id) REFERENCES tours(tour_id),
        UNIQUE(user_id, tour_id)
    )
    ''')
    
    # Create user surveys table (NEW STRUCTURE)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_surveys (
        user_id INTEGER PRIMARY KEY,
        gender TEXT,
        age_group TEXT,
        cities_5 TEXT,
        cities_4 TEXT,
        cities_3 TEXT,
        cities_2 TEXT,
        cities_1 TEXT,
        izbrannoe TEXT,
        cities_prosmotr_more TEXT,
        cities_prosmotr_less TEXT,
        poznavatelnyj_kulturno_razvlekatelnyj BOOLEAN,
        delovoy BOOLEAN,
        etnicheskiy BOOLEAN,
        religioznyj BOOLEAN,
        sportivnyj BOOLEAN,
        obrazovatelnyj BOOLEAN,
        ekzotic BOOLEAN,
        ekologicheskiy BOOLEAN,
        selskij BOOLEAN,
        lechebno_ozdorovitelnyj BOOLEAN,
        sobytijnyj BOOLEAN,
        gornolyzhnyj BOOLEAN,
        morskie_kruizy BOOLEAN,
        plyazhnyj_otdykh BOOLEAN,
        s_detmi BOOLEAN,
        s_kompaniej_15_24 BOOLEAN,
        s_kompaniej_25_44 BOOLEAN,
        s_kompaniej_45_66 BOOLEAN,
        s_semej BOOLEAN,
        v_odinochku BOOLEAN,
        paroj BOOLEAN,
        kuhnya TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # Create ready_cities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ready_cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        federal_district TEXT,
        region TEXT,
        fias_level INTEGER,
        capital_marker INTEGER,
        population INTEGER,
        foundation_year INTEGER,
        features TEXT
    )
    ''')
    
    conn.commit()
    conn.close() 
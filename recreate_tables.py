import sqlite3

DB_PATH = "tours.db"


def recreate_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Удаляем таблицу tours, если она существует
    cursor.execute("DROP TABLE IF EXISTS tours")

    # Создаем таблицу tours
    cursor.execute("""
        CREATE TABLE tours (
            tour_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            date_start TEXT NOT NULL,
            date_end TEXT NOT NULL,
            location TEXT NOT NULL,
            rating REAL NOT NULL,
            relevance REAL NOT NULL
        )
    """)

    # Удаляем таблицу places, если она существует
    cursor.execute("DROP TABLE IF EXISTS places")

    # Создаем таблицу places
    cursor.execute("""
        CREATE TABLE places (
            id_place INTEGER PRIMARY KEY,
            tour_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            rating REAL NOT NULL,
            date_start TEXT NOT NULL,
            date_end TEXT NOT NULL,
            description TEXT,
            photo TEXT,
            mapgeo_x REAL NOT NULL,
            mapgeo_y REAL NOT NULL,
            FOREIGN KEY (tour_id) REFERENCES tours(tour_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Таблицы успешно пересозданы!")


if __name__ == "__main__":
    recreate_tables()

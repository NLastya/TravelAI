import overpy
import sqlite3
from transliterate import translit

# Транслитерация названия города для имени таблицы
def translit_name(name):
    return translit(name, 'ru', reversed=True).replace(" ", "_").lower()

# Определение категории места по тегам
def get_place_type(tags):
    if 'amenity' in tags and tags['amenity'] == 'restaurant':
        return 'Ресторан'
    if 'leisure' in tags and tags['leisure'] == 'park':
        return 'Парк'
    if 'tourism' in tags:
        if tags['tourism'] == 'museum':
            return 'Музей'
        elif tags['tourism'] == 'attraction':
            return 'Достопримечательность'
    if 'historic' in tags:
        return 'Историческое место'
    return 'Другое'

# Центроид для way/relation
def get_centroid_latlon(way_or_relation):
    coords = []
    for node in getattr(way_or_relation, 'nodes', []):
        coords.append((float(node.lat), float(node.lon)))
    if coords:
        lat = sum(c[0] for c in coords) / len(coords)
        lon = sum(c[1] for c in coords) / len(coords)
        return lat, lon
    # fallback: пробуем взять center_lat/center_lon если есть
    lat = getattr(way_or_relation, 'center_lat', None)
    lon = getattr(way_or_relation, 'center_lon', None)
    if lat is not None and lon is not None:
        try:
            return float(lat), float(lon)
        except (TypeError, ValueError):
            pass
    return None, None

# Главная функция
def fetch_places_to_sqlite(city_name: str, db_name: str = "places.db"):
    api = overpy.Overpass()
    table_name = f"places_{translit_name(city_name)}"

    # Overpass запрос
    query = f"""
    [out:json];
    area[name="{city_name}"]->.searchArea;
    (
      node["amenity"="restaurant"](area.searchArea);
      way["amenity"="restaurant"](area.searchArea);
      node["leisure"="park"](area.searchArea);
      way["leisure"="park"](area.searchArea);
      relation["leisure"="park"](area.searchArea);
      node["tourism"="museum"](area.searchArea);
      way["tourism"="museum"](area.searchArea);
      relation["tourism"="museum"](area.searchArea);
      node["tourism"="attraction"](area.searchArea);
      way["tourism"="attraction"](area.searchArea);
      relation["tourism"="attraction"](area.searchArea);
      node["historic"](area.searchArea);
      way["historic"](area.searchArea);
      relation["historic"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """

    print(f"Загружаем данные для: {city_name}")
    result = api.query(query)

    # Обработка объектов
    places = []
    for element in result.nodes + result.ways + result.relations:
        name = element.tags.get("name")
        if not name or not name.strip():
            continue  # пропускаем без имени

        place_type = get_place_type(element.tags)
        rating = element.tags.get("rating", "нет данных")
        cuisine = element.tags.get("cuisine", "")
        hours = element.tags.get("opening_hours", "")

        # координаты
        if isinstance(element, overpy.Node):
            lat = float(element.lat)
            lon = float(element.lon)
        else:
            lat, lon = get_centroid_latlon(element)
            # Если координаты невалидные, пробуем другие способы
            if (lat is None or lon is None or (lat == 0.0 and lon == 0.0)):
                # 1. Пробуем взять координаты первой ноды
                nodes = getattr(element, 'nodes', [])
                if nodes:
                    lat = float(nodes[0].lat)
                    lon = float(nodes[0].lon)
                # 2. Пробуем взять center_lat/center_lon
                if (lat is None or lon is None or (lat == 0.0 and lon == 0.0)):
                    lat = getattr(element, 'center_lat', 0.0)
                    lon = getattr(element, 'center_lon', 0.0)
                    try:
                        lat = float(lat)
                        lon = float(lon)
                    except Exception:
                        lat, lon = 0.0, 0.0
                # 3. Пробуем взять из bounds (если есть)
                if (lat is None or lon is None or (lat == 0.0 and lon == 0.0)) and hasattr(element, 'bounds'):
                    bounds = getattr(element, 'bounds', None)
                    if bounds:
                        lat = float(bounds.get('minlat', 0.0))
                        lon = float(bounds.get('minlon', 0.0))
            lat = float(lat) if lat is not None else 0.0
            lon = float(lon) if lon is not None else 0.0

        # Пропускаем места с невалидными координатами
        if lat == 0.0 and lon == 0.0:
            continue

        place_info = (
            element.id,
            name.strip(),
            type(element).__name__,
            place_type,
            rating,
            cuisine,
            hours,
            lat,
            lon
        )
        places.append(place_info)

    # Сохраняем в SQLite
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id INTEGER PRIMARY KEY,
            name TEXT,
            element_type TEXT,
            category TEXT,
            rating TEXT,
            cuisine TEXT,
            opening_hours TEXT,
            latitude REAL,
            longitude REAL
        )
    """)
    cur.execute(f'DELETE FROM "{table_name}"')

    cur.executemany(
        f"""INSERT INTO "{table_name}" 
        (id, name, element_type, category, rating, cuisine, opening_hours, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        places
    )

    conn.commit()
    conn.close()
    print(f"Данные сохранены в таблицу '{table_name}' в '{db_name}'.")
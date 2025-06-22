import pandas as pd
from lightfm import LightFM
from lightfm.data import Dataset
from itertools import chain
import numpy as np

# Функции

def filter_cities(city_string):
    if not isinstance(city_string, str):
        return ''
    cities = [city.strip() for city in city_string.split(', ')]
    filtered = [city for city in cities if city in allowed_cities]
    return ', '.join(filtered)


def age_group(age_str):
    if age_str.split(' ')[0] == 'Более':
        return 'senior'
    age = int(age_str.split(' - ')[0])
    if age == 18:
        return 'teen'
    elif age == 21:
        return 'young_adult'
    elif age == 31:
        return 'adult'


def population_group(pop):
    if pop is None:
        return ''
    if pop <= 10000:
        return 'very small'
    if pop <= 50000:
        return 'small'
    elif pop <= 100000:
        return 'medium'
    elif pop <= 500000:
        return 'high medium'
    elif pop <= 1000000:
        return 'high'
    else:
        return 'very high'


def foundation_year(year):
    if year is None:
        return ''
    if year <= 1500:
        return 'very old'
    if year <= 1700:
        return 'medium'
    elif year <= 1900:
        return 'high medium'
    else:
        return 'new'


def get_user_features(user_id):  # Добавляем учитывания признака пользователей
    row = df.loc[user_id]
    return [feat for feat in all_user_features if row[feat] == True]


def recommend(user_id, model, n=5):  # Получаем ТОП-5 рекомендаций
    user_index = list(df.index).index(user_id)
    known_cities = set(
        df.loc[user_id, 'cities_prosmotr_more_2'].split(', ') + df.loc[user_id, 'cities_prosmotr_less_2'].split(', ') +
        df.loc[user_id, 'izbrannoe'].split(', ') + df.loc[user_id, 'cities_5'].split(', ') + df.loc[
            user_id, 'cities_4'].split(', ') + df.loc[user_id, 'cities_3'].split(', ') + df.loc[
            user_id, 'cities_2'].split(', ') + df.loc[user_id, 'cities_1'].split(', '))
    city_list = list(dataset.mapping()[2].keys())

    scores = model.predict(user_ids=user_index,
                           item_ids=np.arange(len(city_list)),
                           user_features=user_features,
                           item_features=item_features)

    city_scores = list(zip(city_list, scores))
    city_scores = sorted(city_scores, key=lambda x: -x[1])
    recommendations = [city for city, score in city_scores if city not in known_cities][:n]

    return recommendations


# Подготовка данных

df = pd.read_excel('data.xlsx').drop('Unnamed: 0', axis=1)  # Пользователи
city_f = pd.read_excel('ready_cities.xlsx')  # Города
allowed_cities = city_f['city'].unique().tolist()
# Проверка, что все города из списка
df['cities_5'] = df['cities_5'].apply(filter_cities)
df['cities_4'] = df['cities_4'].apply(filter_cities)
df['cities_3'] = df['cities_3'].apply(filter_cities)
df['cities_2'] = df['cities_2'].apply(filter_cities)
df['cities_1'] = df['cities_1'].apply(filter_cities)
df['izbrannoe'] = df['izbrannoe'].apply(filter_cities)
df['cities_prosmotr_more_2'] = df['cities_prosmotr_more_2'].apply(filter_cities)
df['cities_prosmotr_less_2'] = df['cities_prosmotr_less_2'].apply(filter_cities)
df['age_group'] = df['age_group'].map(age_group)
df['gender'] = df['gender'].astype(str)
city_f['population'] = city_f['population'].map(population_group)
city_f['foundation_year'] = city_f['foundation_year'].map(foundation_year)

# Подготовка модели

dataset = Dataset()
all_users = df.index.astype(str).tolist()  # Пользователи
all_items = [i for i in city_f['city'].unique().tolist() if i != '']  # Города
all_user_features = df.columns[4:-1].tolist()
all_user_features += ['gender']  # Признаки пользователей
all_city_features = [
    'исторический', 'курортный', 'лыжный', 'промышленный', 'религиозный',
    'студенческий', 'туристический', 'торговый', 'военный', 'сельскохозяйственный',
    'медицинский', 'IT и технологический', 'экологический', 'семейный отдых',
    'экзотический', 'спортивный', 'большой', 'средний', 'маленький'
]
all_city_features.extend(city_f['federal_district'].unique().tolist())
all_city_features.extend(city_f['region'].unique().tolist())
all_city_features.extend([f'fias_level: {i}' for i in city_f['fias_level'].unique().tolist()])
all_city_features.extend([f'capital_marker: {i}' for i in city_f['capital_marker'].unique().tolist()])
all_city_features.extend([f'population: {i}' for i in city_f['population'].unique().tolist()])
all_city_features.extend(
    [f'foundation_year: {i}' for i in city_f['foundation_year'].unique().tolist()])  # Признаки городов

dataset.fit(  # Создание датасета
    users=all_users,
    items=all_items,
    user_features=all_user_features,
    item_features=all_city_features
)

user_features = dataset.build_user_features(
    ((str(user_id), get_user_features(user_id)) for user_id in df.index)
)

(interactions, weights) = dataset.build_interactions(  # Добавляем взаимодействия
    chain(
        ((str(user_id), city.strip(), 1) for user_id, cities in df['cities_5'].items() for city in cities.split(',') if
         city != ''),
        ((str(user_id), city.strip(), 0.8) for user_id, cities in df['cities_4'].items() for city in cities.split(',')
         if city != ''),
        ((str(user_id), city.strip(), 0.6) for user_id, cities in df['cities_3'].items() for city in cities.split(',')
         if city != ''),
        ((str(user_id), city.strip(), 0.4) for user_id, cities in df['cities_2'].items() for city in cities.split(',')
         if city != ''),
        ((str(user_id), city.strip(), 0.2) for user_id, cities in df['cities_1'].items() for city in cities.split(',')
         if city != ''),
        ((str(user_id), city.strip(), 0.9) for user_id, cities in df['izbrannoe'].items() for city in cities.split(',')
         if city != ''),
        ((str(user_id), city.strip(), 0.8) for user_id, cities in df['cities_prosmotr_more_2'].items() for city in
         cities.split(',') if city != ''),
        ((str(user_id), city.strip(), 0.4) for user_id, cities in df['cities_prosmotr_less_2'].items() for city in
         cities.split(',') if city != '')
        )
)

city_feature_tuples = []  # Учитываем признаки городов
for _, row in city_f.iterrows():
    features = [
        row['federal_district'],
        row['region'],
        f"fias_level: {row['fias_level']}",
        f"capital_marker: {row['capital_marker']}",
        f"population: {row['population']}",
        f"foundation_year: {row['foundation_year']}"
    ]
    city_features = [f.strip() for f in str(row['features']).split(",") if f != 'unknown']
    features.extend(city_features)
    city_feature_tuples.append((row['city'], features))
item_features = dataset.build_item_features(city_feature_tuples)

# Модель
RANDOM_STATE = 42
best_model = LightFM(
    no_components=70,
    loss='warp',
    learning_schedule='adagrad',
    learning_rate=0.07532001740060823,
    user_alpha=1.696934838853893e-05,
    item_alpha=7.26743364143695e-05,
    random_state=RANDOM_STATE
)
best_model.fit(
    interactions,
    user_features=user_features,
    item_features=item_features,
    epochs=29,
    num_threads=4,
    verbose=True
)

df['recommendations'] = df.index.map(lambda user_id: recommend(user_id, best_model))
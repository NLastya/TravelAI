from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import bs4
import requests
import re
import time
import os
import tempfile


user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_{os.getpid()}")
options = ChromeOptions()
options.add_argument("--incognito")
options.add_argument(f"--user-data-dir=/tmp/chrome_profile_{os.getpid()}")
options.page_load_strategy = 'eager'
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


def extract_city_and_id(url):
    pattern = r"weather-([a-zA-Z\-]+)-(\d+)/month/"
    match = re.search(pattern, url)

    if match:
        city = match.group(1)  # Город
        city_id = match.group(2)  # ID города
        return city, city_id
    else:
        return None, None


def get_city_id(request):

    driver.get(f"https://www.google.com/search?q={request}")
    time.sleep(3)
    first_result = driver.find_element(By.CSS_SELECTOR, "h3").find_element(By.XPATH, "..")
    first_link = first_result.get_attribute("href")
    city, city_id = extract_city_and_id(first_link)
    return city, city_id



def get_mounth(date):
    if "дек" in date:
        return 12
    if "янв" in date:
        return 1
    else:
        return date[-1]

def main(location):
    request = location
    request = request + " погода гисметео на месяц"
    city, city_id = get_city_id(request)
    site = f"https://www.gismeteo.ru/weather-{city}-{city_id}/month/"
    driver.get(site)

    soap = bs4.BeautifulSoup(driver.page_source, "html.parser")

    DATA = soap.find_all("a", class_="row-item row-item-month-date")

    ans = []

    for el in DATA:
        date = el.find("div", class_="date").get_text(strip=True)
        if len(date) > 2:
            meow = get_mounth(date)
            date = date.replace("дек", "")
            date = date.replace("янв", "")
        # Исправленные f-строки с разными кавычками
        print(f"{'' if int(date) >= 10 else 0}{int(date)}.{'' if meow >= 10 else 0}{meow}", end=" ")
        maxt = el.find("div", class_="maxt").get_text(strip=True)
        mint = el.find("div", class_="mint").get_text(strip=True)
        print(f"Макс: {maxt} Мин: {mint}", end=" ")
        print(el.get("data-tooltip"))
        ans.append(
            [f"{'' if int(date) >= 10 else 0}{int(date)}.{'' if meow >= 10 else 0}{meow}", el.get("data-tooltip")])

    return ans


if __name__ == '__main__':
    driver = webdriver.Chrome(options=options)
    request = "магнитогорск"
    request = request + " погода гисметео на месяц"
    city, city_id = get_city_id(request)
    site = f"https://www.gismeteo.ru/weather-{city}-{city_id}/month/"
    driver.get(site)

    soap = bs4.BeautifulSoup(driver.page_source, "html.parser")

    DATA = soap.find_all("a", class_ = "row-item row-item-month-date")

    for el in DATA:
        date = el.find("div", class_="date").get_text(strip=True)
        if len(date) > 2:
            meow = get_mounth(date)
            date = date.replace("дек", "").replace("янв", "")

        # Исправленная f-строка: заменяем вложенные "" на '' или используем форматирование
        print(f"{int(date)}.{'' if meow >= 10 else 0}{meow}", end=" ")

        maxt = el.find("div", class_="maxt").get_text(strip=True)
        mint = el.find("div", class_="mint").get_text(strip=True)
        print(f"Макс: {maxt} Мин: {mint}", end=" ")
        print(el.get("data-tooltip"))
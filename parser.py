from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import bs4
import requests
import re
import time



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
    if " дек" in date:
        return "12"
    if " янв" in date:
        return "01"
    else:
        return date[-1]

def get_weather(data_start, data_end, city_request):
    weather_data=[]
    options = ChromeOptions()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    soap = bs4.BeautifulSoup(driver.page_source, "html.parser")
    DATA = soap.find_all("a", class_ = "row-item row-item-month-date")
    city_request = city_request + " погода гисметео на месяц"
    city, city_id = get_city_id(city_request)

    site = f"https://www.gismeteo.ru/weather-{city}-{city_id}/month/"
    driver.get(site)


    for el in DATA:
        date = el.find("div", class_ = "date").get_text(strip = True)
        if len(date)>2:
            meow = get_mounth(date)
            date = date.replace(" дек", "")
            date = date.replace(" янв", "")
        if len(date)==1:
                date = "0"+ date
        date = date + "." + meow

        if (date >= data_start) or (date <= data_end):
            what_weather = el.get("data-tooltip")
            weather_data.append([date, what_weather])
    return weather_data
print(get_weather("27.12", "08.01", "магнитогорск"))

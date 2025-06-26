from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4
import requests
import time

options = ChromeOptions()
options.page_load_strategy = 'eager'
# options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


def get_images(query):
    urls=[]
    # Открываем DuckDuckGo
    driver.get(f"https://duckduckgo.com/?q={query}&iax=images&ia=images")
    time.sleep(1)

    # Находим все элементы с изображениями
    image_links = driver.find_elements(By.CSS_SELECTOR, "div.SZ76bwIlqO8BBoqOLqYV")
    time.sleep(1)

    if image_links:
        # Прокручиваем к первому элементу (если нужно)
        driver.execute_script("arguments[0].scrollIntoView();", image_links[0])

        for i in range(1,6):
            # Кликаем на первую картинку
            image_links[i].click()
            time.sleep(2)
            # Получаем URL увеличенного изображения
            opened_image = driver.find_element(By.CSS_SELECTOR, "img.d1fekHMv2WPYZzgPAV7b")
            url = opened_image.get_attribute("src")
            urls.append(url)
            img_data = requests.get(url).content
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)
    return urls

if __name__ == "__main__":
    search_query = "москва"
    urls = get_images(search_query)
    for el in urls:
        print(el)

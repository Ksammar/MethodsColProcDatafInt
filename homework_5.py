# Написать программу, которая собирает посты из группы https://vk.com/tokyofashion
# Будьте внимательны к сайту! Делайте задержки, не делайте частых запросов!
#
# 1) В программе должен быть ввод, который передается в поисковую строку по постам группы
# 2) Соберите данные постов:
# - Дата поста
# - Текст поста
# - Ссылка на пост(полная)
# - Ссылки на изображения(если они есть)
# - Количество лайков, "поделиться" и просмотров поста
# 3) Сохраните собранные данные в MongoDB
# 4) Скролльте страницу, чтобы получить больше постов(хотя бы 2-3 раза)
# 5) (Дополнительно, необязательно) Придумайте как можно скроллить "до конца"
# до тех пор пока посты не перестанут добавляться
#
# Чем пользоваться?
# Selenium, можно пользоваться lxml, BeautifulSoup
import tqdm
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
from lxml import html
from pymongo import MongoClient


def get_url(url, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    dom = html.fromstring(req.text)
    return dom.xpath(params)

def click_timeout_element(in_driver, class_name, timeout):
    try:
        button = WebDriverWait(in_driver, timeout).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        button.click()
    except Exception as e:
        print(e)

def find_text(text):
    search_panel = driver.find_element_by_xpath('//a[contains(@class, "ui_tab_search")]')
    time.sleep(3)
    search_panel.click()
    search_panel = driver.find_element_by_id("wall_search")
    search_panel.send_keys(text)
    search_panel.send_keys(Keys.ENTER)

def get_url_photo(main_win, webel):
    webel.click()
    click_timeout_element(main_win, "JoinForm__notNow", 3)
    time.sleep(1)
    photo_url = webel.find_element_by_xpath('//div[contains(@id, "pv_photo")]/img').get_attribute('src')
    search_panel = webel.find_element_by_xpath('//div[contains(@class, "pv_close_btn")]')
    search_panel.click()
    return photo_url

def load_mongo(in_dict):
    MONGO_URL = "127.0.0.1:27017"
    MONGO_DB = "posts"
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        col = db['tokyofashion']
        counter = 0
        for el in in_dict:
            col.update_one(
                {"$and":
                     [{'hyperlink': {"$eq": el['hyperlink']}},
                      {'text': {"$eq": el['text']}}
                      ]
                 },
                {'$set': el},
                upsert=True
            )
        print('БД постов обновлена')

def find_elements_posts(item):
    info = {}
    try:
        info['date'] = str(item.find_element_by_xpath('.//span[contains(@class, "rel_date")]').text). \
            replace("\xa0", ' ')
        info['text'] = item.find_element_by_xpath('.//div[contains(@class, "wall_post_text")]').text
        info['likes'] = (
            {
                'likes': item.find_element_by_xpath('.//a[contains(@class, "like_btn like _like")]'
                                                    '/div[contains(@class, "like_button_count")]').text,
                'share': item.find_element_by_xpath('.//a[contains(@class, "like_btn share _share")]'
                                                    '/div[contains(@class, "like_button_count")]').text,
                'views': item.find_element_by_xpath('.//div[contains(@class, "like_views _views")]').text
            }
        )
        info['hyperlink'] = item.find_element_by_xpath('.//a[contains(@class, "post_link")]').get_attribute('href')
        try:
            photos = item.find_elements_by_xpath('.//div[contains(@class, "page_post_sized_thumbs  clear_fix")]/*')
            i_photo = {}
            for j, photo in enumerate(photos):
                try:
                    i_photo[f'photo_{j}'] = get_url_photo(driver, photo)
                except Exception as e2:
                    pass

            info['photos_links'] = i_photo
        except Exception as e1:
            pass

    except Exception as e:
        print(e)
    return info


options = Options()
options.add_argument("start-maximized")

DRIVER_PATH = "D:\MaxData\Downloads\Методы сбора и обработки данных\chromedriver.exe"
driver = webdriver.Chrome(DRIVER_PATH)

url = "https://vk.com/tokyofashion"
driver.get(url)

# find_text('популярная модель')

print()
timeout = 5
info_items = []
for i in range(2):
    click_timeout_element(driver, "JoinForm__notNow", 2)
    articles = driver.find_elements_by_xpath('//div[contains(@class, "_post post")]')
    for item in articles:
        info_items.append(find_elements_posts(item))
        time.sleep(1)

    end_article = driver.find_elements_by_class_name("_post")[-1]
    actions = ActionChains(driver)
    actions.move_to_element(end_article)
    actions.perform()
    time.sleep(1)

load_mongo(info_items)

print('finish')
driver.quit()


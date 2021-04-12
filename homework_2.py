# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно
# вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
import json
import time
import pickle
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy


def get_vacancy(vacancy, header, proxi, area=0):
    vacancy = vacancy.replace(' ', '+')
    url = 'https://hh.ru/search/vacancy/'
    param = {
        "text": f'{vacancy}',
        "area": f'{area}',  # area 1 - Moscow, 78 - Samara
        "order_by": 'relevance',
        "items_on_page": '50',
        "page": "0"
    }
    req = requests.get(url, headers=header, params=param, proxies=proxi)
    # req = requests.get(url, headers=header, params=param)
    return req


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36'
}
proxies = {
    'http': f'{FreeProxy().get()}'
    # 'https': 'https://165.227.223.19:3128',
}
r = get_vacancy('data engineer', headers, proxies, 1)
# r = get_vacancy('data engineer', headers, proxies, '78')
# r = get_vacancy('data engineer', headers, area='1')
soup = bs(r.text, "html.parser")

# item_list = soup.find(attrs={"class": "vacancy-serp-item vacancy-serp-item_premium"})
item_list = soup.find(attrs={"class": "vacancy-serp"})
items = soup.find_all(attrs={"class": "vacancy-serp-item"})
items_info = []
for el in item_list.children:
    info = {}
    # a = el.find('vacancy-serp__vacancy-title')
    a = el.find("a", attrs={"class": "bloko-link"})
    if a is not None:
        info['vacance'] = a.attrs['href']
print()
# items_info = []
# for item in items:
#     info = {}
#     a = item.find("a", attrs={"class": "selection-film-item-meta__link"})
#     info['href'] = a.attrs["href"]
#     info["name"] = a.find(attrs={"class": "selection-film-item-meta__name"}).text
#     info["original_name"] = a.find(attrs={"class": "selection-film-item-meta__original-name"}).text
#     try:
#         rating = item.find(attrs={"class": "rating__value"}).text
#         rating = float(rating)
#         info["rating"] = rating
#     except Exception as e:
#         print(e)
#     items_info.append(info)
#     print()


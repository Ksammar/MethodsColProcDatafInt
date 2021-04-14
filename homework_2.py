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
import pandas as pd
import time
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy


def read_int_words(in_list_words):
    in_list_words = str(in_list_words)
    length = len(in_list_words)
    integ = []
    i = 0
    while i < length:
        s_int = ''
        a = in_list_words[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i > length:
                break
            a = in_list_words[i]
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    return integ

def read_str_words(in_list_words):
    in_list_words = str(in_list_words)
    length = len(in_list_words)
    strin = []
    i = 0
    while i < length:
        s_str = ''
        a = in_list_words[i]
        while ('а' <= a <= 'я') or ('a' <= a <= 'z'):
            s_str += a
            i += 1
            if i > length:
                break
            a = in_list_words[i]
        i += 1
        if s_str != '':
            strin.append(s_str)
    return strin


def get_vacancy(url, vacancy, header, proxi, page):
    # vacancy = vacancy.replace(' ', '+')
    param = {
        "L_save_area": "true",
        "clusters": "true",
        "enable_snippets": "true",
        "salary": {"st": "searchVacancy"},
        "text": f'{vacancy}',
        "enable_snippets": "true",
        "showClusters": "true",
        "page": f"{page}",
    }
    # req = requests.get(url, headers=header, params=param, proxies=proxi)
    req = requests.get(url, headers=header, params=param)
    return bs(req.text, "html.parser")


def find_hh(soup, url, vacancy, headers, proxies):
    items_info = []
    for i in range(0, counter_page):
        items = soup.find_all(attrs={"class": "vacancy-serp-item"})
        for el in items:
            info = {}
            salary = el.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
            if salary is not None:
                list_w = []
                list_sal = []
                list_word = []
                for el_sal in salary.contents:
                    list_w.append(el_sal.replace("\u202f", "").lower())
                list_sal = read_int_words(list_w)
                list_word = read_str_words(list_w)
                if len(list_sal) > 1:
                    info['salary_min'] = f"{list_sal[0]}"
                    info['salary_max'] = f"{list_sal[1]}"
                if len(list_word) > 0:
                    if list_word[0] == 'до':
                        info['salary_max'] = f"{list_sal[0]}"
                    if list_word[0] == 'от':
                        info['salary_min'] = f"{list_sal[0]}"
                    if list_word[-1] == "руб" or list_word[-1] == "usd" or list_word[-1] == "kzt":
                        info['salary_currency'] = f"{list_word[-1]}"

            a = el.find("a", attrs={"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-title"})
            info['vacance'] = a.contents[0]
            # salary = el.find("div", attrs={"class": "vacancy-serp-item__sidebar"})

            info['hyperlink'] = a.attrs["href"]
            info['input_website'] = url
            items_info.append(info)
        print(f'Finish page {i + 1}')
        time.sleep(0.005)
        soup = get_vacancy(url, vacancy, headers, proxies, f"{i + 1}")
    return items_info


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36'
}
proxies = {
    "http": f"{FreeProxy().get()}"
    # 'https': 'https://165.227.223.19:3128',
}
url = f"https://samara.hh.ru/search/vacancy"

vacancy = input('Please input vacancy: ')
soup = get_vacancy(url, vacancy, headers, proxies, 0)

# soup = get_vacancy(url, "data engineer", headers, proxies, "0")

pages = soup.find_all(attrs={"class": "pager-item-not-in-short-range"})
counter_page = 1
if pages is not None:
    res = pages[-1].find("a", attrs={"class": "bloko-button", "rel": "nofollow"})
    counter_page = int(res.contents[0])
items_info = []
print(f'Find {counter_page} pages')
items_info = find_hh(soup, url, vacancy, headers, proxies)
print()
df = pd.DataFrame.from_records(items_info)
df.to_csv(f'{vacancy}_vacancy.csv', index=False)
print(f'Create file "{vacancy}_vacancy.csv". Finish work!')


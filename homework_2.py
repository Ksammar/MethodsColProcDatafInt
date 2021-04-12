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
import pickle
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy


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


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36'
}
proxies = {
    "http": f"{FreeProxy().get()}"
    # 'https': 'https://165.227.223.19:3128',
}
url = f"https://samara.hh.ru/search/vacancy"
# vacancy = input('Please input vacancy: ')
# soup = get_vacancy(url, vacancy, headers, proxies, 0)
# r = get_vacancy("продавец", headers, proxies)
soup = get_vacancy(url, "data engineer", headers, proxies, "0")
pages = soup.find_all(attrs={"class": "pager-item-not-in-short-range"})
counter_page = 1
if pages is not None:
    res = pages[-1].find("a", attrs={"class": "bloko-button", "rel": "nofollow"})
    counter_page = int(res.contents[0])
items_info = []
for i in range(0, counter_page):
    items = soup.find_all(attrs={"class": "vacancy-serp-item"})
    for el in items:
        info = {}
        salary = el.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
        if salary is None:
            continue
        else:
            # info['salary'] = salary.contents[0]
            list_word = []
            list_sal = []
            for word in salary.contents:
                try:
                    word = word.split('-')
                    if len(word) > 1:
                        try:
                            numb = float(word.replace('\u202f000', '000'))
                            list_sal.append(numb)
                            list_word.append('-')
                        except:
                            pass
                    else:
                        if word != "":
                            word = word.replace(' ', "")
                            if (word == "от") or (word == "до"):
                                list_word.append(word)
                        try:
                            numb = float(word.replace('\u202f000', '000'))
                            list_sal.append(numb)
                        except:
                            pass
                for i, el_lw in enumerate(list_word):
                    if el_lw == "от":
                        info['salary'] = {"salary_min": f"{list_sal[i]}"}
                    if el_lw == "до":
                        info['salary'] = {"salary_max": f"{list_sal[i]}"}
                    if el_lw == '-':
                        info['salary'] = {"salary_min": f"{list_sal[0]}"}
                        info['salary'] = {"salary_max": f"{list_sal[1]}"}
                        break
        a = el.find("a", attrs={"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-title"})
        info['vacance'] = a.contents[0]
        # salary = el.find("div", attrs={"class": "vacancy-serp-item__sidebar"})

        info['hyperlink'] = a.attrs["href"]
        info['input_website'] = url
        items_info.append(info)
    print(f'Finish page {i + 1}')
    time.sleep(0.005)
    soup = get_vacancy(url, "data engineer", headers, proxies, f"{i + 1}")
print()
df = pd.DataFrame.from_records(items_info)
df.to_csv('vacancy.csv', index=False)
print('Finish!!!!!!')
# # item_list = soup.find(attrs={"class": "vacancy-serp"})
# # items = soup.find_all(attrs={"class": "vacancy-serp-item"})
# items_info = []
# # pages = soup.find_all(attrs={"class": "pager-item-not-in-short-range"})
# if pages is not None:
#     res = pages[-1].find("a", attrs={"class": "bloko-button", "rel": "nofollow"})
#     for i in range(0, int(res.contents[0])):
#         for el in items:
#             info = {}
#             a = el.find("a", attrs={"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-title"})
#             info['vacance'] = a.contents[0]
#             salary = el.find("div", attrs={"class": "vacancy-serp-item__sidebar"})
#             salary = el.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
#
#             if salary is not None:
#                 info['salary'] = salary.contents[0]
#
#             info['hyperlink'] = a.attrs["href"]
#             info['input_website'] = url
#             items_info.append(info)

# description = el.find("g-user-content")
# # description = el.find('vacancy-serp__vacancy_snippet_requirement')
# if description is not None:
#     info['description'] = description.contents
# else:
#     description = el.find('vacancy - serp__vacancy_snippet_responsibility')
#     if description is not None:
#         info['description'] = description.contents

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

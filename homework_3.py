# + 1. Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы, а также использование одновременно
# мин/макс зарплаты. Необязательно - возможность выбрать вакансии без указанных зарплат
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
from pprint import pprint
from pymongo import MongoClient
import pandas as pd
import homework_2 as fv

MONGO_URL = "127.0.0.1:27017"
MONGO_DB = "vacancy"


def load_vacance_mongo(input_data, cod=0):
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        col = db['loaded_vacancy']
        if cod == 0:
            col.delete_many({})
            for i in range(0, len(input_data.vacance)):
                col.insert_one({
                    "_id": f"num_str{i}",
                    input_data.columns[0]: input_data.vacance[i],
                    input_data.columns[1]: input_data.hyperlink[i],
                    # input_data.columns[2]: input_data.input_website[0],
                    input_data.columns[3]: input_data.salary_min[i],
                    input_data.columns[4]: input_data.salary_max[i],
                    input_data.columns[5]: input_data.salary_currency[i]
                })
                return col.find({})
        elif cod == 1:
            df = pd.DataFrame.from_records(input_data)
            counter = 0
            elem_count = col.count_documents({})
            for i in range(0, len(df.vacance)):
                if col.find_one({'hyperlink': df.hyperlink[i]}) is None:
                    counter += 1
                    col.insert_one({
                        "_id": f"num_str{elem_count + i}",
                        df.columns[0]: df.vacance[i],
                        df.columns[1]: df.hyperlink[i],
                        # df.columns[2]: df.input_website[0],
                        df.columns[3]: df.salary_min[i],
                        df.columns[4]: df.salary_max[i],
                        df.columns[5]: df.salary_currency[i]
                    })
            if counter > 0:
                print(f'Добавлено {counter} вакансий')
            else:
                print('нет новых вакансий')


def found_vacance(cod_found=1, salary_min=0, salary_max=1000000, currency="руб", url="127.0.0.1:27017", in_db="vacancy", collect='loaded_vacancy'):
    '''
    :input:
    kod_found =
    0 - з\п больше salary_min
    1 - з\п в диапазоне (salary_min, salary_max)
    2 - вакансии без величины з\п
    :return:
    список вакансий
    '''
    # $eq - равенство
    # $gt - больше, чем
    # $gte - больше или равно
    # $ in - вхождение в массив
    # $lt - меньше, чем
    # $lte - меньше или равно
    # $ne - не равно
    # $nin - значение отсутствует или поле не существует
    with MongoClient(url) as client:
        db = client[in_db]
        col = db[collect]
        # result = col.find({})
        if cod_found == 0:
            result = col.find(
                {
                    "$and": [
                        {"salary_min": {"$gt": salary_min}},
                        {"salary_currency": {"$eq": currency}}
                    ],
                }
            )
        elif cod_found == 1:
            result = col.find(
                {
                    "$and": [
                        {"salary_max": {"$lte": salary_max}},
                        {"salary_min": {"$gt": salary_min}},
                        {"salary_currency": {"$eq": currency}}
                    ],
                }
            )
        elif cod_found == 2:
            result = col.find(
                {
                    "$and": [
                        # {"salary_max": {"$nin": []}},
                        # {"salary_min": {"$nin": []}},
                        {"salary_currency": {"$nin": ["руб", "usd", "kzt"]}}
                    ],
                }
            )
        for item in result:
            pprint(item)
    return result


def load_new_vacance():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36'
    }
    url = f"https://samara.hh.ru/search/vacancy"
    soup = fv.get_vacancy(url, "data engineer", headers, None, "0")
    # soup = fv.get_vacancy(url, "data scientist", headers, None, "0")

    pages = soup.find_all(attrs={"class": "pager-item-not-in-short-range"})
    counter_page = 1
    if pages is not None:
        res = pages[-1].find("a", attrs={"class": "bloko-button", "rel": "nofollow"})
        counter_page = int(res.contents[0])
    items_info = []
    print(f'Find {counter_page} pages')
    items_info = fv.find_hh(soup, url, 'data engineer', headers, None, counter_page)
    # items_info = fv.find_hh(soup, url, 'data scientist', headers, None, counter_page)
    result_load = load_vacance_mongo(items_info, 1)

# ДЗ п.1
# from_file = pd.read_csv('data engineer_vacancy.csv', delimiter=',')
# result_load = load_vacance_mongo(from_file)
# ДЗ п.2
# found_vacance(kod_found=1, salary_min=10000, salary_max=200000)
# found_vacance(kod_found=0, salary_min=200000)
# found_vacance(kod_found=2)
# ДЗ п.3
load_new_vacance()

print()



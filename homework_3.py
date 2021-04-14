# + 1. Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы, а также использование одновременно
# мин/макс зарплаты. Необязательно - возможность выбрать вакансии без указанных зарплат
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
from pprint import pprint
from pymongo import MongoClient
import pandas as pd

MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "vacancy"


def load_vacance_mongo(input_data):
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        col = db['loaded_vacancy']
        #  TODO логика обновления данных
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


from_file = pd.read_csv('data engineer_vacancy.csv', delimiter=',')
result_load = load_vacance_mongo(from_file)
print()

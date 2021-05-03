# 4) Написать функцию, которая будет делать запрос к базе,
#    который вернет список подписчиков только указанного пользователя --------- followers # подписчики
# 5) Написать функцию, которая будет делать запрос к базе,
#    который вернет список профилей, на кого подписан указанный пользователь -- following # подписки
from pymongo import MongoClient
from pprint import pprint

MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "posts"

def get_id_users(user):
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        collection = db["instagram"]
        result = collection.find({"username": user})
        for item in result:
            id = item['_id']
        return  id

def get_followers(user):
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        collection = db["instagram"]
        result = collection.find({"following": get_id_users(user)})
        for item in result:
            pprint(item)
        return result


def get_followings(user):
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        collection = db["instagram"]
        result = collection.find({"followers": get_id_users(user)})
        for item in result:
            pprint(item)
        return result


if __name__ == '__main__':
    search = str(input("Введите пользователя и через пробел, 1 - найти подписчиков, 2 - подписки: ")).split()
    if search[1] == "1":
        get_followers(search[0])
    elif search[1] == "2":
        get_followings(search[0])

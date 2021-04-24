# Написать приложение, которое собирает основные новости с сайтов
# mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
from pymongo import MongoClient
import requests
from lxml import html
import time
import datetime


def get_url(url, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    dom = html.fromstring(req.text)
    return dom.xpath(params)


def read_news_mail(cod_news, from_to_list, items):
    """
    :param cod_news:
    1 - фотоновости
    2 - текстовые новости
    :return:
    """
    for item in items:
        info = {}
        try:
            if cod_news == 1:
                info["news"] = str(item.xpath('.//span[contains(@class, "photo__title")]//text()')[0]).replace("\xa0", ' ')
            elif cod_news == 2:
                if str(item.xpath('.//a[contains(@class, "list__text")]//text()')[0]).replace("\xa0", ' ') == None:
                    return from_to_list
                info["news"] = str(item.xpath('.//a[contains(@class, "list__text")]//text()')[0]).replace("\xa0", ' ')
            info["hyperlink"] = item.xpath('.//a/@href')[0]
            items_news = get_url(item.xpath('.//a/@href')[0], '//div[contains(@class, "breadcrumbs_article")]')
            info["date_news"] = items_news[0].xpath('.//span/@datetime')
            info["source_name"] = items_news[0].xpath('.//a/@href')[0]
        except Exception as e:
            print(e)
        from_to_list.append(info)
        time.sleep(0.01)
    return from_to_list


def read_news_lenta(from_to_list, items):
    url = f"https://lenta.ru"
    for item in items:
        info = {}
        try:
            news = item.xpath('.//a/text()')
            info["news"] = str(news[0]).replace("\xa0", ' ')
            url2 = url + item.xpath('.//a/@href')[0]
            info["hyperlink"] = url2
            items_news = get_url(url2, '//div[contains(@class, "topic__info")]')
            info["date_news"] = items_news[0].xpath('.//time/@datetime')
            items_news = get_url(url2, '//p[contains(@class, "content__author")]')
            info["source_name"] = url + items_news[0].xpath('.//a/@href')[0]
        except Exception as e:
            print(e)
        from_to_list.append(info)
        time.sleep(0.005)
    return from_to_list


def read_news_yandex(from_to_list, items):
    today = str(datetime.date.today())
    for item in items:
        info = {}
        try:
            info["news"] = str(item.xpath('.//text()')[0]).replace("\xa0", ' ')
            info["hyperlink"] = item.xpath('.//a/@href')[0]
            info["source_name"] = item.xpath('.//a/@aria-label')[0]
            time_post_news = today + ' ' + item.xpath('//span[contains(@class, "mg-card-source__time")]//text()')[0]
            info["date_news"] = datetime.datetime.strptime(time_post_news, '%Y-%m-%d %H:%M')
        except Exception as e:
            print(e)
        from_to_list.append(info)
    return from_to_list


def load_news_to_mongo(input_data):
    MONGO_URL = "127.0.0.1:27017"
    MONGO_DB = "hot_last_news"
    with MongoClient(MONGO_URL) as client:
        db = client[MONGO_DB]
        col = db['loaded_news']
        counter = 0
        for el in input_data:
            if col.find_one({'news': el.get('news')}) is None:
                counter += 1
                col.insert_one(el)
        if counter > 0:
            print(f'Добавлено {counter} новостей')
        else:
            print('нет новых новостей')


info_list = []
items = get_url("https://lenta.ru", '//div[contains(@class, "yellow-box__wrap")]/div[contains(@class, "item")]')
info_list = read_news_lenta(info_list, items)
print('Read news from lenta.ru')

items = get_url("https://news.mail.ru/", '//table/*/td/div[contains(@class, "daynews")]')
info_list = read_news_mail(1, info_list, items)
print('Read photo news from news.mail.ru')
items = get_url("https://news.mail.ru/", '//ul/li[contains(@class, "list__item")]')
info_list = read_news_mail(2, info_list, items)
print('Read text news from news.mail.ru')

items = get_url("https://yandex.ru/news", '//div[contains(@class, "news-top-flexible-stories")]/div')
info_list = read_news_yandex(info_list, items)
print('Read topnews from yandex.ru/news')

load_news_to_mongo(info_list)

print('finish!')
print()


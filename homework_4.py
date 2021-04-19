# Написать приложение, которое собирает основные новости с сайтов
# mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
import pandas as pd
import requests
from lxml import html
import time


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
                info["news"] = str(item.xpath('.//a[contains(@class, "list__text")]//text()')[0]).replace("\xa0", ' ')
            if str(item.xpath('.//a[contains(@class, "list__text")]//text()')[0]).replace("\xa0", ' ') == None:
                return from_to_list
            info["hyperlink"] = item.xpath('.//a/@href')[0]
            items_news = get_url(item.xpath('.//a/@href')[0], '//div[contains(@class, "breadcrumbs_article")]')
            info["date_news"] = items_news[0].xpath('.//span/@datetime')
            info["source_name"] = items_news[0].xpath('.//a/@href')[0]
        except Exception as e:
            print(e)
        from_to_list.append(info)
        time.sleep(0.005)
    return from_to_list


def read_news_lenta(from_to_list, items):
    url = f"https://lenta.ru"
    for item in items:
        info = {}
        try:
            info["news"] = item.xpath('.//text()')
            info["hyperlink"] = item.xpath('.//a/@href')[0]
            url2 = url + item.xpath('.//a/@href')[0]
            items_news = get_url(url2, '//div[contains(@class, "topic__info")]')
            info["date_news"] = items_news[0].xpath('.//time/@datetime')
            items_news = get_url(url2, '//p[contains(@class, "content__author")]')
            info["source_name"] = url + items_news[0].xpath('.//a/@href')[0]
        except Exception as e:
            print(e)
        from_to_list.append(info)
        time.sleep(0.005)
    return from_to_list


url = f"https://lenta.ru"
info_list = []
items = get_url(url, '//div[contains(@class, "yellow-box__wrap")]/div[contains(@class, "item")]')
info_list = read_news_lenta(info_list, items)

url = f"https://news.mail.ru/"
items = get_url(url, '//table/*/td/div[contains(@class, "daynews")]')
info_list = read_news_mail(1, info_list, items)
items = get_url(url, '//ul/li[contains(@class, "list__item")]')
info_list = read_news_mail(2, info_list, items)

df = pd.DataFrame.from_records(info_list)
df.to_csv(f'from_lenta_mail.csv', index=False)
print('finish!')
print()


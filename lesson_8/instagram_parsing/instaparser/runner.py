from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.spiders.instagram import InstagramSpider
from instaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # search = str(input("Введите интересующих пользователей через пробел: ")).split()
    search = ['ringovka63', 'samara_dog163', 'sunny_margo_litvinova', 'shipova.natalia', 'marinagold80']
    # search = ['ringovka63']
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider, search=search)
    process.start()

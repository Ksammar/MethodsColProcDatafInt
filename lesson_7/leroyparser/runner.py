from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

import settings
from spiders.leroymerlin import LeroymerlinSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    search = input("Введите свой запрос: ")
    # search = 'врезные замки'
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search=search)
    process.start()

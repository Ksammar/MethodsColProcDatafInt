import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroyparser.items import LeroyparserItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    find_url = 'https://samara.leroymerlin.ru'

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://samara.leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        print(response)
        links = response.xpath("//div[contains(@class,'largeCard')]/a/@href").getall()
        for link in links:
            print(link)
            yield response.follow(self.find_url + link, callback=self.parse_item)
        print(links)


    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath("photos", '//uc-pdp-media-carousel/img[contains(@slot, "thumbs")]/@src')
        loader.add_xpath("name", '//h1[@itemprop="name"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', '//uc-pdp-price-view/span[contains(@slot, "price")]/text()')
        loader.add_xpath("parameters", '//div[contains(@class, "def-list__group")]')
        yield loader.load_item()

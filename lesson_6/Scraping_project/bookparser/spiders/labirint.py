import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/search/космическая%20фантастика/?stype=0']

    def parse(self, response):
        parent_url = 'https://www.labirint.ru'
        links = response.xpath('//div[contains(@class, "_cover-wrapper")]/a/@href').getall()
        for link in links:
            yield response.follow(parent_url + link, callback=self.process_item)

        next_page = response.xpath('//div[contains(@class, "pagination-next")]/a/@href').get()
        if next_page:
            url = 'https://www.labirint.ru/search/космическая%20фантастика' + next_page
            yield response.follow(url, callback=self.parse)

    def process_item(self, response=HtmlResponse):
        item = BookparserItem()
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').get()
        item['author'] = response.xpath('//div[contains(@class, "authors")]//a//text()').get()
        item['price'] = response.xpath('//span[contains(@class, "buying-priceold-val-number")]//text()').get()
        item['discount_price'] = response.xpath('//span[contains(@class, "buying-pricenew-val-number")]//text()').get()
        item['rating'] = response.xpath('//div[contains(@id, "rate")]//text()').get()
        yield item

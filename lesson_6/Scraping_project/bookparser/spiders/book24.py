import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=космическая%20фантастика']

    def parse(self, response=HtmlResponse):
        parent_url = 'https://book24.ru'
        links = response.xpath('//div[contains(@class, "product-card__content")]/a/@href').getall()
        for link in links:
            yield response.follow(parent_url + link, callback=self.process_item)

        next_page = response.xpath('//li[contains(@class, "pagination__button-item")]//a//@href').get()
        if next_page:
            yield response.follow(parent_url + next_page, callback=self.parse)

    def process_item(self, response=HtmlResponse):
        item = BookparserItem()
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').get()
        item['author'] = response.xpath('//span[contains(@class, "__chars-value")]//a//text()').get()
        item['price'] = response.xpath('//div[contains(@class, "__price-old")]//text()').get()
        item['discount_price'] = response.xpath('//div[contains(@class, "__price")]//b//text()').get()
        item['rating'] = response.xpath('//div[contains(@class, "__rate-value")]//text()').get()
        yield item





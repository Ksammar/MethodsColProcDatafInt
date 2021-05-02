import scrapy
from scrapy.loader.processors import TakeFirst, Compose
from scrapy.http import HtmlResponse


def toprice(price):
    return int(price[0].replace(' ', ''))


def set_params(in_url):
    out = {}
    for elem in in_url:
        response = HtmlResponse(url="my HTML string", body=elem, encoding='utf-8')
        type = response.xpath('//dt/text()').get()
        value = response.xpath('//dd/text()').get()
        value = value.replace('\n', '').replace('  ', '')
        out[type] = value
    return out


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    # photos = scrapy.Field(input_processor=MapCompose(get_big_img_url))
    photos = scrapy.Field()
    parameters = scrapy.Field(input_processor=Compose(set_params))
    url = scrapy.Field()
    price = scrapy.Field(input_processor=Compose(toprice))

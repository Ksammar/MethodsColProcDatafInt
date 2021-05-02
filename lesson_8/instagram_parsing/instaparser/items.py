# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import TakeFirst, Compose

def make_list_users(following):
    out = []
    return out.append(following)

class InstaparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    followers = scrapy.Field()  # подписчики
    following = scrapy.Field(input_processor=Compose(make_list_users))  # подписки выбранного юзверя
    # likes = scrapy.Field()
    # post_data = scrapy.Field()

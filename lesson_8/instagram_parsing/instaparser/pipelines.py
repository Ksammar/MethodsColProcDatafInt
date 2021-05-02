# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        self.client = MongoClient("localhost:27017")
        self.db = self.client["posts"]

    def process_item(self, item, spider):
        # id = item.get('user_id')
        # item['_id'] = id.split('-')[-1].replace('/', '')
        self.db[spider.name].update_one({'_id': {"$eq": item['_id']}}, {'$set': item}, upsert=True)
        return item

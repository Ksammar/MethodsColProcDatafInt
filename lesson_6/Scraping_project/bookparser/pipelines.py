# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from itemadapter import ItemAdapter


class BookparserPipeline:
    def __init__(self):
        self.client = MongoClient("localhost:27017")
        self.db = self.client["books"]

    def process_item(self, item, spider):
        id = item.get('url')
        if spider.name == 'book24':
            item['_id'] = id.split('-')[-1].replace('/', '')
        elif spider.name == 'labirint':
            item['_id'] = id.replace('/', ' ').split()[-1]
        self.db[spider.name].update_one({'_id': {"$eq": item['_id']}}, {'$set': item}, upsert=True)
        # if self.db[spider.name].find_one({'_id': item.get('_id')}) is None:
        #     self.db[spider.name].insert_one(item)
        print()
        return item

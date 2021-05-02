import scrapy
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from pymongo import MongoClient
from scrapy.utils.python import to_bytes


class leroyparserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for photo_url in item['photos']:
                try:
                    yield scrapy.Request(photo_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [itm[1] for itm in results]
        print()
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["name"]}/{image_guid}.jpg'


class leroyparserPipeline:
    def __init__(self):
        self.client = MongoClient("localhost:27017")
        self.db = self.client["products"]

    def process_item(self, item, spider):
        id = item.get('url')[0]
        item['_id'] = id.split('-')[-1].replace('/', '')
        self.db[spider.name].update_one({'_id': {"$eq": item['_id']}}, {'$set': item}, upsert=True)
        return item

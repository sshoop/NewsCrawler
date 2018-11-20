# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from NewsCrawler.common.logs import Logger


class NewscrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item['label']
        collection = self.db[collection_name]
        if item is None:
            #logger = Logger('SAVE')
            pass
        elif item['title'] == '头条号自律组织成立':
            #logger = Logger('SAVE')
            pass
        elif collection.find_one({'url': item['url']}):
            '''
            去重，虽然scrapy默认基于sha1(method + url + body + header)进行去重，
            但我们每次请求的url都不同，而且自己定义url去重麻烦且数据量较小
            因此直接查询mongodb是否重复
            '''
            #logger = Logger('SAVE')
            pass
        else:
            collection.insert_one(dict(item))

            logger = Logger('SAVE')
            message = '成功 ' + item['title']
            # logger.info(message,)
        return item


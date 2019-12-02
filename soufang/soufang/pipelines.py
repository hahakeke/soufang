# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

# class SoufangPipeline(object):
#     def process_item(self, item, spider):
#         return item
from soufang.items import NewHouseItem
from soufang.items import EsfHouseItem
import logging

logger = logging.getLogger(__name__)

class SavetoMongoPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient(host='192.168.1.101', port=27017)
        self.db = self.client["fangtianxia"]
        print("打开数据库...")

    def close_spider(self, spider):
        print('写入完毕，关闭数据库.')
        self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, NewHouseItem):
                self.db.newhouse.insert(dict(item))
            elif isinstance(item, EsfHouseItem):
                self.db.erf.insert(dict(item))
        except Exception as f:
            print("存储失败!", item)
            logger.warning(f)
            logger.warning(item)
        return item

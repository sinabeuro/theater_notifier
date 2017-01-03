# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy.conf import settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TheatercrawlerPipeline(object):
    def __init__(self):

        connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        replies = item['replies']
        title =  item['title']
        addr =  item['addr']
        uids = item['uids']
        chours = item['chours']

        for r, t, a, u, c in zip(replies, title, addr, uids, chours):
            self.collection.replace_one(dict(uids=u), dict(uids=u, title=t, replies=r, addr=a, chours=c), upsert=True)
            return item
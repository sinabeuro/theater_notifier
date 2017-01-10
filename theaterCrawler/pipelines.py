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
        t = item['theatercode']
        a =  item['areacode']
        d =  item['date']
        m = item['moviename']

        if m == 'null':
            self.collection.remove(dict(theatercode=t, areacode=a, date=d))
        else:
            self.collection.replace_one(dict(theatercode=t, areacode=a, date=d, moviename=m), dict(theatercode=t, areacode=a, date=d, moviename=m), upsert=True)
        return item
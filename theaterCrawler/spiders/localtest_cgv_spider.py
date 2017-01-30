# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy import Selector, Spider
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from theaterCrawler.items import TheatercrawlerItem
from cgv_spider_core import TheaterSpiderCore
from scrapy.conf import settings
import pymongo

class LocaltestCgvSpider(Spider, TheaterSpiderCore):
    name = "localtest"
    allowed_domains = ["cgv.co.kr"]
    start_urls = (
        'file:///home/pi/Documents/scrapy/theaterCrawler/iframeTheater.html',
    )

    fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170111&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'

    def start_requests(self):
        connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
        db = connection[settings['MONGODB_DB']]
        coll = db[settings['MONGODB_COLLECTION']]

        self.init_pagecache(coll)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        response = response.replace(url=self.fake_url)
        for item in self.do_parse_item(response):
            yield item
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
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from page import PageCache

class LocaltestCgvSpider(Spider, TheaterSpiderCore):
    name = "localtest"
    allowed_domains = ["cgv.co.kr"]
    start_urls = (
        'file:///home/pi/Documents/scrapy/theaterCrawler/iframeTheater.html',
    )
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
    }

    fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170209&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'
    def spider_idle(self, spider):
        spider.logger.info('Spider idle: %s', spider.name)
        raise DontCloseSpider

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LocaltestCgvSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def start_requests(self):
        connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
        db = connection[settings['MONGODB_DB']]
        coll = db[settings['MONGODB_COLLECTION']]

        self.init_pagecache(coll)
        pagecache = PageCache.get_instance(coll)
        pages = pagecache.get_pages()

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

        for page in pages:
            if page.url:
                yield self.make_requests_from_url(page.url)

    def parse(self, response):
        if response.url in self.start_urls:
            response = response.replace(url=self.fake_url)
        print 'parse ::', response.url

        for emissions in self.do_parse_item(response):
            yield emissions
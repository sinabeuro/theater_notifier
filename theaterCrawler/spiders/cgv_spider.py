# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem
from cgv_spider_core import TheaterSpiderCore
from scrapy.conf import settings
import pymongo
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from page import PageCache

class CgvSpider(CrawlSpider, TheaterSpiderCore):
    name = "cgv"
    allowed_domains = ["cgv.co.kr"]
    start_urls = (
        'http://www.cgv.co.kr/theaters/special/show-times.aspx?regioncode=07',
    )

    rules = (
        Rule(LinkExtractor(tags=('a', 'area', 'iframe'), attrs=('href', 'src', ), allow=('regioncode\=07')), callback='parse_item', follow=True),
    )

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def spider_idle(self, spider):
        spider.logger.info('Spider idle: %s', spider.name)
        raise DontCloseSpider

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CgvSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
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

        for page in pages:
            if page.url:
                yield self.make_requests_from_url(page.url)

    def parse_item(self, response):
        # some page just in charge of bridge
        if re.search(r'date=\d+', response.url) is None:
            return

        print 'parse ::', response.url
        for emissions in self.do_parse_item(response):
            yield emissions
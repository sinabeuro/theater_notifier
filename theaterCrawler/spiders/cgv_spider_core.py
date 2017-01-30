# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem
from page import PageCache

class TheaterSpiderCore(object):
    allowed_domains = ["cgv.co.kr"]
    path_for_imax = '//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]'

    def get_value(self, url, key):
        match = re.search(r'%s=(\d+)'%key, url)
        return match.group(1)

    def init_pagecache(self, coll):
        pagecache = PageCache.get_instance(coll)
        pagecache.add_batch_page()

    def do_parse_item(self, response):
        theatercode = self.get_value(response.url, 'theatercode')
        areacode = self.get_value(response.url, 'areacode')
        date = self.get_value(response.url, 'date')
        pagecache = PageCache.get_instance()

        page = pagecache.get_page(dict(theatercode=theatercode, areacode=areacode, date=date))
        page.update(response)
        item = TheatercrawlerItem()
        item['page'] = page
        yield item
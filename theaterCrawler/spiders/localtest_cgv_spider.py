# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Spider
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem
from cgv_spider_core import TheaterSpiderCore

class LocaltestCgvSpider(Spider, TheaterSpiderCore):
    name = "localtest"
    allowed_domains = ["cgv.co.kr"]
    start_urls = (
        'file:///home/pi/Documents/scrapy/theaterCrawler/iframeTheater.html',
    )

    fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170111&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'
    def parse(self, response):
        response = response.replace(url=self.fake_url)
        for item in self.do_parse_item(response):
            yield item
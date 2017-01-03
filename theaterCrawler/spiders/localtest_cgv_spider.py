# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Spider
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem
from cgv_spider_core import CgvSpiderCore

class LocaltestCgvSpider(scrapy.Spider, CgvSpiderCore):
    name = "localtest"
    allowed_domains = ["cgv.co.kr"]
    start_urls = (
        'file:///home/pi/Documents/scrapy/theaterCrawler/iframeTheater.html',
    )

    def parse(self, response):
        response = response.replace(url='http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170106&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113')
        self.do_parse_item(response)
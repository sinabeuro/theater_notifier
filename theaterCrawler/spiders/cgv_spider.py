# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem
from cgv_spider_core import TheaterSpiderCore

class CgvSpider(CrawlSpider, TheaterSpiderCore):
    name = "cgv"
    allowed_domains = ["cgv.co.kr"]
    start_urls = (
        'http://www.cgv.co.kr/theaters/special/show-times.aspx?regioncode=07',
    )

    rules = (
        Rule(LinkExtractor(tags=('a', 'area', 'iframe'), attrs=('href', 'src', ), allow=('regioncode\=07')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # some page just in charge of bridge
        if re.search(r'date=\d+', response.url) is None:
            return
        self.do_parse_item(response)
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
import re

class CgvSpider(scrapy.Spider):
    name = "cgv"
    allowed_domains = ["http://www.cgv.co.kr/"]
    start_urls = (
        'file:///home/pi/Documents/scrapy/theaterCrawler/iframeTheater.html',
    )

    def parse(self, response):
        self.logger.info('%s', 'parse')
        hxs = Selector(response=response)
        halls = hxs.xpath('//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]')
        halls_ext = halls.extract()
        mov_info = []
        #self.logger.info(halls_ext)
        if halls is not None:
            mov_info = halls.xpath('../../../..//div[@class="info-movie"]').extract()

        yield Request(self.start_urls[0], callback=self.parse, dont_filter=True)
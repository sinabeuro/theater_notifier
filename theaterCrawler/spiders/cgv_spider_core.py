# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem

class CgvSpiderCore(object):
    allowed_domains = ["cgv.co.kr"]

    @classmethod
    def get_value(cls, url, key):
        match = re.search(r'%s=(\d+)'%key, url)
        return match.group(1)

    def do_parse_item(self, response):
        hxs = Selector(response=response)
        halls = hxs.xpath('//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]')
        halls_ext = halls.extract()
        self.logger.info('%s : %s', response.url, halls_ext)

        if halls != []:
            return
        
        item = TheatercrawlerItem()
        for moviename in halls.xpath('../../../..//div[@class="info-movie"]//strong/text()').extract():
            item['theatercode'] = self.get_value(response.url, 'theatercode')
            item['areacode'] = self.get_value(response.url, 'areacode')
            item['date'] = self.get_value(response.url, 'date')
            item['moviename'] = moviename
            self.logger.info('%s', item['moviename'])
        
        """
        hxs = Selector(response=response)
        halls = hxs.xpath('//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]')
        halls_ext = halls.extract()
        mov_info = []
        #self.logger.info(halls_ext)
        if halls is not None:
            mov_info = halls.xpath('../../../..//div[@class="info-movie"]').extract()

        yield Request(self.start_urls[0], callback=self.parse, dont_filter=True)
        """
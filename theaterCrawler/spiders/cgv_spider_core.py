# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import re
from theaterCrawler.items import TheatercrawlerItem
from theaterCrawler.spiders.states import TheaterStateFactory, Running, Closing, Preparing, Unopened

class TheaterSpiderCore(object):
    allowed_domains = ["cgv.co.kr"]
    path_for_imax = '//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]'
    
    @classmethod
    def get_value(cls, url, key):
        match = re.search(r'%s=(\d+)'%key, url)
        return match.group(1)

    @classmethod
    def is_there_imax(cls, response):
        hxs = Selector(response=response)
        halls = hxs.xpath(path_for_imax)
        return False if not halls else True

    def init_page_pool():
        pass

    def do_parse_item(self, response):
        state = TheaterStateFactory.get_state_by_response(response)
        movies = state.get_movies(response)

        for moviename in movies:
            item = TheatercrawlerItem()
            item['theatercode'] = self.get_value(response.url, 'theatercode')
            item['areacode'] = self.get_value(response.url, 'areacode')
            item['date'] = self.get_value(response.url, 'date')
            item['moviename'] = moviename.lstrip()
            self.logger.info('%s', item['moviename'])
            yield item

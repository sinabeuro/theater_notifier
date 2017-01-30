import pytest
import pymongo
from theaterCrawler.spiders.cgv_spider import CgvSpider
from theaterCrawler.spiders.states import Running, Closing, Preparing, Unopened
from scrapy.http import HtmlResponse
from theaterCrawler.spiders.page import Page, PageCache

fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170106&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'

class TestClass:
    def test_one(self):
        assert CgvSpider.get_value(fake_url, 'areacode') == '02' 

    def test_two(self):
        assert CgvSpider.get_value(fake_url, 'date') == '20170106'

    def test_three(self):
        assert CgvSpider.get_value(fake_url, 'theatercode') == '0113'
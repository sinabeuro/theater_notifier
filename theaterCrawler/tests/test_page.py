import pytest
import pymongo
from theaterCrawler.spiders.cgv_spider import CgvSpider
from theaterCrawler.spiders.states import Running, Preparing, Unopened, PageState, PageStateFactory #,Closing
from scrapy.http import HtmlResponse
from theaterCrawler.spiders.page import Page, PageCache

fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170106&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'

class TestPage(object):

    def test_page_creation(self):
        assert Page(None).__class__ == Page

    @pytest.fixture
    def coll(self):
        db_conn = pymongo.MongoClient(
			'localhost',
			27017
		)
        db = db_conn['theater']
        coll = db['info']
        return coll    

    def test_pagecache_sync(self, coll):
        pagecache = PageCache.get_instance(coll)
        assert pagecache

    def test_pagecache_get_page(self, coll):
        pagecache = PageCache.get_instance(coll)
        assert pagecache.get_page(date='20170111', areacode='02', theatercode='0113')

    def test_page_update(self, coll):
        pagecache = PageCache.get_instance(coll)
        page = pagecache.get_page(date='20170111', areacode='02', theatercode='0113')
        
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        
        page.update(fake_response)
        print page.movies

        assert pagecache.get_page(date='20170111', areacode='02', theatercode='0113')
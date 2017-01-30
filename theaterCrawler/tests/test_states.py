import pytest
import pymongo
from theaterCrawler.spiders.cgv_spider import CgvSpider
from theaterCrawler.spiders.states import Running, Preparing, Unopened, PageState, PageStateFactory #,Closing
from scrapy.http import HtmlResponse
from theaterCrawler.spiders.page import Page, PageCache

fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170106&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'

class TestState(object):
    
    def test_state_creation(self):
        running = Running(None)
        assert running

    def test_singleton(self):
        running_0 = Running(None)
        running_1 = Running(None)
        assert running_0 is running_1

    def test_state_of_running(self):
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        running = Running(None)
        b_running = running.is_this_state(fake_response)
        assert b_running == True

    def test_state_of_running_ab(self):
        f = open("state_of_running_ab.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        running = Running(None)
        b_running = running.is_this_state(fake_response)
        assert b_running == False
    """
    def test_state_of_closing(self):
        fake_response = HtmlResponse(fake_url)
        closing = Closing(None)
        b_closing = closing.is_this_state(fake_response)
        assert b_closing == True
    """
    def test_state_of_unopened(self):
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        unopened = Unopened(None)
        b_unopened = unopened.is_this_state(fake_response)
        assert b_unopened == False

    def test_get_movies(self):
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        running = Running(None)
        movies = running.get_movies(fake_response)
        #for movie in movies: print movie
        assert len(movies) == 2

    def test_get_state(self):
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        state = PageStateFactory.get_pagestate_by_rsp(fake_response)
        assert type(state) is Running
import pytest
from theaterCrawler.spiders.cgv_spider import CgvSpider
from theaterCrawler.spiders.states import Running, Closing, Preparing, Unopened
from scrapy.http import HtmlResponse

fake_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170106&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'

class TestClass:
    def test_one(self):
        assert CgvSpider.get_value(fake_url, 'areacode') == '02' 

    def test_two(self):
        assert CgvSpider.get_value(fake_url, 'date') == '20170106'

    def test_three(self):
        assert CgvSpider.get_value(fake_url, 'theatercode') == '0113'

    def test_state_of_running(self):
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        b_running = Running.is_this_state(fake_response)
        assert b_running == True

    def test_state_of_running_ab(self):
        f = open("state_of_running_ab.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        b_running = Running.is_this_state(fake_response)
        assert b_running == False

    def test_state_of_closing(self):
        fake_response = HtmlResponse(fake_url)
        b_closing = Closing.is_this_state(fake_response)
        assert b_closing == True

    def test_state_of_unopened(self):
        f = open("state_of_running.html", 'r')
        fake_body = f.read()
        fake_response = HtmlResponse(fake_url, body=fake_body)
        b_running = Unopened.is_this_state(fake_response)
        assert b_running == False

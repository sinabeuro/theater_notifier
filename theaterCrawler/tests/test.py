import pytest
from theaterCrawler.spiders.spider import CgvSpider

url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=02&date=20170106&regioncode=07&screencodes=&screenratingcode=02&theatercode=0113'

class TestClass:
    def test_one(self):
        assert CgvSpider.get_value(url, 'areacode') == '02' 

    def test_two(self):
        assert CgvSpider.get_value(url, 'date') == '20170106'

    def test_three(self):
        assert CgvSpider.get_value(url, 'theatercode') == '0113' 
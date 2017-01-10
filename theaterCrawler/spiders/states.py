import sys
import inspect
from transitions import State
from scrapy import Selector
import datetime
import re

path_for_imax = '//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]'

def get_value(url, key):
    match = re.search(r'%s=(\d+)'%key, url)
    return match.group(1)

def get_halls(response):
    hxs = Selector(response=response)
    halls = hxs.xpath(path_for_imax)
    return halls

def is_there_imax(response):
    halls = get_halls(response)
    return False if not halls else True

def do_get_movies(response):
        halls = get_halls(response)
        movies = halls.xpath('../../../..//div[@class="info-movie"]//strong/text()').extract()
        return movies

# Pay attention to the order of the class declaration    
class Closing(State):
    """description of class"""

    @staticmethod    
    def is_this_state(response):
        raw_date = get_value(response.url, 'date')
        date = datetime.datetime.strptime(raw_date, '%Y%m%d')
        now =  datetime.datetime.now()
        delta = now - date
        return True if delta.days > 0 else False

    @staticmethod  
    def get_movies(response):
        return ['']

class Running(State):
    """description of class"""

    @staticmethod    
    def is_this_state(response):
        imax = is_there_imax(response)
        return imax

    @staticmethod  
    def get_movies(response):
        return do_get_movies(response)

class Unopened(State):
    """description of class"""

    @staticmethod
    def is_this_state(response):
        imax = is_there_imax(response)
        return not imax

    @staticmethod  
    def get_movies(response):
        return ['']

class Preparing(State):
    """description of class"""
    
    @staticmethod
    def is_this_state(response):
        # Implementation is required
        return False

    @staticmethod  
    def get_movies(response):
        return do_get_movies(response)

class TheaterStateFactory(object):
    
    @staticmethod
    def get_state_by_response(response):
        for state in globals()['State'].__subclasses__():
            if state.is_this_state(response):
                return state
import sys
import inspect
from transitions import State
from scrapy import Selector
import datetime
import re

class PageState(State):

    not_impl_warning = "You must implement %s" % sys._getframe().f_code.co_name
    path_for_imax = '//div[@class="info-hall"]/ul/li[contains(./text(), "IMAX")]'
    __instances = {}

    def __init__(self, name, **kwargs):
        super(PageState, self).__init__(name, **kwargs)
        self.add_callback('enter', 'top_half')

    @classmethod
    def get_value_from_url(cls, url, key):
        match = re.search(r'%s=(\d+)'%key, url)
        return match.group(1)

    @classmethod
    def get_halls(cls, response):
        hxs = Selector(response=response)
        halls = hxs.xpath(cls.path_for_imax)
        return halls

    @classmethod
    def is_there_imax(cls, response):
        halls = cls.get_halls(response)
        return False if not halls else True

    @classmethod
    def do_get_movies(cls, response):
            halls = cls.get_halls(response)
            movies = []
            for hall in halls:
                movies.append(hall.xpath('../../../..//div[@class="info-movie"]//strong/text()').extract()[0].lstrip())
            return movies

    def __new__(cls, name=None, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(PageState, cls).__new__(cls, name=None, **kwargs)
        return cls.__instances[cls]
 
    @classmethod
    def is_this_state(cls, response):
        raise NotImplementedError(cls.not_impl_warning)

    @classmethod
    def top_half(cls):
        raise NotImplementedError(cls.not_impl_warning)

    @classmethod
    def bottom_half(cls):
        raise NotImplementedError(cls.not_impl_warning)

    @classmethod
    def get_movies(cls):
        raise NotImplementedError(cls.not_impl_warning)

# Pay attention to the order of the class declaration    
"""
class Closing(PageState):

    @classmethod
    def is_this_state(cls, response):
        raw_date = cls.get_value_from_url(response.url, 'date')
        date = datetime.datetime.strptime(raw_date, '%Y%m%d')
        now =  datetime.datetime.now()
        delta = now - date
        return True if delta.days > 0 else False

    @classmethod
    def top_half(cls):
        pass

    @classmethod
    def bottom_half(cls, coll, doc):
        coll.remove(doc)
    
    @classmethod
    def get_movies(cls, response):
        return ['']
"""
class Running(PageState):

    def __init__(self, name, **kwargs):
        super(Running, self).__init__(name, **kwargs)

    @classmethod
    def is_this_state(cls, response):
        imax = cls.is_there_imax(response)
        return imax

    @classmethod
    def top_half(cls):
        print 'top half'

    @classmethod
    def bottom_half(cls, coll, doc):
        coll.replace_one(doc, doc, upsert=True)

    @classmethod
    def get_movies(cls, response):
        return cls.do_get_movies(response)

class Unopened(PageState):
    """description of class"""

    @classmethod
    def is_this_state(cls, response):
        imax = cls.is_there_imax(response)
        return not imax

    @classmethod
    def top_half(cls):
        pass

    @classmethod
    def bottom_half(cls):
        pass

    @classmethod
    def get_movies(cls, response):
        return ['']

class Preparing(PageState):

    @classmethod
    def is_this_state(cls, response):
        # Implementation is required
        return False

    @classmethod
    def top_half(cls):
        pass

    @classmethod
    def bottom_half(cls):
        pass

    @classmethod
    def get_movies(cls, response):
        return cls.do_get_movies(response)

class PageStateFactory(object):

    @staticmethod
    def get_pagestate_by_name(name):
        for state_cls in globals()['PageState'].__subclasses__():
            state = state_cls(state_cls.__name__)
            if state.__class__.__name__ == name:
                return state

    @staticmethod
    def get_pagestate_by_rsp(response):
        for state_cls in globals()['PageState'].__subclasses__():
            state = state_cls(state_cls.__name__)
            if state.is_this_state(response):
                return state
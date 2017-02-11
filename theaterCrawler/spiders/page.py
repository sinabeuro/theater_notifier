from transitions import Machine
from theaterCrawler.spiders.states import PageStateFactory, Running, Preparing, Unopened, Closing
import errno
from theaterCrawler.spiders.listener import Listener, Listenable

class Page(Listenable):
    """description of class"""
    
    def __init__(self, db_coll, doc=None, dirty=False):
        super(Page, self).__init__()
        self.db_coll = db_coll
        self.dirty = dirty
        self.valid = True
        if doc: self.deserialize(doc)

    def __str__(self):
        return "%s %s %s\n" % (self.theatercode, self.areacode, self.date)

    def serialize(self):
        doc = {}
        doc['theatercode'] = self.theatercode
        doc['areacode'] = self.areacode
        doc['date'] = self.date
        doc['moviename'] = self.moviename
        doc['state'] = self.state.__class__.__name__
        doc['url'] = self.url
        return doc

    def deserialize(self, doc):
        self.theatercode = doc.get('theatercode')
        self.areacode = doc.get('areacode')
        self.date = doc.get('date')
        self.moviename = doc.get('moviename', [])
        self.url = doc.get('url')
        state = PageStateFactory.get_pagestate_by_name(doc.get('state', 'Unopened'))
        self.set_state(state)

    def match(self, date, areacode, theatercode):
        # Need a logic that checks the parameters
        if self.theatercode == theatercode and \
        self.areacode == areacode and \
        self.date == date :
            return True
        else:
            return False

    def update(self, response):
        next_state = PageStateFactory.get_pagestate_by_rsp(response)
        movies = next_state.get_movies(response)
        need_reschedule = True

        # There is no need to update ..
        if self.state == next_state and \
            self.moviename == movies:
            print 'PASS'
            self.dirty = False
            return need_reschedule
        
        self.set_state(next_state)
        print self.state.__class__.__name__
        if not self.state.update():
            self.notify_event()
            need_reschedule = False

        self.url = response.url
        self.moviename = movies
        self.dirty = True
        return need_reschedule

    def writeback(self):
        print self.dirty
        if self.dirty:
            doc = self.serialize()
            self.state.writeback(self.db_coll, doc)
            self.dirty = False

    def set_state(self, state):
            self.state = state

    def notify_event(self):
        self.listener.on_event(self)

    def add_event_listener(self, listener):
        self.listener = listener

class PageCache(Listener):

    __instance = None
    __pages = list()
    __db_coll = None

    def __init__(self, coll):
        super(PageCache, self).__init__()
        self.__db_coll = coll
        self.add_batch_page()
        
        if PageCache.__instance != None:
            raise NotImplementedError("This is a singleton class.")

    def __str__(self):
        pages = ''
        for page in self.__pages:
            pages += str(page)
        return pages

    @staticmethod
    def get_instance(coll=None):
        if PageCache.__instance == None:
            PageCache.__instance = PageCache(coll)
        return PageCache.__instance

    def get_page(self, arg):
        found = None
        for page in self.__pages:
            if page.match(**arg) :
                found = page
                break

        if not found:
            found = Page(self.__db_coll, arg, True)
            found.add_event_listener(self)
            self.__pages.append(found)

        return found
       
    def add_page(self, page):
        self.__pages.append(page)
        return 0

    def add_batch_page(self):
        for doc in self.__db_coll.find():
            page = Page(self.__db_coll, doc)
            page.add_event_listener(self)
            self.add_page(page)

    def get_pages(self):
        return self.__pages

    def on_event(self, listenable):
        if type(listenable) == Page:
            page = listenable
            self.__pages.remove(page)
from transitions import Machine
from theaterCrawler.spiders.states import PageStateFactory, Running, Preparing, Unopened #,Closing

class Page(object):
    """description of class"""
    
    def __init__(self, db_coll, doc=None):
        self.machine = Machine()
        self.db_coll = db_coll
        self.dirty = False
        if doc: self.deserialize(doc)

    def __str__(self):
        return "%s %s %s\n" % (self.theatercode, self.areacode, self.date)

    def serialize(self):
        doc = {}
        doc['theatercode'] = self.theatercode
        doc['areacode'] = self.areacode
        doc['date'] = self.date
        doc['moviename'] = self.moviename
        doc['state'] = self.machine.state
        return doc

    def deserialize(self, doc):
        self.theatercode = doc.get('theatercode')
        self.areacode = doc.get('areacode')
        self.date = doc.get('date')
        self.moviename = doc.get('moviename')
        state = PageStateFactory.get_pagestate_by_name(doc.get('state', 'Unopened'))
        self.machine.set_state(state)

    def match(self, date, areacode, theatercode):
        # need a logic that checks the parameters
        if self.theatercode == theatercode and \
        self.areacode == areacode and \
        self.date == date :
            return True
        else:
            return False

    def update(self, response):
        next_state = PageStateFactory.get_pagestate_by_rsp(response)
        movies = next_state.get_movies(response)

        # There is no need to update ..
        if self.machine.state == next_state and self.movies == movies:
            return

        # top_half will be executed
        self.machine.set_state(next_state)
        self.movies = movies
        self.dirty = True

    def writeback(self):
        doc = self.serialize()
        state_obj = PageStateFactory.get_pagestate_by_name(self.machine.state)
        state_obj.bottom_half(self.db_coll, doc)

class PageCache(object):   
    """ Resource manager.
    Handles checking out and returning resources from clients.
    It's a singleton class.
    """

    __instance = None
    __pages = list()
    __db_coll = None

    def __init__(self, coll):
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
            found = page if page.match(**arg) else None
        return found
       
    def add_page(self, page):
        self.__pages.append(page)
        return 0

    def add_batch_page(self):
        for doc in self.__db_coll.find():
            self.add_page(Page(self.__db_coll, doc))
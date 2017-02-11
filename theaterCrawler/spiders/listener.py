class Listener(object):

    def on_event(self, listenable):
        pass


class Listenable(object):

    def __init__(self):
        self.__listener = None

    def add_event_listener(self, listener):
        self.__listener = listener

    def notify_event(self):
        listenable = self
        self.__listener.on_event(listenable)
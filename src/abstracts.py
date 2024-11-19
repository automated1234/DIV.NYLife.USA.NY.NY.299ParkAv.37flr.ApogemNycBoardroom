# "author": "ted.cygan"

# from extronlib import event
from enum import Enum
from debug import DebugClass

class eDialerType(Enum):    #or eDialerType(str, Enum)
    POTS = 'TICallStatus'
    VOIP = 'VoIPCallStatus'



class AbstractDvClass(DebugClass):
    def __init__(self, alias, data, subscriptions):
        DebugClass.__init__(self, alias)

        self.power = None
        self.online = None 
        self._data = data
        self._subscriptions = subscriptions
        self.__events = []
        self.__event = None
        if alias+'name' in data:
            self.name = data[alias+'name']
        else:
            self.name=alias


    def subscribe(self, event):    
        if event not in self.__events:
            self.__events.append(event)
            if len(self.__events) > self._data['touchpanel_count']*2:
                self.print_me('ERR __events count:{} error (mem leak?)'.format(len(self.__events)))


    def unsubscribe(self, event):    
        if event in self.__events:
            self.__events.remove(event)

    def subscribe_one(self, event): 
        self.__event = event         

    def _raise_event(self, c, v, q):
        for event in self.__events:
            if event is not None:
                event(c,v,q)

    def _raise_event_one(self, c, v, q):
        self.__event(c,v,q)



class AbstractUiClass(DebugClass):
    def __init__(self, alias, tp, data):
        DebugClass.__init__(self, alias)

        self._tp=tp
        self._data = data
        self.__event = None
        if alias+'name' in data:
            self.name = data[alias+'name']
        else:
            self.name=alias


    def subscribe_one(self, event): 
        self.__event = event

    def _raise_event_one(self, c, v, q):
        if self.__event is not None:
            self.__event(c,v,q)

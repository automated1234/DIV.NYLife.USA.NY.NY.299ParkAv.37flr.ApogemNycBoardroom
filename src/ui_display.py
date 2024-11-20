# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button, Label, Level
from abstracts import AbstractUiClass



class UiDisplayClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, displays): 
        AbstractUiClass.__init__(self, alias, tp, data)

        self.__displays = displays
        

        __names = {
            351:displays[1].name,
        }
        self.__lblnames = {}
        for ky in __names:  
            self.__lblnames[ky]=Label(tp, ky)
            self.__lblnames[ky].SetText(__names[ky])



        self.__offlines = {
            391:'',
        }
        self.__btnofflines = {}
        for ky in self.__offlines:  
            self.__btnofflines[ky]=Button(tp, ky)
            self.__btnofflines[ky].SetVisible(not displays[ky-390].online)



        self.__ons = {
            361:'On',
        }
        self.__btnons = {}
        for ky in self.__ons:  
            self.__btnons[ky]=Button(tp, ky)
            self.__btnons[ky].SetText(self.__ons[ky])

        @event(list(self.__btnons.values()), ['Pressed', 'Released'])
        def __btnonspress(button, state):
            if state == 'Pressed':
                self.__displays[button.ID-360].power_me(True)


        self.__offs = {
            371:'Off',
        }
        self.__btnoffs = {}
        for ky in self.__offs:  
            self.__btnoffs[ky]=Button(tp, ky)
            self.__btnoffs[ky].SetText(self.__offs[ky])

        @event(list(self.__btnoffs.values()), ['Pressed', 'Released'])
        def __btnoffspress(button, state):
            if state == 'Pressed':
                self.__displays[button.ID-370].power_me(False)


        self.__displays[1].subscribe(self.__driver1_event_cb)

       
     #END CONSTRUCTOR


    def __driver1_event_cb(self, command, value, qualifier):
        self.__driver_event_process(command, value, qualifier, 1)
    
    
    def __driver_event_process(self, command, value, qualifier, index):

        if command == 'ConnectionStatus':
            if value == 'Connected':  
                self.__btnofflines[390+index].SetVisible(False)
            else:
                self.__btnofflines[390+index].SetVisible(True)

        if command == 'Power':
            if value == 'On':
                self.__btnons[360+index].SetState(1)
                self.__btnoffs[370+index].SetState(0)

            elif value == 'Off':
                self.__btnons[360+index].SetState(0)
                self.__btnoffs[370+index].SetState(1)

        self._raise_event_one(command, value, qualifier)


    def warmcool_cancel(self):
        self.__displays[1].warmcool_cancel()



    def forcehdmi(self):
        self.__displays[1].forcehdmi()









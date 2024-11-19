
# "author": "ted.cygan"

from abstracts import *



class RoomClass(AbstractDvClass):
    def __init__(self, alias, data, switcher, biamp, cams, displays, poly, onebeyond):
        AbstractDvClass.__init__(self, alias, data, [])

        self.__switcher = switcher
        self.__biamp = biamp
        self.__cams = cams
        self.__displays = displays
        self.__poly = poly
        self.__onebeyond = onebeyond
        self.online = True

        
    def room_on(self, subpage):
        self.print_me('room_on room:{}'.format(self.alias))

        if subpage=='main_center_atc':
            self.__biamp.preset('RM1_ON')
            self._raise_event('On', None, None)
        else:
            if self.power != True:
                self.power = True
                for disp in self.__displays:
                    self.__displays[disp].power_me(True)

                self.__biamp.preset('RM1_ON')
                self.__poly.power_me(True)
                self._raise_event('On', None, None)
                # self.__onebeyond.power_me(True)



    def room_off(self):
        self.print_me('room_off room:{}'.format(self.alias))
        self.power = False

        self._raise_event('Off', None, None)

        for disp in self.__displays:
            self.__displays[disp].power_me(False)
        self.__biamp.dialer_dial_hangup(False)
        self.__biamp.preset('RM1_OFF')

        self.__poly.shares(0) 
        self.__poly.hooks('Hangup All') 
        self.__poly.power_me(False)
        self.__onebeyond.power_me(False)
        self.__switcher.preset_me(0, 1, 8)




    



  



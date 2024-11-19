# "author": "ted.cygan"

from extronlib import event
from extronlib.interface import SerialInterface
from abstracts import AbstractDvClass


class LutronQseCiNwkClass(AbstractDvClass): 
    def __init__(self, alias, data, processor):
        AbstractDvClass.__init__(self, alias, data, [])

        # self.__driver = SerialInterface(processor, data[alias], Baud=9600)



        # @event(self.__driver, ['Online', 'Offline'])
        # def __driverOnlineOffline(interface, state):
        #     self.print_me('__driverOnlineOffline status:{}'.format(state))
        #     if state=='Online':
        #         self.online = True
        #         self._raise_event('ConnectionStatus',  'Connected', None)
        #     else:
        #         self.online = False
        #         self._raise_event('ConnectionStatus', state, None)


        # @event(self.__driver, 'ReceiveData')  
        # def __driverreceive(interface, rcvdata):
        #     self.print_me('rx <{}>'.format(rcvdata))

    #END CONSTRUCTOR



    def send_direct(self, val):  
        self.print_me('send_direct <{}>'.format(val))
        if self.online:
            self.__driver.Send(val)


    def tx_inject(self, val):  
        self.print_me('TRUE tx_inject (overr) <{}>'.format(val))
        if self.online:
            self.__driver.Send(val)

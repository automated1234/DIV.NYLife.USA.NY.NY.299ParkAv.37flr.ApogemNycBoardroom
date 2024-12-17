# "author": "ted.cygan"

from extronlib import event
from extronlib.system import Timer, Wait
from abstracts import AbstractDvClass
from extronlib.interface import SerialInterface


class PlanarUr9851Class(AbstractDvClass):
    def __init__(self, alias, data, processor):
        AbstractDvClass.__init__(self, alias, data, [])


        self.driver = SerialInterface(processor, data[alias], 19200)
        self.__polling = Timer(30, self.__polling_cb)


        @event(self.driver, ['Online', 'Offline'])
        def __driveronlineoffline(interface, state):
            if state == 'Online':
                self.online = True
                self._raise_event('ConnectionStatus', 'Connected', None)
            else:
                self.online = False
                self._raise_event('ConnectionStatus', 'Disconnected', None)


        @event(self.driver, 'ReceiveData') 
        def __driverReceiveData(interface, rcvdata):
            self.print_me('rx <{}>'.format(rcvdata))
            if b'DISPLAY.POWER:ON\r' in rcvdata:
                self._raise_event('Power', 'On', None)
            elif b'SYSTEM.STATE:POWERING.ON\r' in rcvdata:
                self._raise_event('Power', 'On', None)
            elif b'SYSTEM.STATE:ON\r' in rcvdata:
                self._raise_event('Power', 'On', None)

            elif b'DISPLAY.POWER:OFF\r' in rcvdata:
                self._raise_event('Power', 'Off', None)
            elif b'SYSTEM.STATE:STANDBY\r' in rcvdata:
                self._raise_event('Power', 'Off', None)

            
    #END CONSTRUCTOR


    def __polling_cb(self, timer, count): 
        self.print_me('__polling_cb online:{}'.format(self.online))
        self.__send('SYSTEM.STATE?\r')   


    
    def power_me(self, desired):
        self.print_me('power_me:{}'.format(desired))

        if desired:
            self.__send('DISPLAY.POWER=ON\r')   

            @Wait(6)    
            def __powerwaitInput():
                self.__send('SOURCE.SELECT=HDMI.1\r')   

        else:
            self.__send('DISPLAY.POWER=OFF\r')   



    def __send(self, val):
        self.print_me('tx <{}>'.format(val))
        self.driver.Send(val)


    def tx_inject(self, val):
        self.__send(val)


    def forcehdmi(self):
        self.__send('SOURCE.SELECT=HDMI.1\r')   





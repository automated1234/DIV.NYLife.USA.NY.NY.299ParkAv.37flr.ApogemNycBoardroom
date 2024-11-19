# "author": "ted.cygan"

from extronlib import event
from abstracts import AbstractDvClass
import drivers.ctrs_tt_232_ATSC_Series_v1_2_2_0 as cable_driver
from drivers.ConnectionHandler import GetConnectionHandler


class ContemporaryReClass(AbstractDvClass):
    def __init__(self, alias, data, processor):
        
        AbstractDvClass.__init__(self, alias, data, ['ConnectionStatus', 'ChannelStatus', 'Power'])

        # self.driver = GetConnectionHandler(cable_driver.EthernetClass(data[alias], 23, Model='232-ATSC 4'),'ClosedCaption', DisconnectLimit=5, pollFrequency=5)
        self.driver = GetConnectionHandler(cable_driver.SerialClass(processor, data[alias], Model='232-ATSC 4'),'ClosedCaption', DisconnectLimit=5, pollFrequency=5)


        self.driver.AutoReconnect = True
        self.driver.DeviceID='1'
        self.driver.Connect()
       
       
        def __subscribe_cb(command, value, qualifier): 
            self.print_me('__subscribe_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

            if command == 'ConnectionStatus':
                if value == 'Connected':   
                    self.online = True
                    # self.__polling.Restart()
                else:
                    self.online = False
                    # self.__polling.Cancel()
            elif command == 'Power':
                if value == 'On':   
                    self.power = True
                else:
                    self.power = False
            # if command == 'ChannelStatus':
            #     if value == 'On':   
            #         self.__autofocusstate = True
            #     else:
            #         self.__autofocusstate = False

            self._raise_event(command, value, qualifier)

            
        for cmd in self._subscriptions:
            self.driver.SubscribeStatus(cmd, None, __subscribe_cb) 
        
    #END OF CONSTRUCTOR


    # def __polling_loop(self): 
    #     pass
    #     # if self.online:   
    #     #     self.__driver.Update('Power')
    #     #     self.power = self.__driver.ReadStatus('Power')    

    def channel_discrete(self, chan):
        self.print_me('channel_discrete:{}'.format(chan))

        if self.online:
            self.driver.Set('ChannelDiscrete', chan)

    def channel_updown(self, str):
        self.print_me('channel_updown:{}'.format(str))
        if self.online:
            self.driver.Set('ChannelStep', str)


    def navigation_updownleftrightokexit(self, str):
        self.print_me('navigation:{}'.format(str))
        if self.online:
                self.driver.Set('MenuNavigation', str)


    def power_me(self, desired):
        self.print_me('power_me:{}'.format(desired))
        if self.online:   
            # self.__driver.Update('Power')
            if self.driver.ReadStatus('Power')=='On':
                self.power=True
            else:
                self.power=False

            if desired:
                self.driver.Set('Power', 'On')
            else:
                self.driver.Set('Power', 'Off')


            

        
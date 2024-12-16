# "author": "ted.cygan"

from extronlib.system import Wait, Timer
from abstracts import AbstractDvClass
from drivers.ConnectionHandler import GetConnectionHandler
import drivers.plnr_display_UR_9850_8450_v1_0_3_0 as display_driver


class PlanarUr9851Class(AbstractDvClass):
    def __init__(self, alias, data, processor):
        AbstractDvClass.__init__(self, alias, data, ['ConnectionStatus', 'Power'])


        self.__driver = GetConnectionHandler(display_driver.SerialClass(processor, data[alias], Model='UR9850'), 'Power', DisconnectLimit=5,  pollFrequency=10)
        # self.__driver = display_driver.SerialClass(processor, data[alias], Model='UR9851')
        # self.__polling = Timer(10, self.__polling_loop) 


        def __subscribe_cb(command, value, qualifier):  
            self.print_me('__subscribe_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))
            if command == 'Power':
                if value == 'On':   
                    self.power = True
                else:
                    self.power = False
            elif command == 'ConnectionStatus':
                if value == 'Connected':   
                    self.online = True
                    # self.__polling.Restart()
                else:
                    self.online = False
                    # self.__polling.Cancel()

            self._raise_event(command, value, qualifier)


        for cmd in self._subscriptions:
            self.__driver.SubscribeStatus(cmd, None, __subscribe_cb)

        self.__driver.Connect()


    #END CONSTRUCTOR

    # def __polling_loop(self, timer, count): 
    #     if self.online:   
    #         self.__driver.Update('Power')


    
    def power_me(self, desired):

        if self.online:   
            self.__driver.Update('Power')
            sta = self.__driver.ReadStatus('Power')
            self.print_me('power_me desired:{}, curr:{}'.format(desired, sta))

            if sta=='On' or sta=="Warming Up":
                self.power=True
            else:
                self.power=False

            if desired != self.power:
                self.__driver.Set('Power', 'On')
                @Wait(3)    
                def __powerwaitInput():
                    self.__driver.Set('Input', 'HDMI 1')
            else:
                self.__driver.Set('Power', 'Off')


    def forcehdmi(self):
        self.__driver.Set('Input', 'HDMI 1')





  





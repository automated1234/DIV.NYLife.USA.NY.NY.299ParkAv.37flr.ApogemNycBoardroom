# "author": "ted.cygan"

from extronlib.system import Timer
from abstracts import AbstractDvClass
import drivers.onebynd_sm_Automate_VX_Series_v1_0_7_0 as onebeyond_driver



class OnebeyondClass(AbstractDvClass):
    def __init__(self, name, data):
        AbstractDvClass.__init__(self, name, data, ['ConnectionStatus', 'AutoSwitch', 'Output'])
        # self.driver = GetConnectionHandler(onebeyondDriver.HTTPClass(data[name], 3579, 'admin', 'password', Model='Automate VX'), 'AutoSwitch') #, DisconnectLimit=5, pollFrequency=15)
        if data['labtest']==False:
            self.__driver = onebeyond_driver.HTTPClass(data[name], 3579, 'admin', '1beyond', Model='Automate VX Plus') #, 'AutoSwitch') #, DisconnectLimit=5, pollFrequency=15)
            self.__auto_switch_fb = 'On'
            self.__driver.connectionCounter = 5

            self.__polling = Timer(60, self.__polling_cb)

            def __subscribe_cb(command, value, qualifier): 
                self.print_me('__subscribe_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

                if command == 'ConnectionStatus':
                    if value == 'Connected':   
                        self.online = True
                        # self.__polling.Restart()
                    else:
                        self.online = False
                        # self.__polling.Cancel()
                elif command == 'AutoSwitch':
                    self.__auto_switch_fb=value

                self._raise_event(command, value, qualifier)
                

            for cmd in self._subscriptions:
                self.__driver.SubscribeStatus(cmd, None, __subscribe_cb) 
    #END CONSTRUCTOR


    def __polling_cb(self, timer, count): 
        self.__update_auto_switch_FB()    
        self.print_me('online:{} alias:{}'.format(self.online, self.alias))


    def auto_switch(self, val):
        self.print_me('auto_switch:{}'.format(val))
        if self.online:   
            self.__driver.Set('AutoSwitch', val)
            self.__update_auto_switch_FB()   


            
    def mode_switch(self, val):
        self.print_me('mode_switch:{}'.format(val))
        if self.online:   
            self.__driver.Set('ForceRoomConfiguration', str(val))


    def switch_cam(self, val):
        self.print_me('switch_cam:{}'.format(val))
        if self.online:   
            self.__driver.Set('SwitchCamera', val)



    def __update_auto_switch_FB(self):
        if self.online:   
            self.__driver.Update('AutoSwitch')
            self.__auto_switch_fb=self.__driver.ReadStatus('AutoSwitch')
            self._raise_event('AutoSwitch', self.__auto_switch_fb, None)

            

    def power_me(self, val):
        self.print_me('system_power:{}'.format(val))
        
        if self.online:   
            if val:
                self.__driver.Set('Wake', None)
            else:
                self.__driver.Set('Sleep', None)


   
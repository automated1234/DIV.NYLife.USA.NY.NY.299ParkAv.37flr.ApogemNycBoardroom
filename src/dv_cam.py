# "author": "ted.cygan"

from extronlib.system import Timer
from abstracts import AbstractDvClass
import drivers.onebynd_camera_AutoTracker_3_v1_0_1_1 as cam_driver
from drivers.ConnectionHandler import GetConnectionHandler


class CamClass(AbstractDvClass):
    def __init__(self, alias, data, onebeyond, poly):
        AbstractDvClass.__init__(self, alias, data, ['ConnectionStatus', 'Power','FocusMode'])
        self.__driver = GetConnectionHandler(cam_driver.EthernetClass(data[alias], 5500,  Model='AutoTracker 3'), 'Power') 

        self.__driver.AutoReconnect = True
        self.__driver.Connect()
        self.__autofocusstate = True

        self.__onebeyond = onebeyond
        self.__poly = poly

        self.__polling = Timer(10, self.__polling_loop) 

        def __subscription_cb(command, value, qualifier): 
            self.print_me('__subscription_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

            if command == 'ConnectionStatus':
                if value == 'Connected':   
                    self.online = True
                else:
                    self.online = False
            
            elif command == 'Power':
                if value == 'On':   
                    self.power = True
                else:
                    self.power = False
            
            elif command == 'FocusMode':
                if value == 'Auto':   
                    self.__autofocusstate = True
                else:
                    self.__autofocusstate = False

            self._raise_event(command, value, qualifier)

            
        for cmd in self._subscriptions:
            self.__driver.SubscribeStatus(cmd, None, __subscription_cb) 
    #END CONSTRUCTOR

        
    def __polling_loop(self, timer, count): 
        pass
        # if self.online:   
            # self.__driver.Update('FocusMode')


    def focus_farNearStop(self, val):
        if self.online:
            self.__driver.Set('Focus', val, {'Focus Speed':'4'})


    def auto_focus(self):
        if self.online:
            if self.__autofocusstate:
                self.__driver.Set('FocusMode', 'Manual')
            else:
                self.__driver.Set('FocusMode', 'Auto')


    def home(self):
        if self.online:
            self.__driver.Set('Home', None)


    def power_me(self, val):
        self.print_me('power_me val:{}'.format(val))
        if self.online:
            if val:
               self.__driver.Set('Power', 'On')
            else:
                self.__driver.Set('Power', 'Off')


    def pantilt(self, val): 
        self.print_me('pantilt val:{}'.format(val))
        if self.online:   
            self.__driver.Set('PanTilt', val, {'Pan Speed': '10', 'Tilt Speed': '10'})


    def zoom(self, val):
        self.print_me('zoom val:{}'.format(val))
        if self.online:
            self.__driver.Set('Zoom', val,  {'Zoom Speed': '4'})


    def preset(self, val, save):
        self.print_me('preset pre:{}, save:{}'.format(val, save))
        if self.online:
            if save:
                self.__driver.Set('PresetSave', str(val))
            else:
                self.__driver.Set('PresetRecall', str(val))


    def onebeyond_autoswitch_me(self, val):
        self.print_me('onebeyond_autoswitch_me val:{}'.format(val))
        self.__onebeyond.auto_switch(val)


    def onebeyond_mode_me(self, val):
        self.print_me('onebeyond_mode_me val:{}'.format(val))
        self.__onebeyond.mode_switch(val)


    def onebeyond_switch_cam(self, val):
        self.print_me('onebeyond_switch_cam val:{}'.format(val))
        self.__onebeyond.switch_cam(val)


    def cam_source(self, val):
        self.print_me('cam_source val:{}'.format(val))
        self.__poly.driver.Send('camera near {}\r'.format(val))




        
# "author": "ted.cygan"

from extronlib.system import Timer
from abstracts import AbstractDvClass
from drivers.ConnectionHandler import GetConnectionHandler
import drivers.poly_vtc_G7500_v1_5_1_0 as poly_driver
from util_stopwatch import StopwatchClass


class PolyG7500Class(AbstractDvClass):
    def __init__(self, alias, data, processor, switcher, biamp):
        AbstractDvClass.__init__(self, alias, data, ['ConnectionStatus', 'SleepMode', 'VideoContentSource','CallInfoState', 'Volume'])

        self.driver = GetConnectionHandler(poly_driver.SerialClass(processor, data[alias], Model='G7500'), 'Version', DisconnectLimit=5,  pollFrequency=10)
        # self.driver = GetConnectionHandler(poly_driver.SSHClass(data[alias], 22, Credentials=('admin', ''), Model='G7500'), 'CallInfoState', DisconnectLimit=5,  pollFrequency=10)
        self.driver.AutoReconnect = True
        self.driver.Connect()


        # self.__dialer_hook_state = 'Inactive'
        self.__dialer_dial_string = ''
        # self.__shift = False
        self.__switcher = switcher
        self.__biamp = biamp
        self.__piplayout = 1
        self.shareinput=1  
        self.processor = processor


        self.__stopwatch = StopwatchClass('polystopwatch', data, None, 1.0)  
        self.__stopwatch.subscribe_one(self.__stopwatch_event_cb)   

        self.__sharing = False


        self.__pips = {
            1:'self-view corner',
            2:'self-view full-screen',
            3:'content dual',
            4:'content single',
        }


        def __subscribe_cb(command, value, qualifier):  
            self.print_me('__subscribe_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))
            if command == 'SleepMode':
                if value == 'Wake':   
                    self.power = True
                else:
                    self.power = False
            elif command == 'ConnectionStatus':
                if value == 'Connected':   
                    self.online = True
                    self.volume_update([30])
                    # self.__polling.Restart()
                else:
                    self.online = False
                    # self.__polling.Cancel()
            elif command == 'CallInfoState':
                self.__dialer_hook_state = value
                if value == "Connected":
                    self.__stopwatch.start(None)
                else:
                    self.__stopwatch.stop()

            elif command == 'VideoContentSource':
                if value == "Stop":
                    self.__sharing = False
                else:
                    self.__sharing = True

            self._raise_event(command, value, qualifier)


        for cmd in self._subscriptions:
            self.driver.SubscribeStatus(cmd, None, __subscribe_cb)

    #END OF CONSTRUCTOR
    
    
    
    def power_me(self, desired):
        self.print_me('power_me:{}'.format(desired))

        if self.online:   
            # self.__driver.Update('Power')
            if self.driver.ReadStatus('SleepMode')=='Wake':
                self.power=True
            else:
                self.power=False

            if desired:
                self.driver.Set('SleepMode', 'Wake')
            else:
                self.driver.Set('SleepMode', 'Sleep')



    def mic_mute(self, val):
        self.print_me('mic_mute:{}'.format(val))

        if self.online:   
            if val:
                self.driver.Set('TransmitMute', 'On')
            else:
                self.driver.Set('TransmitMute', 'Off')



    # def views(self, str):
    #     self.print_me('views:{}'.format(str))

    #     if self.online:   
    #         self.driver.Set('Selfview', str)


    # def menus(self, str):
    #     self.print_me('menus:{}'.format(str))

    #     if self.online:   
    #         self.driver.Set('MenuNavigation', str)

    
    def shares(self, val):
        self.print_me('shares:{} sending:-2'.format(val))

        if self.online: 
            if val == 0:
                self.driver.Set('VideoContentSource', 'Stop')
                self.__biamp.logic_state_raw('RM1_VTC_CONTENT_AUDIO', '1', True)
                self.__switcher.switch_me(val, 5)
                self.__switcher.switch_me(val, 8)

                self.__switcher.switch_me(6, 1)
                self.__switcher.switch_me(7, 2)
                self.__switcher.switch_me(6, 3)
                self.__switcher.switch_me(7, 4)


            elif val == 10:
                self.driver.Set('VideoContentSource', '2')  #tbd if 1
                self.__biamp.logic_state_raw('RM1_VTC_CONTENT_AUDIO', '1', False)
                self.__biamp.mute_descrete_raw('PGM_FAR', '1', 'Off')

                self.__switcher.switch_me(self.shareinput, 5)
                self.__switcher.switch_me(self.shareinput, 8)

                self.__switcher.switch_me(6, 1)
                self.__switcher.switch_me(7, 2)
                self.__switcher.switch_me(6, 3)
                self.__switcher.switch_me(7, 4)

            else:
                self.shareinput=val  
                if self.__sharing == False:
                    self.__switcher.switch_me(self.shareinput, 1)
                    self.__switcher.switch_me(self.shareinput, 3)
                    self.__switcher.switch_me(self.shareinput, 8)
                    self.__biamp.mute_descrete_raw('PGM_FAR', '1', 'On')

                else:
                    self.__switcher.switch_me(self.shareinput, 5)
                    self.__switcher.switch_me(self.shareinput, 8)
            
            
            self.driver.Update('VideoContentSource')



    def dtmfs(self, str):
        self.print_me('dtmfs:{}'.format(str))

        if self.online:   
            self.driver.Set('DTMF', str)


    def iremulates(self, str):
        self.print_me('iremulates:{}'.format(str))
        if self.online:   
            self.driver.Send('button {}\r'.format(str))
            #second action for some btns
            if str == 'hangup':
                self.driver.Send('button back\r'.format(str))
            elif str == 'home':
                self.driver.Send('button menu\r'.format(str))



    def hooks(self, str):
        self.print_me('hooks:{}'.format(str))

        if self.online:   
            self.driver.Set('Hook', str)


    def piplayout(self):
        self.print_me('piplayout: curr{}'.format(self.__piplayout))
        if self.__piplayout < 4:
            self.__piplayout += 1
        else:
            self.__piplayout =1 

        if self.online:
            self.driver.Send('configpresentation {}\r'.format(self.__pips[self.__piplayout]))



    def dialpad_dial(self):
        self.print_me('dialpad_dial:{}'.format(self.__dialer_dial_string))

        if self.online:   
            self.driver.Set('DialString', self.__dialer_dial_string)
            self.driver.Set('Hook', 'Dial Auto')


    def dialpad_press(self, str):
        # if self.online and self.__dialer_hook_state == 'Off':
        #     self.driver.Set('DTMF', str, {'Instance Tag': self.dialer_instance_tags[dialer], 'Line': self.dialer_lines[dialer]})
        self.__dialer_dial_string += str
        return self.__dialer_dial_string


    def dialpad_back(self):
        self.__dialer_dial_string = self.__dialer_dial_string[:-1]
        # self._raise_event(self.dialer_instance_status_tags, self.__dialer_dial_string[dialer], self.dialer_lines[dialer])
        return self.__dialer_dial_string


    def dialpad_clear(self):
        self.__dialer_dial_string = ''
        return self.__dialer_dial_string
    

    def volume_update(self, level):
        self.print_me('volume_update:{}'.format(level))
        if self.online:   
            self.driver.Set('Volume', level[0])
            # self.driver.Update('Volume')


    def tx_inject(self, val):
        self.print_me('TRUE tx_inject (overrdn) <{}>'.format(val))
        self.driver.Send(val)


    def __stopwatch_event_cb(self, command, value, qualifier):
        self.print_me('__timer_event_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))
        self._raise_event(command, value, qualifier)





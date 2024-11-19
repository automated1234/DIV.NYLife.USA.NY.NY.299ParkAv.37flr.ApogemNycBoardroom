# "author": "ted.cygan"

from abstracts import AbstractDvClass
from main_data import data

import drivers.extr_matrix_XTPIICrossPointSeries_v1_12_0_1 as switcher_driver
from drivers.ConnectionHandler import GetConnectionHandler


class SwitcherClass(AbstractDvClass):
    SWITCHER_INSCOUNT = data['switcher_inscount']
    SWITCHER_OUTSCOUNT = data['switcher_outscount']


    def __init__(self, alias, data):
        AbstractDvClass.__init__(self, alias, data, ['ConnectionStatus', 'InputSignalStatus','OutputTieStatus', 'VideoMute'])
        
        self.__driverraw = switcher_driver.EthernetClass(data[alias], 23, Model='XTP II CrossPoint 1600')
        self.__driverraw.devicePassword = 'password'
        self.__driverraw.NumberofInputs = data['switcher_inscount']
        self.__driverraw.NumberofOutputs = data['switcher_outscount']
        self.__driver = GetConnectionHandler(self.__driverraw, 'ExecutiveMode', DisconnectLimit=5, pollFrequency=15)

        self.__driver.AutoReconnect = True
        self.__driver.Connect()

        self.__videomutedemo = 'Off'


        def __subscribe_cb(command, value, qualifier): 
            self.print_me('__subscribe_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

            if command == 'ConnectionStatus':
                if value == 'Connected':   
                    self.online = True
                else:
                    self.online = False

            self._raise_event(command, value, qualifier)
            
        for cmd in self._subscriptions:
            self.__driver.SubscribeStatus(cmd, None, __subscribe_cb) 
        
    #END CONSTRUCTOR



    def preset_me(self, inp, st, en):
        en+=1
        for x in range(st, en, 1):  
            self.switch_me(inp, x)


    def switch_me(self, innumber, outnumber):
        self.print_me('switch_me > in:{}, out:{}'.format(innumber, outnumber))

        if innumber >= 0 and outnumber > 0 and innumber <= SwitcherClass.SWITCHER_INSCOUNT and outnumber <= SwitcherClass.SWITCHER_OUTSCOUNT:
            if outnumber == 8:
                tietype ='Audio'
            else:
                tietype ='Video'

            if self.online:
                self.__driver.Set('MatrixTieCommand', None, {'Input': str(innumber), 'Output': str(outnumber), 'Tie Type':tietype})
                # if outnumber == 6: #vtc content
                #     self.__driver.Set('MatrixTieCommand', None, {'Input': str(innumber), 'Output': '9', 'Tie Type':'Audio'})

            else:
                self._raise_event('OutputTieStatus', innumber, {'Output': str(outnumber),'Tie Type':tietype})
        else:
            self.print_me('ERR switch_me invalid in:{} or out:{}'.format(innumber, outnumber))


    def video_mute(self, out):
        self.print_me('video_mute > out:{}'.format(out))

        if out > 0 and out <= SwitcherClass.SWITCHER_OUTSCOUNT:
            if self.online:
                val = self.__driver.ReadStatus('VideoMute', {'Output': str(out)})
                if val == 'On':
                    self.__driver.Set('VideoMute', 'Off', {'Output': str(out)})
                else:
                    self.__driver.Set('VideoMute', 'On', {'Output': str(out)})
           
                self.__driver.Update('VideoMute', {'Output': str(out)})
                return self.__driver.ReadStatus('VideoMute', {'Output': str(out)})
            else:
                if self.__videomutedemo == 'On':
                    self.__videomutedemo = 'Off'
                else:
                    self.__videomutedemo = 'On'

                self._raise_event('VideoMute', self.__videomutedemo, {'Output': str(out)})
                return self.__videomutedemo

        else:
            self.print_me('ERR video_mute invalid out:{}'.format(out))

    def get_videomute(self, out):
        return self.__driver.ReadStatus('VideoMute', {'Output': str(out)})



    def video_mute_discrete(self, out, val):
        self.print_me('video_mute_discrete > out:{}, val:{}'.format(out, val))

        if out > 0 and out <= SwitcherClass.SWITCHER_OUTSCOUNT:
            if self.online:
                if val:
                    self.__driver.Set('VideoMute', 'On', {'Output': str(out)})
                    self.__videomutedemo == 'On'
                else:
                    self.__driver.Set('VideoMute', 'Off', {'Output': str(out)})
                    self.__videomutedemo == 'Off'

        else:
            self.print_me('ERR video_mute_discrete invalid out:{}'.format(out))




        
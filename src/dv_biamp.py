# "author": "ted.cygan"

from extronlib.system import Timer
from abstracts import *
import drivers.biam_dsp_TesiraSeries_v1_15_1_0 as biamp_driver 
from drivers.ConnectionHandler import GetConnectionHandler
from util_stopwatch import StopwatchClass


class BiampClass(AbstractDvClass):
    def __init__(self, alias, data, tags, processor):
        AbstractDvClass.__init__(self, alias, data, ['ConnectionStatus'])


        # ttp/command string on biamp software to make rs232 work
        self.__driver = GetConnectionHandler(biamp_driver.SSHClass(data[alias], 22,  Credentials=('default', ''), Model='Tesira SERVER-IO'), 'VerboseMode', DisconnectLimit=5)
        # self.__driver = GetConnectionHandler(biamp_driver.SerialClass(processor, data[alias], Model='Tesira SERVER-IO'), 'VerboseMode', DisconnectLimit=5)
        self.__driver.AutoReconnect = True
        # self.__driver.Connect()


        self.__stopwatch = StopwatchClass('biampstopwatch', data, None, 1.0)  
        self.__stopwatch.subscribe_one(self.__stopwatch_event_cb)  

        self.__tags = tags
        
        self.__dialer_hook_state = 'Off'
        self.__dialer_status = 'unknown'
        self.__dialer_callerid = 'unknown'
        # self.lineStatus = None
        self.__dialer_dial_string = ''

        self.dialer_type = eDialerType.VOIP

        self.dialer_instance_tag = None
        self.dialer_instance_status_tag = None
        self.dialer_line = 1




        self.__polling = Timer(30, self.__polling_cb)
        

        def __subscribe_cb(command, value, qualifier):
            self.print_me('__subscribe_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

            if command == 'ConnectionStatus':
                if value == 'Connected':
                    try:
                        # for tag in self.__tags:  #apply defaults
                        #     # if tag['subscription'] =='LevelControl':  
                        #     #     self.__driver.Set('LevelControl', -20, {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']})
                        #     if tag['subscription'] =='MuteControl':  
                        #         self.__driver.Set('MuteControl', 'Off', {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']})
                        #     elif tag['subscription'] =='LogicState':  
                        #         self.__driver.Set('LogicState', 'False', {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']})
                        #     # elif tag['subscription'] =='VoIPCallStatus':  
                        #     #     self.driver.Set('VoIPCallStatus', {'Instance Tag': self.tag['statusInstanceTag'], 'Line':'1', 'Call Appearance':'1'})
                        self.online = True
                        self.__polling.Restart()
                    except:
                        pass
                else:
                    self.online = False
                    self.__polling.Stop()
            elif command == self.dialer_type.value:
                self.__dialer_hook_state = value
                if self.dialer_type==eDialerType.VOIP:
                    if value == "Active":
                        self.__stopwatch.start(None)
                    else:
                        self.__stopwatch.stop()
                # else:
                #     if value == "Connected":
                #         self.__stopwatch.start()
                #     else:
                #         self.__stopwatch.stop()

            self._raise_event(command, value, qualifier)


        for cmd in self._subscriptions:
            self.__driver.SubscribeStatus(cmd, None, __subscribe_cb)


        if data['labtest']==False:
            self.__driver.Connect()


        for tag in self.__tags:
            if tag['subscription'] =='LevelControl':
                self.__driver.SubscribeStatus(tag['subscription'], {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']}, __subscribe_cb)
            elif tag['subscription'] =='MuteControl': 
                self.__driver.SubscribeStatus(tag['subscription'], {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']}, __subscribe_cb)
            elif tag['subscription'] =='MuteControlDiscrete': 
                self.__driver.SubscribeStatus('MuteControl', {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']}, __subscribe_cb)
            elif tag['subscription'] =='LogicState': 
                self.__driver.SubscribeStatus(tag['subscription'], {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']}, __subscribe_cb)
            elif tag['subscription'] == eDialerType.VOIP.value or tag['subscription'] == eDialerType.POTS.value:
                self.__driver.SubscribeStatus(tag['subscription'], None, __subscribe_cb) 
                self.__driver.SubscribeStatus(tag['subscription2'], None, __subscribe_cb)
                self.__driver.SubscribeStatus(tag['subscription3'], None, __subscribe_cb)

                self.dialer_instance_tag = tag['instanceTag']
                self.dialer_instance_status_tag = tag['statusInstanceTag']
                self.dialer_line = tag['line']

                if tag['subscription'] == eDialerType.VOIP.value:
                    self.dialer_type = eDialerType.VOIP
                elif tag['subscription'] == eDialerType.POTS.value:
                    self.dialer_type = eDialerType.POTS
    #END CONSTRUCTOR
        
    def __polling_cb(self, timer, count):  
        if self.online:  
            for tag in self.__tags:
                if tag['subscription'] =='LevelControl':
                    self.__driver.Update('LevelControl', {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']})
                elif tag['subscription'] =='MuteControl':  
                    self.__driver.Update('MuteControl', {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']})
                elif tag['subscription'] =='LogicState':  
                    self.__driver.Update('LogicState', {'Instance Tag': tag['instanceTag'], 'Channel': tag['channel']})
                elif tag['subscription'] == self.dialer_type.value: 
                    if self.dialer_type == eDialerType.VOIP: 
                        self.__driver.Update(self.dialer_type.value, {'Instance Tag': tag['statusInstanceTag'], 'Line':tag['line'], 'Call Appearance':'1'})
                    else:
                        self.__driver.Update(self.dialer_type.value, {'Instance Tag': tag['statusInstanceTag'], 'Line':tag['line']})


    def preset(self, pre):
        self.print_me('preset > pre:{}'.format(pre))
        self.__driver.Set('PresetRecallName', None, {'Name': pre})


    def preset_id(self, pre):
        self.print_me('preset_id > pre:{}'.format(pre))
        self.__driver.Set('PresetRecall', pre)


    def mute_toggle(self, mytag):
        self.print_me('mute_toggle {}, chan:{}'.format(mytag['instanceTag'], mytag['channel']))

        if self.online:
            self.__driver.Update('MuteControl', {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})
            value = self.__driver.ReadStatus('MuteControl', {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})

            if value == 'On':
                newval = 'Off'
            else:
                newval ='On'

            self.__driver.Set('MuteControl', newval, {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})

            # james seo lazy hacks
            if mytag['instanceTag']=='RM1_PRG':
                self.__driver.Set('MuteControl', newval, {'Instance Tag': 'PGM_FAR', 'Channel': '1'})
            if mytag['instanceTag']=='RM1_ATC_RX':
                self.__driver.Set('MuteControl', newval, {'Instance Tag': 'ATC_FAR', 'Channel': '1'})
            if mytag['instanceTag']=='RM1_VTC_RX':
                self.__driver.Set('MuteControl', newval, {'Instance Tag': 'USB_FAR', 'Channel': '1'})



    def mute_discrete(self, mytag, val):
        self.print_me('mute_discrete {}, chan:{}, {}'.format(mytag['instanceTag'], mytag['channel'], val))

        if self.online:
            if val:
                self.__driver.Set('MuteControl', 'On', {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})
            else:
                self.__driver.Set('MuteControl', 'Off', {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})

            self.__driver.Update('MuteControl', {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})


    def mute_descrete_raw(self, instancetag, chan, val):
        self.print_me('mute_descrete_raw {}, chan:{}, {}'.format(instancetag, chan, val))
        self.__driver.Set('MuteControl', val, {'Instance Tag': instancetag, 'Channel': chan})


    def logic_state(self, mytag, val):
        self.print_me('logic_state {}, chan:{}, {}'.format(mytag['instanceTag'], mytag['channel'], val))

        if self.online:
            self.__driver.Set('LogicState', str(val), {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})

            self.__driver.Update('LogicState', {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})


    def logic_state_raw(self, insttag, chan, val):
        self.print_me('logic_state_raw {}, chan:{}, {}'.format(insttag, chan, val))
        if self.online:
            self.__driver.Set('LogicState', str(val), {'Instance Tag': insttag, 'Channel': chan})


    def level_update(self, mytag, level):
        self.print_me('level_update {}, chan:{}, {}'.format(mytag['instanceTag'], mytag['channel'], level))

        if self.online:
            self.__driver.Set('LevelControl', level[0], {'Instance Tag': mytag['instanceTag'], 'Channel': mytag['channel']})


    def dialer_dialpad_press(self, str):
        if self.__dialer_hook_state == 'Active':
            if self.online:
                self.__driver.Set('DTMF', str, {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})

            self.__dialer_dial_string=str
        else:
            self.__dialer_dial_string += str
        
        self._raise_event(self.dialer_instance_status_tag, self.__dialer_dial_string, self.dialer_line)

        return self.__dialer_dial_string


    def dialer_dialpad_back(self):
        self.__dialer_dial_string = self.__dialer_dial_string[:-1]
        self._raise_event(self.dialer_instance_status_tag, self.__dialer_dial_string, self.dialer_line)

        return self.__dialer_dial_string


    def dialer_dialpad_clear(self):
        self.__dialer_dial_string = ''
        self._raise_event(self.dialer_instance_status_tag, self.__dialer_dial_string, self.dialer_line)

        return self.__dialer_dial_string

        
    def dialer_dial_hangup(self, val):
        self.__dialer_refresh_call_status

        self.print_me('dialer_dial_hangup:{} > string:{}, __dialer_status:{}'.format(val, self.__dialer_dial_string, self.__dialer_status))


        if self.online:
            if self.dialer_type == eDialerType.VOIP:
                if val:
                    if self.__dialer_status == 'Idle':
                        self.__driver.Set('VoIPHook', 'Dial', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line, 'Call Appearance': '1', 'Number': str(self.__dialer_dial_string)})
                    elif self.__dialer_status == 'Init':
                        self.__driver.Set('VoIPHook', 'Off', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line, 'Call Appearance': '1'})
                        # self.__driver.Set('VoIPHook', 'On', {'Instance Tag': self.tag['instanceTag'], 'Line': '1', 'Call Appearance': '1'})
                else:
                    if self.__dialer_status == 'Active':
                        self.__driver.Set('VoIPHook', 'End', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line, 'Call Appearance': '1'})
                    else:
                        self.__driver.Set('VoIPHook', 'On', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line, 'Call Appearance': '1'})
            else:
                if val:
                    if self.__dialer_status == 'Idle':
                        self.__driver.Set('TIHook', 'Dial', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line, 'Number': str(self.__dialer_dial_string)})
                    elif self.__dialer_status == 'Init':
                        self.__driver.Set('TIHook', 'Off', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})
                    else:
                        self.__driver.Set('TIHook', 'Off', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})
                else:
                    if self.__dialer_status == 'Connected':
                        self.__driver.Set('TIHook', 'End', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})
                    else:
                        self.__driver.Set('TIHook', 'On', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})



    def dialer_answer_reject(self, val):
        if self.dialer_type == eDialerType.VOIP:
            if self.online:
                if val:
                    self.__driver.Set('VoIPHook', 'Answer', {'Instance Tag':self.dialer_instance_tag, 'Line': self.dialer_line, 'Call Appearance': '1'})
                else:
                    self.__driver.Set('VoIPHook', 'End', {'Instance Tag': self.dialer_instance_tag, 'Line':self.dialer_line, 'Call Appearance': '1'})
            else:
                self._raise_event('VoIPCallStatus', 'Idle',  {'Instance Tag': self.dialer_instance_tag, 'Line':self.dialer_line, 'Call Appearance': '1'})
        else:
            if self.online:
                if val:
                    self.__driver.Set('TIHook', 'Answer', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})
                else:
                    self.__driver.Set('TIHook', 'End', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})
            else:
                self._raise_event('TICallStatus', 'Idle', {'Instance Tag': self.dialer_instance_tag, 'Line': self.dialer_line})
            

    def dialer_set_call_status(self, state):
        self.__dialer_status = state



    def dialer_refresh_dial_string(self):
        # self.print_me('dialer:{}, status tags:{},  dial strings:{}'.format(dialer, self.dialer_instance_status_tags, self.__dialer_dial_string))
        self._raise_event(self.dialer_instance_status_tag, self.__dialer_dial_string, self.dialer_line)


    
    def dialer_get_callerid(self):
        if self.dialer_type == eDialerType.POTS:
            if self.online:
                self.__driver.Update('TICallerID', {'Instance Tag': self.dialer_instance_status_tag, 'Line': self.dialer_line})
                self.__dialer_callerid = self.__driver.ReadStatus(
                    'TICallerID', {'Instance Tag': self.dialer_instance_status_tag, 'Line': self.dialer_line})
                # , 'Line':'1', 'Call Appearance':'1'})
        return self.__dialer_callerid


    def __dialer_refresh_call_status(self):
        self.print_me('> __dialer_refresh_call_status online:{}, tag:{}, tagstatus:{}, line:{}'
                      .format(self.online, self.dialer_instance_tag, self.dialer_instance_status_tag, self.dialer_line))
              
        if self.online:
            self.__driver.Update(self.dialer_type.value, {'Instance Tag': self.dialer_instance_status_tag, 'Line': self.dialer_line})
            self.__dialer_status = self.__driver.ReadStatus(self.dialer_type.value, {'Instance Tag': self.dialer_instance_status_tag, 'Line': self.dialer_line})


    # def voip_ringing_status(self):
    #     if self.online:
    #         self.__driver.Update('VoIPCallerID', {'Instance Tag': self.tag['statusInstanceTag'], 'Line':'1', 'Call Appearance':'1'})
    #         self.__voip_caller_id= self.__driver.ReadStatus('VoIPCallerID', {'Instance Tag': self.tag['statusInstanceTag'], 'Line':'1', 'Call Appearance':'1'})
        
    #     return self.__voip_caller_id

    def __stopwatch_event_cb(self, command, value, qualifier):
        self.print_me('__timer_event_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))
        self._raise_event(command, value, qualifier)

                     
        
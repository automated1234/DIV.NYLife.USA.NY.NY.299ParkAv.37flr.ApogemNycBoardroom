# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button, Label, Level
from abstracts import *



import dv_biamp_data
import re
class UiBiampClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, biamp, poly): 
        AbstractUiClass.__init__(self, alias, tp, data)

        self.__biamp = biamp
        self.__biamp.subscribe(self.__driver_event_cb)
        __tags=dv_biamp_data.data

        self.__poly = poly
        self.currsubpage = ''



        self.__lblincall = Label(tp, 673)
        self.__lblincall.SetVisible(False)
        self.__lbltimer = Label(tp, 674)
        self.__lbltimer.SetVisible(False)
        self.__lbltimer.SetText('')



        self.__btnmutes =  {}
        self.__btnups =  {}
        self.__btndowns =  {}
        self.__lblmutes = {}
        self.__lblupsdowns = {}
        self.__lvllevels = {}
        self.__btndialernums = {}
        self.__lbldialerlabels = {}
        self.__btnpresets = {}
        self.__btnmuteons =  {}
        self.__btnmuteoffs =  {}
        self.__lblmuteonoffs = {}
        self.__btnlogicons =  {}
        self.__btnlogicoffs =  {}
        self.__lbllogics = {}



        self.__btnoffline = Button(tp, 799)
        self.__btnoffline.SetVisible(not self.__biamp.online)


        for tag in __tags:
            if tag['subscription'] =='MuteControl':
                key = tag['instanceTag']+tag['channel']
                self.__btnmutes[key] = Button(tp, tag['muteID'])
                if tag['nameID'] != 9999:
                    self.__lblmutes[key] = Label(tp, tag['nameID'])
                    self.__lblmutes[key].SetText(tag['name'])

            elif tag['subscription'] =='MuteControlDiscrete':
                key = tag['instanceTag']+tag['channel']
                self.__btnmuteons[key] = Button(tp, tag['onID'])
                self.__btnmuteoffs[key] = Button(tp, tag['offID'])
                if tag['nameID'] != 9999:
                    self.__lblmuteonoffs[key] = Label(tp, tag['nameID'])
                    self.__lblmuteonoffs[key].SetText(tag['name'])

            elif tag['subscription'] =='LogicState':
                key = tag['instanceTag']+tag['channel']
                self.__btnlogicons[key] = Button(tp, tag['onID'])
                self.__btnlogicoffs[key] = Button(tp, tag['offID'])
                if tag['nameID'] != 9999:
                    self.__lbllogics[key] = Label(tp, tag['nameID'])
                    self.__lbllogics[key].SetText(tag['name'])


            elif tag['subscription'] =='LevelControl':
                key = tag['instanceTag']+tag['channel']
                self.__btnups[key]=Button(tp, tag['upID'], repeatTime = 0.5)
                self.__btndowns[key]=Button(tp, tag['downID'], repeatTime = 0.5)
                self.__lvllevels[key]=Level(tp, tag['levelID'])
                self.__lvllevels[key].SetRange(tag['minRange'], tag['maxRange'])
                if tag['nameID'] != 9999:
                    self.__lblupsdowns[key]= Label(tp, tag['nameID'])
                    self.__lblupsdowns[key].SetText(tag['name'])

            elif tag['subscription'] == self.__biamp.dialer_type.value:
                self.__btndialernums['num1ID'] = Button(tp, tag['num1ID'])
                self.__btndialernums['num2ID'] = Button(tp, tag['num2ID'])
                self.__btndialernums['num3ID'] = Button(tp, tag['num3ID'])
                self.__btndialernums['num4ID'] = Button(tp, tag['num4ID'])
                self.__btndialernums['num5ID'] = Button(tp, tag['num5ID'])
                self.__btndialernums['num6ID'] = Button(tp, tag['num6ID'])
                self.__btndialernums['num7ID'] = Button(tp, tag['num7ID'])
                self.__btndialernums['num8ID'] = Button(tp, tag['num8ID'])
                self.__btndialernums['num9ID'] = Button(tp, tag['num9ID'])
                self.__btndialernums['num0ID'] = Button(tp, tag['num0ID'])
                self.__btndialernums['numHashID'] = Button(tp, tag['numHashID'])
                self.__btndialernums['numStarID'] = Button(tp, tag['numStarID'])
                self.__btndialernums['numBackID'] = Button(tp, tag['numBackID'])
                self.__btndialernums['numClearID'] = Button(tp, tag['numClearID'])
                self.__btndialernums['numDialID'] = Button(tp, tag['numDialID'])
                self.__btndialernums['numHangupID'] = Button(tp, tag['numHangupID'])
                self.__btndialernums['numAnswerCallID'] = Button(tp, tag['numAnswerCallID'])
                self.__btndialernums['numRejectCallID'] = Button(tp, tag['numRejectCallID'])
                self.__lbldialerlabels['labelDialStringID'] = Label(tp, tag['labelDialStringID'])
                self.__lbldialerlabels['labelCallerID'] = Label(tp, tag['labelCallerID'])
                self.__lbldialerlabels['labelStatusID'] = Label(tp, tag['labelStatusID'])
                # self.__lbldialerlabels['nameID'] = Label(tp, tag['nameID'])
                # self.__lbldialerlabels['nameID'].SetText(tag['name'])

            elif tag['subscription'] =='presettbd':
                self.__btnpresets[tag['instanceTag']] = Button(tp, tag['presetID'])
                self.__btnpresets[tag['instanceTag']].SetText(tag['name'])



        def __find_tag_by_type_and_id(type, id):
            for tag in __tags:
                if tag['subscription'] == type:
                    vals=list(tag.values())
                    if id in vals:
                        return tag

            self.print_me('ERR > subcription/type:{} and buttonId:{} not found'.format(type, id))
            return None        
        

        def __find_tag_by_type(type):
            for tag in __tags:
                if tag['subscription'] == type:
                    return tag

            self.print_me('ERR > subcription/type:{} not found'.format(type))
            return None        


        @event(list(self.__btndialernums.values()), ['Pressed', 'Released'])
        def __btndialernumspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                tag = __find_tag_by_type(self.__biamp.dialer_type.value)
                if tag is not None:
                    if button.ID in list(tag.values()):
                        mykey = list(tag.keys())[list(tag.values()).index(button.ID)]  
                    else:
                        self.print_me('ERR > button.ID:{} not found in:{} tag'.format(button.ID, self.__biamp.dialer_type.value))
                else:
                    return

                val = re.findall(r'\d+', mykey)
                if len(val) != 0:
                    if val[0].isdigit():
                        self.__lbldialerlabels['labelDialStringID'].SetText(biamp.dialer_dialpad_press(val[0]))
                elif mykey=='numHashID':
                    self.__lbldialerlabels['labelDialStringID'].SetText(biamp.dialer_dialpad_press('#'))
                elif mykey=='numStarID':
                    self.__lbldialerlabels['labelDialStringID'].SetText(biamp.dialer_dialpad_press('*'))
                elif mykey=='numBackID':
                    self.__lbldialerlabels['labelDialStringID'].SetText(biamp.dialer_dialpad_back())
                elif mykey=='numClearID':
                    self.__lbldialerlabels['labelDialStringID'].SetText(biamp.dialer_dialpad_clear())
                elif mykey=='numDialID':
                    biamp.dialer_dial_hangup(True)
                elif mykey=='numHangupID':
                    biamp.dialer_dial_hangup(False)
                    self.__lbldialerlabels['labelDialStringID'].SetText(biamp.dialer_dialpad_clear())

                elif mykey=='numAnswerCallID':
                    biamp.dialer_answer_reject(True)
                    self._raise_event_one(biamp.dialer_type.value, 'answered', 'Pressed')
                elif mykey=='numRejectCallID':
                    biamp.dialer_answer_reject(False)
                    self._raise_event_one(biamp.dialer_type.value, 'rejected', 'Pressed')
            else:
                button.SetState(0)
                

        @event(list(self.__btnmutes.values()), 'Pressed')
        def __btnmutespress(button, state):
            tag=__find_tag_by_type_and_id('MuteControl', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, channel:{}, muteID:{}'.format(tag['instanceTag'], tag['channel'], tag['muteID']))
                biamp.mute_toggle(tag)


        @event(list(self.__btnmuteons.values()), 'Pressed')
        def __btnmuteonspress(button, state):
            tag=__find_tag_by_type_and_id('MuteControlDiscrete', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, channel:{}, onID:{}'.format(tag['instanceTag'], tag['channel'], tag['onID']))
                biamp.mute_discrete(tag, True)


        @event(list(self.__btnmuteoffs.values()), 'Pressed')
        def __btnmuteoffspress(button, state):
            tag=__find_tag_by_type_and_id('MuteControlDiscrete', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, channel:{}, offID:{}'.format(tag['instanceTag'], tag['channel'], tag['offID']))
                biamp.mute_discrete(tag, False)

        
        @event(list(self.__btnlogicons.values()), 'Pressed')
        def __btnlogiconspress(button, state):
            tag=__find_tag_by_type_and_id('LogicState', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, channel:{}, onID:{}'.format(tag['instanceTag'], tag['channel'], tag['onID']))
                biamp.logic_state(tag, True)


        @event(list(self.__btnlogicoffs.values()), 'Pressed')
        def __btnlogicoffspress(button, state):
            tag=__find_tag_by_type_and_id('LogicState', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, channel:{}, offID:{}'.format(tag['instanceTag'], tag['channel'], tag['offID']))
                biamp.logic_state(tag, False)


        @event(list(self.__btnpresets.values()),  ['Pressed', 'Released'])
        def __btnpresetspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                tag=__find_tag_by_type_and_id('presettbd', button.ID)
                if tag is not None:
                    self.print_me('> instanceTag:{}, presetID:{}'.format(tag['instanceTag'], tag['presetID']))
                    biamp.preset(tag['instanceTag'])
            else:
                button.SetState(0)


        @event(list(self.__btnups.values()), ['Pressed', 'Released', 'Repeated'])
        def BtnUpsPress(button, state):
            tag=__find_tag_by_type_and_id('LevelControl', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, channel:{}, upID:{}, online:{}'.format(tag['instanceTag'], tag['channel'], tag['upID'], self.__biamp.online))

                key = tag['instanceTag']+tag['channel']

                if state == 'Pressed':
                    button.SetState(1)
                    # LvlLevels[tag['instanceTag']].SetRange(tag['minRange'], tag['maxRange'], 1)
                    self.__lvllevels[key].Inc()
                    biamp.level_update(tag, self.__lvllevels[key].Level)
                elif state == 'Repeated':
                    # LvlLevels[tag['instanceTag']].SetRange(tag['minRange'], tag['maxRange'], 3)
                    self.__lvllevels[key].Inc()
                    biamp.level_update(tag, self.__lvllevels[key].Level)
                else:
                    button.SetState(0)


        @event(list(self.__btndowns.values()), ['Pressed', 'Released', 'Repeated'])
        def __btndownspress(button, state):
            tag=__find_tag_by_type_and_id('LevelControl', button.ID)
            if tag is not None:
                self.print_me('> instanceTag:{}, downID:{}, online:{}'.format(tag['instanceTag'], tag['downID'], self.__biamp.online))

                key = tag['instanceTag']+tag['channel']

                if state == 'Pressed':
                    button.SetState(1)
                    self.__lvllevels[key].Dec()
                    biamp.level_update(tag, self.__lvllevels[key].Level)
                elif state == 'Repeated':
                    self.__lvllevels[key].Dec()
                    biamp.level_update(tag, self.__lvllevels[key].Level)
                else:
                    button.SetState(0)
     #END CONSTRUCTOR


    def __driver_event_cb(self, command, value, qualifier):
        self.print_me('__driver_event_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command == 'ConnectionStatus':
            if value == 'Connected':  
                self.__btnoffline.SetVisible(False)
            else:
                self.__btnoffline.SetVisible(True)
        elif command == 'MuteControl':
            key = qualifier['Instance Tag']+ qualifier['Channel']

            if value == 'On':
                if key in self.__btnmutes.keys():
                    self.__btnmutes[key].SetState(1)

                    # if qualifier['Instance Tag'] == "RM1_MIC_MUTE":
                    #     if self.currsubpage.startswith=='main_center_vtc_':                        
                    #         self.__poly.mic_mute(True)

                elif key in self.__btnmuteons.keys():
                    self.__btnmuteons[key].SetState(1)
                    self.__btnmuteoffs[key].SetState(0)
                    self.print_me('__btnmuteons > key:{}, value:{}'.format(key, value))


            else:
                if key in self.__btnmutes.keys():
                    self.__btnmutes[key].SetState(0)

                    # if qualifier['Instance Tag'] == "RM1_MIC_MUTE":
                    #     if self.currsubpage.startswith=='main_center_vtc_':                        
                    #         self.__poly.mic_mute(False)

                elif key in self.__btnmuteons.keys():
                    self.__btnmuteons[key].SetState(0)
                    self.__btnmuteoffs[key].SetState(1)
                    self.print_me('__btnmuteons > key:{}, value:{}'.format(key, value))

        
        elif command == 'LogicState':
            key = qualifier['Instance Tag']+ qualifier['Channel']

            if value == 'True':
                if key in self.__btnlogicons.keys():
                    self.__btnlogicons[key].SetState(1)
                    self.__btnlogicoffs[key].SetState(0)
            else:
                if key in self.__btnlogicons.keys():
                    self.__btnlogicons[key].SetState(0)
                    self.__btnlogicoffs[key].SetState(1)
           
                
        elif command == 'LevelControl':
            # currentLevel = self.dsp.ReadStatus('LevelControl', {'Instance Tag': qualifier['Instance Tag'], 'Channel': '1'})
            key = qualifier['Instance Tag']+ qualifier['Channel']
            self.__lvllevels[key].SetLevel(value)
            

        elif command == self.__biamp.dialer_type.value:
            self._raise_event_one(command, value, qualifier)

            # if self.__biamp.dialer_type==eDialerType.VOIP:
            #     pass
            #     # if qualifier['Call Appearance'] == '1' and qualifier['Line'] == '1':
            #     #     self.__biamp.voip_set_call_status(value, self.__dialer)
            #     #     self.__lbldialerlabels['labelVoipStatusID'].SetText(value)
            #     #     if value == 'Active':
            #     #         self.__btndialernums['numHangupID'].SetState(1)
            #     #     # elif value == 'Ringing':
            #     #     #     if self._data['enableincomingcalls']:
            #     #     #         self.__uinav.show_popup('pop_incoming')  #//disabled per client req.  no incoming calls accepted
            #     #     #     # callerid = self.__biamp.voip_ringing_status()
            #     #     #     # self.__lblvoiplabels['labelCallerID'].SetText(callerid)
            #     #     # elif value == 'Idle':
            #     #     #     if self._data['enableincomingcalls']:
            #     #     #         self.__uinav.hide_popup('pop_incoming')  #//disabled per client
            #     #     #     self.__btndialernums['numHangupID'].SetState(0)
            #     #     else:
            #     #         self.__btndialernums['numHangupID'].SetState(0)
            # else:
            
            self.__biamp.dialer_set_call_status(value)
            self.__lbldialerlabels['labelStatusID'].SetText(value)

            # 'Init'
            # 'Fault'
            # 'Idle'
            # 'Dialing'
            # 'Ringback'
            # 'Ringing'
            # 'Busy Tone'
            # 'Connected Mute'
            # 'Dropped'
            # 'Error Tone'
            # 'Connected'
            if value == 'Init':
                self.__biamp.dialer_dial_hangup(True)
                self.__biamp.dialer_dial_hangup(False)

            elif value == 'Active':
                self.__lblincall.SetVisible(True)
                self.__lbltimer.SetVisible(True)
            else:
                self.__lblincall.SetVisible(False)
                self.__lbltimer.SetVisible(False)
    

            if value == 'Active' or value == 'Connected' or value == 'Dialing' or value == 'Connected Mute':
                self.__btndialernums['numDialID'].SetState(1)
                self.__btndialernums['numHangupID'].SetState(0)
            elif value == 'Ringing':
                callid = self.__biamp.dialer_get_callerid()
                self.__lbldialerlabels['labelCallerID'].SetText(callid)
            elif value == 'Idle':
                self.__btndialernums['numDialID'].SetState(0)
                self.__btndialernums['numHangupID'].SetState(0)
                self.__lbldialerlabels['labelDialStringID'].SetText(self.__biamp.dialer_dialpad_clear())
            elif value == 'Dropped':
                self.__biamp.dialer_dial_hangup(False)
                self.__btndialernums['numDialID'].SetState(0)
                self.__btndialernums['numHangupID'].SetState(0)
                self.__lbldialerlabels['labelDialStringID'].SetText(self.__biamp.dialer_dialpad_clear())

            else:
                self.__btndialernums['numDialID'].SetState(0)
                self.__btndialernums['numHangupID'].SetState(0)


        # elif command == 'Running' or command == 'Stopped' or command == 'Paused':  #custom
        #     self.__lbltimer.SetText(qualifier)
        #     if command == 'Running':
        #         self.__lblincall.SetVisible(True)
        #         self.__lbltimer.SetVisible(True)
        #     else:
        #         self.__lblincall.SetVisible(False)
        #         self.__lbltimer.SetVisible(False)



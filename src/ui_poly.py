# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button, Label, Level
from extronlib.system import Clock, MESet, Timer, Wait
from abstracts import AbstractUiClass


class UiPolyClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, poly): 
        AbstractUiClass.__init__(self, alias+'poly', tp, data)

        self.__btnoffline = Button(tp, 1199)
        self.__btnoffline.SetVisible(not poly.online)


        self.__lblincall = Label(tp, 1173)
        self.__lblincall.SetVisible(False)
        self.__lbltimer = Label(tp, 1174)
        self.__lbltimer.SetVisible(False)
        self.__lbltimer.SetText('')

        self.__shift = False

        self.__poly = poly
        self.__poly.subscribe(self.__driver_event_cb)
        # self.__dial_string = ''


        __keys = {
            1201:'1!',
            1202:'2@',
            1203:'3#',
            1204:'4$',
            1205:'5%',
            1206:'6^',
            1207:'7&',
            1208:'8*',
            1209:'9(',
            1210:'0)',
            1211:'qQ',
            1212:'wW',
            1213:'eE',
            1214:'rR',
            1215:'tT',
            1216:'yY',
            1217:'uU',
            1218:'iI',
            1219:'oO',
            1220:'pP',
            1221:'aA',
            1222:'sS',
            1223:'dD',
            1224:'fF',
            1225:'gG',
            1226:'',
            1227:'jJ',
            1228:'kK',
            1229:'lL',
            1230:'zZ',
            1231:'xX',
            1232:'cC',
            1233:'vV',
            1234:'xX',
            1235:'bB',
            1236:'nN',
            1237:'mM',
            1238:'-_',
            1239:'..',
            1240:'@@',
            1242:'  ',
        }

        __keydials = {
            1170:'DIAL',
            1243:'BACKSP',
            1244:'CLEAR',
            1245:'SHIFT'
        }

        __iremulates = {
            1151:'1',
            1152:'2',
            1153:'3',
            1154:'4',
            1155:'5',
            1156:'6',
            1157:'7',
            1158:'8',
            1159:'9',
            1160:'0',
            1161:'*',
            1162:'#',
            1163:'.',
            1129:'keyboard',
            1130:'menu',
            1131:'up',
            1132:'down',
            1133:'left',
            1134:'right',
            1135:'select',
            1136:'delete',
            1137:'call',
            1138:'back',   
            1139:'camera',
            1140:'directory',
            # 1141:'graphics',
            1142:'hangup',    #add back to it
            1143:'home',      #add menu to it
            1144:'info',
            1145:'mute',
            1146:'period',
            1147:'volume+',
            1148:'volume-',
        }


        __layouts = {
            1121:'sidebyside',
            # 1122:'pictuerinpicture',
            1123:'contentonly',
        }

  
        __hooks = {
            1166:'Dial IP',
            1167:'Dial Auto',
            1168:'Answer',
            1169:'Hangup All',  
        }


        __shares = {
            # 1250:0,
            1251:1,
            1252:2,
        }

        __sharenames = {
            1251:data['in1name'],
            1252:data['in2name'],
        }


        self.__sharestartstop = {
            1250:0,
            1260:10
        }


        __vols = {
            621:'up',
            622:'down',
        }

        __btnvols = {}

        for ky in __vols:  
            __btnvols[ky]=Button(tp, ky, repeatTime = 0.5)

        self.__lvlvol=Level(tp, 624)
        self.__lvlvol.SetRange(0, 50)


        # self.__ignoredrvrvolfb=False

        __btniremulates =  {}
        __btnlayouts =  {}
        __btnhooks =  {}
        __btnkeys =  {}
        __btnkeydials =  {}
        self.__btnshares =  {}
        self.__btnsharestartstop =  {}


        # self.__btnpiplayout = Button(tp, 1141)

        self.__lbldial = Label(tp, 1200)

        for ky in __iremulates:  
            __btniremulates[ky]=Button(tp, ky)

        for ky in __layouts:  
            __btnlayouts[ky]=Button(tp, ky)

        for ky in __hooks:  
            __btnhooks[ky]=Button(tp, ky)

        for ky in __keys:  
            __btnkeys[ky]=Button(tp, ky)

        for ky in __keydials:  
            __btnkeydials[ky]=Button(tp, ky)

        for ky in __shares:  
            self.__btnshares[ky]=Button(tp, ky)
            self.__btnshares[ky].SetText(__sharenames[ky])
        self.__msetbtnshares = MESet(list(self.__btnshares.values()))


        for ky in self.__sharestartstop:  
            self.__btnsharestartstop[ky]=Button(tp, ky)
        self.__msetbtnsharestartstop = MESet(list(self.__btnsharestartstop.values()))




        @event(list(__btniremulates.values()), ['Pressed', 'Released'])
        def __btniremulatepress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__poly.iremulates(__iremulates[button.ID])
                if __iremulates[button.ID] == 'hangup':
                    self.__sharestartstop_me(1250)

            else:
                button.SetState(0)


        @event(list(__btnlayouts.values()), ['Pressed', 'Released'])
        def __btnalyoutspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                if __layouts[button.ID]=='sidebyside':
                    self.__poly.driver.Set('ConfigPresentationContent', 'Dual')
                elif __layouts[button.ID]=='contentonly':
                    self.__poly.driver.Set('ConfigPresentationContent', 'Single')
                elif __layouts[button.ID]=='pictuerinpicture':
                    self.__poly.driver.Set('ConfigPresentationSelfView', 'Corner')
            else:
                button.SetState(0)
                if __layouts[button.ID]=='pictuerinpicture':
                    self.__poly.driver.Set('ConfigPresentationSelfView', 'Full Screen')


        @event(list(__btnhooks.values()), ['Pressed', 'Released'])
        def __btnhookspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self._raise_event_one('CallInfoState', __hooks[button.ID], 'Pressed')
                self.__poly.hooks(__hooks[button.ID])
            else:
                button.SetState(0)


        @event(list(__btnkeys.values()), ['Pressed', 'Released'])
        def __btnkeyspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                if not self.__shift:
                    self.__lbldial.SetText(self.__poly.dialpad_press(__keys[button.ID][:1]))
                else:
                    self.__lbldial.SetText(self.__poly.dialpad_press(__keys[button.ID][-1:]))

            else:
                button.SetState(0)


        @event(list(__btnvols.values()), ['Pressed', 'Released', 'Repeated'])
        def __btnvolspress(button, state):
            self.print_me('__btnvolspress: {}, lvllevel{}'.format(state, self.__lvlvol.Level))

            if state == 'Pressed' or state == 'Repeated':
                button.SetState(1)
                if __vols[button.ID]=='up':
                    self.__lvlvol.Inc()
                else:
                    self.__lvlvol.Dec()
                self.__poly.volume_update(self.__lvlvol.Level)

            else:
                button.SetState(0)
        
 
        @event(self.__msetbtnshares.Objects, ['Pressed', 'Released'])
        def __msetbtnsharespress(button, state):
            if button is not None:
                if state == 'Pressed':
                    self.__msetbtnshares.SetCurrent(button.MirroredParent)
                    self.__poly.shares(__shares[button.ID])


        @event(self.__msetbtnsharestartstop.Objects, ['Pressed', 'Released'])
        def __msetbtnsharestartstoppress(button, state):
            if button is not None:
                if state == 'Pressed':
                    self.__sharestartstop_me(button.ID)
                    # self.__msetbtnsharestartstop.SetCurrent(button.MirroredParent)
                    # self.__poly.shares(__sharestartstop[button.ID])
                    # if button.ID==1250:
                    #     self.__msetbtnshares.SetCurrent(None)


        @event(list(__btnkeydials.values()), ['Pressed', 'Released'])
        def __btnkeydialspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                
                if __keydials[button.ID] == 'DIAL':
                    self.__poly.dialpad_dial()
                elif __keydials[button.ID] == 'BACKSP':
                    self.__lbldial.SetText(self.__poly.dialpad_back())
                elif __keydials[button.ID] == 'CLEAR':
                    self.__lbldial.SetText(self.__poly.dialpad_clear())
                elif __keydials[button.ID] == 'SHIFT':
                    self.__shift = not self.__shift
                    if not self.__shift:
                        button.SetState(0)
                    # self.__lbldial.SetText(self.__poly.dialpad_shift())
                        
            else:
                if __keydials[button.ID] != 'SHIFT':
                    button.SetState(0)

    #END CONSTRUCTOR

    def update_sharesfb(self, val):
        if val==0:
            self.__msetbtnsharestartstop.SetCurrent(self.__btnsharestartstop[1250])
        else:
            self.__msetbtnsharestartstop.SetCurrent(self.__btnsharestartstop[1260])


    def __sharestartstop_me(self, val):  
        self.print_me('__sharestartstop_me val:{}'.format(val))  #1250 or 1260
        self.__msetbtnsharestartstop.SetCurrent(self.__btnsharestartstop[val])
        self.__poly.shares(self.__sharestartstop[val])
        if val==1250:
            self.__msetbtnshares.SetCurrent(None)


    def __driver_event_cb(self, command, value, qualifier):
        self.print_me('__driver_event_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command == 'ConnectionStatus':
            if value == 'Connected':  
                self.__btnoffline.SetVisible(False)
                self.__lvlvol.SetLevel(30)
            else:
                self.__btnoffline.SetVisible(True)
        # elif command == 'CallInfoState':
        #     if value == "Ringing'":
        #         self.__lblincall.SetVisible(True)
        #         self.__lbltimer.SetVisible(True)
        #     else:
        #         self.__lblincall.SetVisible(False)
        #         self.__lbltimer.SetVisible(False)
        elif command == 'VideoContentSource':
                if value == "Stop":
                    self.update_sharesfb(0)
                    # self.__msetbtnshares.SetCurrent(self.__btnshares[1250])
                else:
                    self.update_sharesfb(1)

        elif command == 'CallInfoState':
            if value == "Connected":
                self.__lblincall.SetVisible(True)
                self.__lbltimer.SetVisible(True)
            else:
                self.__lblincall.SetVisible(False)
                self.__lbltimer.SetVisible(False)

            if value == "Disconnected":
                self.__lbldial.SetText('')


        elif command == 'Volume':
            self.__lvlvol.SetLevel(value)

        # elif command == 'Running' or command == 'Stopped' or command == 'Paused':
        #     self.__lbltimer.SetText(qualifier)
        #     if command == 'Running':
        #         self.__lblincall.SetVisible(True)
        #         self.__lbltimer.SetVisible(True)
        #     else:
        #         self.__lblincall.SetVisible(False)
        #         self.__lbltimer.SetVisible(False)

        self._raise_event_one(command, value, qualifier)


        

  

    

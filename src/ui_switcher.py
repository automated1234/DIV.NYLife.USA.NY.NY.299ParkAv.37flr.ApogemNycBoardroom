# "author": "ted.cygan"

from extronlib import event
from extronlib.system import MESet
from drivers.MirrorUI import Button, Label, Level
from abstracts import AbstractUiClass
from dv_switcher import SwitcherClass


class UiSwitcherClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, switcher): 
        AbstractUiClass.__init__(self, alias, tp, data)

        self.__switcher = switcher
        self.__switcher.subscribe(self.__driver_event_cb)

        # self.__room = room
        # self.__room.subscribe(self.__room_event_cb)



        self.__ins = {
            400:data['in0name'],
            401:data['in1name'],
            402:data['in2name'],
            403:data['in3name'],
            404:data['in4name'],
        }

        self.__outs = {
            431:'',
            432:'',
        }


        self.__btnins = {}
        self.__btnouts = {}

        self.__btnoffline = Button(tp, 599)
        self.__btnoffline.SetVisible(not self.__switcher.online)


        for ky in self.__ins:
            self.__btnins[ky]=Button(tp, ky, holdTime=3)
            self.__btnins[ky].SetText(self.__ins[ky])


        for ky in self.__outs:
            self.__btnouts[ky]=Button(tp, ky)


        self.__msetbtnins = MESet(list(self.__btnins.values()))
        self.__currin=0


        @event(self.__msetbtnins.Objects, ['Tapped', 'Held'])
        def __msetbtninspress(button, state):

            if button is not None:
                if state == 'Tapped':
                    if button.ID==405:
                        self.__select_input_special(8)
                    else:
                        self.select_input(button.ID-400)


        @event(list(self.__btnouts.values()), ['Pressed', 'Released'])
        def __btnoutspress(button, state):

            if button is not None:
                if state == 'Pressed':
                    button.SetState(1)
                    self.__switcher.switch_me(self.__currin,  button.ID-430)  
                else:
                    button.SetState(0)


    def __driver_event_cb(self, command, value, qualifier):
        self.print_me('__driver_event_cb c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command == 'ConnectionStatus':
            if value == 'Connected':  
                self.__btnoffline.SetVisible(False)
            else:
                self.__btnoffline.SetVisible(True)
                
        elif command == 'MATRIXROUTE':
            if value <= self._data['switcher_inscount']:
                if qualifier <= self._data['switcher_outscount']:
 
                    self.__btnouts[430+qualifier].SetText(self.__ins[value+400].alias)
                    # self.__lbloutsstatus[480+qualifier].SetText(self.__ins[value+400].alias)

                else:
                    self.print_me('ERR switcher invalid out:{}'.format(qualifier))
            else:
                self.print_me('ERR switcher invalid in:{}'.format(value))

        
        # elif command == 'INPUTSYNCS':
        #     if self.__lastsyncs  != value:
        #         self.__lastsyncs = value

        #         for ky in value:
        #             if value[ky]=='1':
        #                 self.__btnins[ky+400].SetState(1)
        #                 # self.__btnins[ky+400].SetText('ACTIVE')
        #                 self.__switcher.switch_me(ky, 1)
        #                 self.__switcher.switch_me(ky, 2)

        #             else:
        #                 self.__btnins[ky+400].SetState(0)
        #                 # self.__btnins[ky+400].SetText('')

        #     self.print_me('WARN same input_syncs as last time checked:{}'.format(value))


        # elif command == 'INPUTSYNC':
        #     if qualifier==1:
        #         self.__switcher.switch_me(value, 1)
        #         self.__switcher.switch_me(value, 2)
        #         self.__btnins[value+400].SetState(1)

        #     else:
        #         self.__btnins[value+400].SetState(0)


    def select_input(self, input):
        self.__currin = input
        self.__msetbtnins.SetCurrent(self.__btnins[input+400])


    def __select_input_special(self, input):
        self.__currin = input
        self.__msetbtnins.SetCurrent(self.__btnins[405])



    # def __room_event_cb(self, command, value, qualifier):
    #     self.print_me('__room_event_cb c:{}, v:{}, q:{}, currin:{}'.format(command, value, qualifier, self.__currin))

    #     if command=='input_change':
    #         if value != self.__currin:
    #             self.select_input(value)




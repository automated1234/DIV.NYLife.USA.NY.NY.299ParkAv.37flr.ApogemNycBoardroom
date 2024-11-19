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
            405:data['in5name'],
            406:data['in6name'],
            407:data['in7name'],
            408:data['in8name'],
            409:data['in9name'],
            410:data['in10name'],
            411:data['in11name'],
            412:data['in12name'],
            413:data['in13name'],
            414:data['in14name'],
            415:data['in15name'],
            416:data['in16name'],
        }

        self.__outs = {
            431:'',
            432:'',
            433:'',
            434:'',
            435:'',
            436:'',
            437:'',
            438:'',
            439:'',
            440:'',
            441:'',
            442:'',
            443:'',
            444:'',
            445:'',
            446:'',
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
                
        elif command == 'OutputTieStatus':
            # if qualifier['Tie Type'] == 'Video' or  qualifier['Tie Type'] == 'Audio/Video':
            out_ = int(qualifier['Output'])
            in_ = int(value)
            if out_ > 0 and out_ <= SwitcherClass.SWITCHER_OUTSCOUNT and in_ >= 0 and in_ <= SwitcherClass.SWITCHER_INSCOUNT:
                self.__btnouts[out_ + 430].SetText(self.__ins[in_ + 400])  
            # else:
            #     self.print_me('ERR invalid in:{} or out:{}'.format(in_, out_))


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




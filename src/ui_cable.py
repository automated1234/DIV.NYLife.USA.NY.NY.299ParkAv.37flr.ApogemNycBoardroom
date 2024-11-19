# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button
from abstracts import AbstractUiClass


class UiCableClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, cable, switcher): 
        AbstractUiClass.__init__(self, alias, tp, data)

        self.__btnoffline = Button(tp, 299)
        self.__cable = cable
        self.__cable.subscribe(self.__driver_event_cb)
        # self.__switcher = switcher
        # self.__switcher.subscribe(self.__switcher_event_cb)


        # __nums = {
        #     211:'1',
        #     212:'2',
        #     213:'3',
        #     214:'4',
        #     215:'5',
        #     216:'6',
        #     217:'7',
        #     218:'8',
        #     219:'9',
        #     220:'0',
        #     221:'Clear',
        #     222:'Enter',
        # }

        __chupdown = {
            225:'Up',
            226:'Down',
        }

        # __menus = {
        #     229:'Menu',
        #     230:'Guide',
        #     231:'Up',
        #     232:'Down',
        #     233:'Left',
        #     234:'Right',
        #     235:'OK',
        #     235:'Exit',
        # }

        # self.__btnblankvideo = Button(tp, 240)

        # __presets = {
        #     # 241:'Blank',
        #     242:'CNN',
        #     243:'CNBC',
        #     244:'FOX NEWS',
        #     245:'NYL',
        # }

        __presets = {
            241:'007',
            242:'004',
            243:'002',
            244:'027',
            245:'017',
            246:'021',
            247:'023',
            248:'6-1',
        }

        __btnchupdown =  {}
        __btnpresets =  {}



        for key in __chupdown:  
            __btnchupdown[key]=Button(tp, key)

        for key in __presets:  
            __btnpresets[key]=Button(tp, key)


        @event(list(__btnchupdown.values()), ['Pressed', 'Released'])
        def __btnchupdownpress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__cable.channel_updown(__chupdown[button.ID])
            else:
                button.SetState(0)


        @event(list(__btnpresets.values()), ['Pressed', 'Released'])
        def __btnpresetspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__cable.channel_discrete(__presets[button.ID])
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



  

    

# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button
from abstracts import AbstractUiClass


class UiLightsClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, lights): 
        AbstractUiClass.__init__(self, alias+'lights', tp, data)

        self.__btnoffline = Button(tp, 899)
        self.__lights = lights
        self.__lights.subscribe(self.__driver_event_cb)

        # tbd
        __lights = {
            801:'#AREA,{},6,1\r'.format(data['lights_id']),
            802:'#AREA,{},6,2\r'.format(data['lights_id']),
            803:'#AREA,{},6,3\r'.format(data['lights_id']),
            804:'#AREA,{},6,4\r'.format(data['lights_id']),
            805:'#AREA,{},6,0\r'.format(data['lights_id']),
            # 806:'#DEVICE,{},6,3\r'.format(data['lights_id']),
            # 807:'#DEVICE,{},7,3\r'.format(data['lights_id']),
            # 808:'#DEVICE,{},8,3\r'.format(data['lights_id']),
            # 809:'#DEVICE,{},9,3\r'.format(data['lights_id']),
            # 810:'#DEVICE,{},10,3\r'.format(data['lights_id']),
        }

   
        __shades = {
            811:'#SHADEGRP,{},6,0\r'.format(data['shades_id1']),
            812:'#SHADEGRP,{},6,30\r'.format(data['shades_id1']),
            # 813:'#SHADEGRP,78,6,0\r',
            # 814:'#SHADEGRP,78,6,30\r',
        }


        self.__btnlights = {}
        self.__btnshades = {}


        for ky in __lights:
            self.__btnlights[ky]=Button(tp, ky)
            self.__btnlights[ky].SetText(data['lights_name'+str(ky-800)]) 


        for ky in __shades:
            self.__btnshades[ky]=Button(tp, ky)
            self.__btnshades[ky].SetText(data['shades_name'+str(ky-810)]) 




        @event(list(self.__btnlights.values()), ['Pressed', 'Released'])
        def __btnlightspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__lights.send_direct(__lights[button.ID])

            else:
                button.SetState(0)


        @event(list(self.__btnshades.values()), ['Pressed', 'Released'])
        def __btnshadespress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__lights.send_direct(__shades[button.ID])
            else:
                button.SetState(0)


        self.__btnoffline.SetVisible(not self.__lights.online)

    #END CONSTRUCTOR


    def __driver_event_cb(self, command, value, qualifier):
        self.print_me('__driver_event_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command == 'ConnectionStatus':
            if value == 'Connected':  
                self.__btnoffline.SetVisible(False)
            else:
                self.__btnoffline.SetVisible(True)



 

    

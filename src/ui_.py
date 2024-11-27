# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button, Label, Level
from extronlib.system import MESet, Wait
from abstracts import *
import ui_biamp, ui_switcher, ui_cam, ui_display, ui_poly, ui_lights



class UiCreateClass():
    def __init__(self, alias, tp, data, switcher, biamp, cams, displays, room, poly, lights, onebeyond):
        uiswitcher = ui_switcher.UiSwitcherClass(alias, tp, data, switcher)
        self.uicam = ui_cam.UiCamClass(alias, tp, data, cams, switcher)
        uidisplay = ui_display.UiDisplayClass(alias, tp, data, displays)
        uipoly = ui_poly.UiPolyClass(alias, tp, data, poly)
        uilights = ui_lights.UiLightsClass(alias, tp, data, lights)
        uibiamp = ui_biamp.UiBiampClass(alias, tp, data, biamp, poly)
        self.ui = UiClass(alias, tp, data, room, switcher, biamp, uibiamp, uipoly, uidisplay, uiswitcher, self.uicam, onebeyond)



class UiClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, room, switcher, biamp, uibiamp, uipoly, uidisplay, uiswitcher, uicam, onebeyond): 
        AbstractUiClass.__init__(self, alias, tp, data)

        self.__biamp = biamp
        self.__switcher = switcher
        self.__uibiamp = uibiamp
        self.__uibiamp.subscribe_one(self.__uibiamp_event_cb)
        self.__uipoly = uipoly
        self.__uipoly.subscribe_one(self.__uipoly_event_cb)
        self.__uidisplay = uidisplay
        self.__uidisplay.subscribe_one(self.__uidisplay_event_cb)

        self.__uiswitcher = uiswitcher
        self.__onebeyond=onebeyond
        self.__uicam=uicam


        self.__room = room
        self.__room.subscribe(self.__room_event_cb)


        __pages = ['splash', 'main']
        self.__lastpage = 'splash'


        self.__popup_busy_display = 'stop'
        __btnwarmcoolstop = Button(tp, 107)
        self.__lblwarmcoolmess = Label(tp, 108)
        self.__lblwarmcoolclock = Label(tp, 109)
        self.__lblwarmcoolclock.SetText('')



        self.__mainmenu = {
            # 111:'main_center_present_laptop',  #tbd bc not sure from gui
            112:'main_center_vtc_menu',
            113:'main_center_vtclaptop',
            114:'main_center_atc',  
            115:'main_center_present_laptop',
            116:'main_center_room_display', 
        }


        self.__maincentersubs = {
            # 121:'main_center_present_laptop',
            # 122:'main_center_present_cable',
            # 123:'main_center_present_vtc',

            131:'main_center_vtc_cam',
            # 132:'main_center_vtc_source',
            133:'main_center_vtc_dial',
            134:'main_center_vtc_keyboard',
            135:'main_center_vtc_menu',

            139:'main_center_vtclaptop_take',


            141:'main_center_room_display',
            # 142:'main_center_room_audio',
            143:'main_center_room_vtc',
            144:'main_center_room_lights',
            # 100:'main_return',
        }


        self.__popups = {
            40:'popup_close',
            41:'popup_shutdown',
            42:'popup_help',
            43:'popup_incoming_atc',
            44:'popup_incoming_vtc',
            45:'popup_busy',
        }


        self.__btnpopups =  {}
        self.__btnmainmenu= {}
        self.__btnmaincentersubs= {}

  

        __btnoff = Button(tp, 110)




        self.__lblroom = Label(tp, 101)
        self.__lblroom.SetText(self.__room.name)
        self.__lblpoweroff = Label(tp, 102)
        self.__lblsourcename = Label(tp, 201)


        for ky in self.__mainmenu:
            self.__btnmainmenu[ky] = Button(tp, ky)
        self.__msetbtnmainmenu = MESet(list(self.__btnmainmenu.values()))



        for ky in self.__maincentersubs:
            self.__btnmaincentersubs[ky] = Button(tp, ky)  #, holdTime=3)
        self.__msetbtnmaincentersubs = MESet(list(self.__btnmaincentersubs.values()))


        self.__btnreturn = Button(tp, 100)
        self.__btnreturn.SetVisible(False)


        for ky in self.__popups:    
            self.__btnpopups[ky] = Button(tp, ky)



        self.__flip2_splash()


        

        @event(__btnoff, ['Pressed', 'Released'])
        def __btnoffpress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__flip2_splash()
                self.__room.room_off()
            else:
                button.SetState(0)


        @event(__btnwarmcoolstop, ['Pressed', 'Released'])
        def __btnwarmupcooldownstoppress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__uidisplay.warmcool_cancel()
                self.__popups_me('popup_close')
            else:
                button.SetState(0)


        @event(self.__msetbtnmainmenu.Objects, ['Pressed', 'Released'])
        def __msetbtnmainmenupress(button, state):
            if state == 'Pressed':

                if self.__lastpage == 'splash':
                    self.__flip2_main()

                self.__msetbtnmainmenu.SetCurrent(button.MirroredParent)
                self.__menu_select(self.__mainmenu[button.ID])
                self.__room.room_on(self.__mainmenu[button.ID])



        @event(self.__msetbtnmaincentersubs.Objects, ['Pressed', 'Released'])
        def __msetbtnmaincentersubspress(button, state):
            if state == 'Pressed':
                self.__menu_select(self.__maincentersubs[button.ID])


        @event(list(self.__btnpopups.values()), 'Pressed')
        def __btnpopspress(button, state):
            self.__popups_me(self.__popups[button.ID])

    #END CONSTRUCTOR



    def __popups_me(self, name):
            if name in self.__popups.values():
                if name == 'popup_close':
                    for sub in self.__popups:
                        if self.__popups[sub] != 'popup_close':
                            self.__hide_subpage(self.__popups[sub])
                else:
                     self.__show_subpage(name) 
            else:
                self.print_me('ERR popup:{}, doesnt exist'.format(name))


    def __show_subpage(self, name):
        self._tp.ShowPopup(name)

    def __hide_subpage(self, name):
        self._tp.HidePopup(name)


    def __show_page(self, name):
        self._tp.ShowPage(name)
        self.__lastpage = name



    def __hide_all_subpages(self):
        self._tp.HideAllPopups()



    def __room_event_cb(self, command, value, qualifier):
        self.print_me('__room_event_cb c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command=='Off':
            self.__flip2_splash()


    def __uibiamp_event_cb(self, command, value, qualifier):
        self.print_me('__uibiamp_event_cb c:{}, v:{}, q:{}'.format(command, value, qualifier))
        if command == self.__biamp.dialer_type.value:
            if value == 'Ringing':
                self.__popups_me('popup_incoming_atc')
            elif value == 'answered' and qualifier=='Pressed':
                self.__popups_me('popup_close')
            elif value == 'rejected'and qualifier=='Pressed':
                self.__popups_me('popup_close')


    def __uipoly_event_cb(self, command, value, qualifier):
        self.print_me('__uipoly_event_cb c:{}, v:{}, q:{}'.format(command, value, qualifier))
        if command == 'CallInfoState':
            if value == 'Ringing':
                self.__popups_me('popup_incoming_vtc')
            elif value == 'Answer' and qualifier=='Pressed':
                self.__popups_me('popup_close')
            elif value == 'Hangup All' and qualifier=='Pressed':
                self.__popups_me('popup_close')


    def __uidisplay_event_cb(self, command, value, qualifier):
        self.print_me('__uidisplay_event_cb c:{}, v:{}, q:{}'.format(command, value, qualifier))
        if command.startswith('WARMCOOL'):
            if value == 'warmup':
                if self.__popup_busy_display == command or  self.__popup_busy_display == 'stop':
                    self.__popup_busy_display = command
                    self.__lblwarmcoolmess.SetText('Please Wait {} Seconds.  System is Warming Up...'.format(self._data['warmup']))
                    # self.__lblwarmcoolclock.SetText(str(qualifier))
                    self.__popups_me('popup_busy')
                #ignore second one if there is one active

            elif value == 'cooldown':
                if self.__popup_busy_display == command or  self.__popup_busy_display == 'stop':
                    self.__popup_busy_display = command
                    self.__lblwarmcoolmess.SetText('Please Wait {} seconds.  System is Cooling Down...'.format(self._data['cooldown']))
                    # self.__lblwarmcoolclock.SetText(str(qualifier))
                    self.__popups_me('popup_busy')

            else:
                self.__popups_me('popup_close')
                self.__lblwarmcoolmess.SetText('')
                self.__lblwarmcoolclock.SetText('')
                @Wait(5)    
                def _waitbeforenextcommand():   
                    self.__popup_busy_display = 'stop'



    def __flip2_splash(self):
        self.__hide_all_subpages()
        self.__show_page('splash')
        #fix for slow poly
        self.__uipoly.update_sharesfb(0)



    def __flip2_main(self):
        self.__show_page('main')

        self.__lblroom.SetText(self.__room.name)
        self.__lblpoweroff.SetText(self.__room.name + ' Off?')



    def __menu_select(self, sub):
        self.print_me('__menu_select subpage:{}'.format(sub))

        if sub in self.__maincentersubs.values():
            ky = list(self.__maincentersubs.keys())[list(self.__maincentersubs.values()).index(sub)]
            self.__msetbtnmaincentersubs.SetCurrent(self.__btnmaincentersubs[ky])
            # self.__room.menu_change_sync(ky)


        # self.__switcher.video_mute_discrete(1, False)
        self.__uicam.currsubpage = sub
        self.__uibiamp.currsubpage = sub



        if sub == 'main_center_atc':
            self.__show_subpage('main_center_atc')
            self.__show_subpage('main_up_atc')
            # self.__biamp.mute_descrete2('RM1_VTC_RX', 'On')


        # elif sub == 'main_center_present_cable':
        #     self.__show_subpage('main_center_present_cable')
        #     self.__show_subpage('main_up_present')
        #     self.__uiswitcher.select_input(4)
        #     self.__uidisplay.forcehdmi()


        elif sub == 'main_center_present_laptop':
            self.__show_subpage('main_center_present_laptop')
            self.__show_subpage('main_up_present')
            # self.__uiswitcher.select_input(0)
            self.__uidisplay.forcehdmi()


        # elif sub == 'main_center_present_vtc':
        #     self.__show_subpage('main_center_present_vtc')
        #     self.__show_subpage('main_up_present')


        elif sub == 'main_center_vtclaptop':
            self.__show_subpage('main_center_vtclaptop')
            self.__show_subpage('main_up_vtclaptop')
            self.__onebeyond.power_me(True)
            self.__uidisplay.forcehdmi()


        elif sub == 'main_center_vtclaptop_take':
            self.__show_subpage('main_center_vtclaptop')
            self.__show_subpage('main_up_vtclaptop')
            self.__switcher.switch_me(3,1)


        elif sub == 'main_center_vtc_cam':
            self.__show_subpage('main_center_vtc_cam')
            self.__show_subpage('main_up_vtc')


        elif sub == 'main_center_vtc_dial':
            self.__show_subpage('main_center_vtc_dial')
            self.__show_subpage('main_up_vtc')


        elif sub == 'main_center_vtc_keyboard':
            self.__show_subpage('main_center_vtc_keyboard')
            self.__show_subpage('main_up_vtc')


        elif sub == 'main_center_vtc_menu':
            self.__show_subpage('main_center_vtc_menu')
            self.__show_subpage('main_up_vtc')
            self.__switcher.switch_me(3,1)
            self.__uiswitcher.select_input(3)
            self.__onebeyond.power_me(True)
            self.__uidisplay.forcehdmi()




        elif sub == 'main_center_vtc_source':
            self.__show_subpage('main_center_vtc_source')
            self.__show_subpage('main_up_vtc')


        elif sub.startswith('main_center_room'):
            self.__show_subpage(sub)
            self.__show_subpage('main_up_room')












   

                



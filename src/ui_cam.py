# "author": "ted.cygan"

from extronlib import event
# from extronlib.ui import Button, Label, Level
from drivers.MirrorUI import Button
from extronlib.system import MESet, Timer, Wait
from abstracts import AbstractUiClass


class UiCamClass(AbstractUiClass):   
    def __init__(self, alias, tp, data, cams, switcher): 
        AbstractUiClass.__init__(self, alias, tp, data)

        self.__cam = None
        self.__cams = cams
        self.__switcher = switcher
        # self.__switcher.subscribe(self.__switcher_event_cb)

        self.currsubpage = ''


        self.__camselects = {
            301:data['cam1name'],
            302:data['cam2name'],
            303:data['cam3name'],
            304:data['cam4name'],
            305:data['cam5name'],
            306:data['cam6name'],
            307:data['cam7name'],
            308:data['cam8name'],
        }

        
        self.__pantilts = {
            331:'Up',
            332:'Down',
            333:'Left',
            334:'Right'
        }


        self.__zooms = {
            336:'Tele',
            337:'Wide',
        }


        self.__presets = {
            311:'Left View',
            312:'Center View',
            313:'Center Wide View',
            314:'Right View',
        }


        self.__modes = {
            321:'Boardroom Mode',
            322:'Presentation Left (West)',
            323:'Presentation Right (East)',
            324:'Split Mode'
        }


        self.__autoswitch = False
        self.__btnautoswitch = Button(tp, 320)
        self.__btnptzimpage = Button(tp, 330)



        self.__btnpantilts = {}
        self.__btnzooms = {}
        self.__btnpresets= {}
        self.__btncamselects = {}
        self.__btnmodes = {}


        self.__offlines = {
            341:'',
            342:'',
            343:'',
            344:'',
            345:'',
            346:'',
            347:'',
            348:'',
        }
        self.__btnofflines = {}
        for ky in self.__offlines:  
            self.__btnofflines[ky]=Button(tp, ky)


        for ky in self.__camselects:
            self.__btncamselects[ky]=Button(tp, ky)
            self.__btncamselects[ky].SetText(self.__camselects[ky])


        for ky in self.__pantilts:
            self.__btnpantilts[ky]=Button(tp, ky)


        for ky in self.__zooms:
            self.__btnzooms[ky]=Button(tp, ky)


        for ky in self.__presets:
            self.__btnpresets[ky]=Button(tp, ky, holdTime=4)
            self.__btnpresets[ky].SetText(self.__presets[ky])


        for ky in self.__modes:
            self.__btnmodes[ky]=Button(tp, ky)
            self.__btnmodes[ky].SetText(self.__modes[ky])
        self.__msetbtnmodes = MESet(list(self.__btnmodes.values()))



                

        self.__btnautofocus = Button(tp, 338)
        # self.__btnoffline = Button(tp, 349)
        # self.__btnpresetsave = Button(tp, 309)
        self.__btnpresetsaving = Button(tp, 310)
        self.__btnpresetsaving.SetVisible(False)
        self.__msetbtncamselects = MESet(list(self.__btncamselects.values()))

        self.__lastpreset = 1


        @event(self.__btnautoswitch, ['Pressed', 'Released'])
        def __btnautotrackingpress(button, state):
            if state == 'Pressed':
                self.__autoswitch_me()



        @event(self.__msetbtncamselects.Objects, ['Pressed', 'Released'])
        def __msetbtncamspress(button, state):
            if state == 'Pressed':
                # self.__msetbtncamselects.SetCurrent(button)
                self.__cam_select(cams[button.ID-300], button.MirroredParent)


        @event(list(self.__btnpresets.values()), 'Tapped')
        def __btnpresetstapped(button, state):
            button.SetState(1)
            self.__cam.preset(button.ID-310, False)
            self.__lastpreset = button.ID-310
            button.SetState(0)

            
        @event(list(self.__btnpresets.values()), 'Released')
        def __btnpresetsreleased(button, state):
            button.SetState(0)
         

        @event(list(self.__btnpresets.values()), 'Held')
        def __btnpresetsheld(button, state):
            button.SetState(1)
            self.__cam.preset(button.ID-310, True)
            self.__btnpresetsaving.SetVisible(True)
            self.__lastpreset = button.ID-310

            @Wait(2)
            def Wait1Sec():
                self.__btnpresetsaving.SetVisible(False)
                button.SetState(0)


        # @event(self.__btnpresetsave, ['Pressed', 'Released'])
        # def __btnpresetsavepress(button, state):
        #     if state == 'Pressed':
        #         button.SetState(1)
        #         self.__cam.preset(self.__lastpreset, True)
        #         self.__btnpresetsaving.SetVisible(True)
        #         @Wait(2)
        #         def Wait1Sec():
        #             self.__btnpresetsaving.SetVisible(False)
        #             button.SetState(0)

                

        @event(self.__btnautofocus, ['Pressed', 'Released'])
        def __btnautofocuspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__cam.auto_focus()
            else:
                button.SetState(0)


        @event(list(self.__btnpantilts.values()), ['Pressed', 'Released'])
        def __btnpantiltspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__cam.pantilt(self.__pantilts[button.ID])
            else:
                self.__cam.pantilt('Stop')
                button.SetState(0)


        @event(list(self.__btnzooms.values()), ['Pressed', 'Released'])
        def __btnzoomspress(button, state):
            if state == 'Pressed':
                button.SetState(1)
                self.__cam.zoom(self.__zooms[button.ID])
            else:
                self.__cam.zoom('Stop')
                button.SetState(0)


        @event(self.__msetbtnmodes.Objects, ['Pressed', 'Released'])
        def __msetbtnmodespress(button, state):
            if state == 'Pressed':
                self.__msetbtnmodes.SetCurrent(button.MirroredParent)
                self.__cam.onebeyond_mode_me(button.ID-320)


        self.__cam_select(cams[1], self.__btncamselects[301])
        self.__autoswitch_me()

    # END CONSTRUCTOR


    def __autoswitch_me(self):
        self.__autoswitch = not self.__autoswitch

        if self.__autoswitch:
            self.__btnautoswitch.SetState(1)
            self.__cam.onebeyond_autoswitch_me('On')
        else:
            self.__btnautoswitch.SetState(0)
            self.__cam.onebeyond_autoswitch_me('Off')


        self.__btnptzimpage.SetVisible(self.__autoswitch)


        for ky in self.__camselects:
            self.__btncamselects[ky].SetEnable(not self.__autoswitch)

        for ky in self.__pantilts:
            self.__btnpantilts[ky].SetEnable(not self.__autoswitch)

        for ky in self.__zooms:
            self.__btnzooms[ky].SetEnable(not self.__autoswitch)

        for ky in self.__presets:
            self.__btnpresets[ky].SetEnable(not self.__autoswitch)

        for ky in self.__modes:
            self.__btnmodes[ky].SetVisible(self.__autoswitch)



    def __driver_event_cb(self, command, value, qualifier):
        self.print_me('c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command == 'ConnectionStatus':
            if value == 'Connected':  
                self.__btnofflines[int(self.__cam.alias[-1])+340].SetVisible(False)
            else:
                self.__btnofflines[int(self.__cam.alias[-1])+340].SetVisible(True)
        elif command == 'FocusMode':
            if value == 'Auto':  
                self.__btnautofocus.SetState(True)
            else:
                self.__btnautofocus.SetState(False)
        elif command == 'Power':
            pass


    def __cam_select(self, cam, button):
        self.print_me('__cam_select cam:{}, curr subpage:{}'.format(cam.alias, self.currsubpage))

        if cam != self.__cam:
            if self.__cam is not None:
                self.__cam.unsubscribe(self.__driver_event_cb)

            self.__cam = cam
            self.__cam.cam_source(2)

            #     if self.currsubpage=='main_center_vtclaptop':
            #         self.__switcher.switch_me(4, 5)
            #     else:
            #         self.__switcher.switch_me(4, 7)
            # else:
            #     btn=self.__btncamselects[302]
            #     if self.currsubpage=='main_center_vtclaptop':
            #         self.__switcher.switch_me(5, 5)
            #     else:
            #         self.__switcher.switch_me(5, 7)

            
            self.__msetbtncamselects.SetCurrent(button)

            self.__cam.subscribe(self.__driver_event_cb)
            self.__btnofflines[int(self.__cam.alias[-1])+340].SetVisible(not self.__cam.online)

            self.__cam.onebeyond_switch_cam(self.__cam.alias[-1])







 
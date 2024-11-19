# "author": "ted.cygan"

# import sys
# sys.dont_write_bytecode = True
from extronlib import event, Version
from extronlib.device import ProcessorDevice, UIDevice, SPDevice
from extronlib.system import Clock
from main_data import data, todo
from drivers.MirrorUI import MirrorUIDevice, ModuleVersion
from abstracts import *


print('<< PROGRAM_LOAD_START >>  Ver:' + Version() + ', Module Ver:' + ModuleVersion())  
print(*todo, sep='\n--')


processor = ProcessorDevice('IPCPPro550xi')

tp1a = UIDevice('TLPPro1025T')
tp1 = MirrorUIDevice([tp1a])


# 000 pages subpages


# 200
import dv_cable
cable = dv_cable.ContemporaryReClass('cable', data, processor)



# 350 - 399
import dv_display
display1 = dv_display.SamsungQm75QClass('display1', data) 

import dv_display
display2 = dv_display.SamsungQm75QClass('display2', data) 

import dv_display
display3 = dv_display.SamsungQm75QClass('display3', data) 

import dv_display
display4 = dv_display.SamsungQm75QClass('display4', data) 

displays = {
    1:display1,
    2:display2,
    3:display3,
    4:display4,
}



# 600 - 799,  600 levels, 650 atc, 700 mics
import dv_biamp
import dv_biamp_data
biamp = dv_biamp.BiampClass('biamp', data, dv_biamp_data.data, processor)


# 400 - 599
import dv_switcher
switcher = dv_switcher.SwitcherClass('switcher', data)


# 800
import dv_lights
lights = dv_lights.LutronQseCiNwkClass('lights', data, processor)


# 1100
import dv_poly
poly = dv_poly.PolyG7500Class('poly', data, processor, switcher, biamp)


import dv_onebeyond
onebeyond = dv_onebeyond.OnebeyondClass('onebeyond', data)


# 300 - 349
import dv_cam
cam1 = dv_cam.CamClass('cam1', data, onebeyond, poly)
cam2 = dv_cam.CamClass('cam2', data, onebeyond, poly)
cam3 = dv_cam.CamClass('cam3', data, onebeyond, poly)
cam4 = dv_cam.CamClass('cam4', data, onebeyond, poly)
cam5 = dv_cam.CamClass('cam5', data, onebeyond, poly)
cam6 = dv_cam.CamClass('cam6', data, onebeyond, poly)
cam7 = dv_cam.CamClass('cam7', data, onebeyond, poly)
cam8 = dv_cam.CamClass('cam8', data, onebeyond, poly)


cams = {
    1:cam1,
    2:cam2,
    3:cam3,
    4:cam4,
    5:cam5,
    6:cam6,
    7:cam7,
    8:cam8,
}



# 100
import dv_
room = dv_.RoomClass('room', data, switcher, biamp, cams, displays, poly, onebeyond)


import ui_
tp1pages = ui_.UiCreateClass('tp1', tp1, data, switcher, biamp, cams, cable, displays, room, poly, lights, onebeyond)


def __clock_room_off_cb():
    # tp1pages.ui.flip2_splash()
    # taprm.room_off
    # tbd
    pass


nightly_shutdown = Clock([data['nightlyshutdown']], None, __clock_room_off_cb)
if data['enable_nightlyshutdown']:
    nightly_shutdown.Enable()


print('<< PROGRAM_LOAD_END >>\n')
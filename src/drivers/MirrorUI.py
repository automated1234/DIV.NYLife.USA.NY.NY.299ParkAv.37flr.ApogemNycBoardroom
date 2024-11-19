from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.system import ProgramLog
from extronlib.ui import Button as OldButton
from extronlib.ui import Knob as OldKnob
from extronlib.ui import Label as OldLabel
from extronlib.ui import Level as OldLevel
from extronlib.ui import Slider as OldSlider

__version__ = '1.2.1'

def ModuleVersion():
    """ This method returns the version of the Mirror UI Module
    """
    return __version__

class MirrorUIDevice():
    """ This class creates an object that contains a list of UIDevice objects
        to be used with the Button, Label, Level and Knob classes defined in
        this file.  The class object is also used in place of the UIDevice
        object for touchpanel operations such as page flips and show/hide
        popup pages.
    """
    def __init__(self, UIList):
        if isinstance(UIList, list):
            self.Objects = UIList
            for obj in self.Objects:
                obj.BrightnessChanged = self.CallBrightnessChanged
                obj.HDCPStatusChanged = self.CallHDCPStatusChanged
                obj.InactivityChanged = self.CallInactivityChanged
                obj.InputPresenceChanged = self.CallInputPresenceChanged
                obj.LidChanged = self.CallLidChanged
                obj.LightChanged = self.CallLightChanged
                obj.MotionDetected = self.CallMotionDetected
                obj.SleepChanged = self.CallSleepChanged
                obj.MirroredParent = self

            self.BrightnessChanged = self.__unassigned
            self.HDCPStatusChanged = self.__unassigned
            self.InactivityChanged = self.__unassigned
            self.InputPresenceChanged = self.__unassigned
            self.LidChanged = self.__unassigned
            self.LightChanged = self.__unassigned
            self.MotionDetected = self.__unassigned
            self.SleepChanged = self.__unassigned
        else:
            ProgramLog('Parameter UIList is not a list', 'error')

    # Methods:
    # The methods defined here operate the same as the UIDevice methods except
    # that the parameters are passed to all of the objects defined in the
    # UIList passed to the MirrorUIDevice object.

    def Click(self, count=1, interval=None):
        """ Plays the default buzzer sound on all mirrored devices.
        """
        for obj in self.Objects:
            obj.Click(count, interval)

    def GetHDCPStatus(self, videoInput):
        """ Returns a list of the current HDCP Status for the given input on
            all devices.
        """
        return [obj.GetHDCPStatus(videoInput) for obj in self.Objects]

    def GetInputPresence(self, videoInput):
        """ Returns a list of the current Input Presence for the given input
            on all devices.
        """
        return [obj.GetInputPresence(videoInput) for obj in self.Objects]

    def GetMute(self, name):
        """ Returns  a list of the current mute state for the given channel
            name on all devices.
        """
        return [obj.GetMute(name) for obj in self.Objects]

    def GetVolume(self, name):
        """ Returns a list of the current volume level for the given channel
            name on all devices.
        """
        return [obj.GetVolume(name) for obj in self.Objects]

    def HideAllPopups(self):
        """ Dismisses all popup pages on all devices.
        """
        for obj in self.Objects:
            obj.HideAllPopups()

    def HidePopup(self, popup):
        """ Hide popup page on all devices.
        """
        for obj in self.Objects:
            obj.HidePopup(popup)

    def HidePopupGroup(self, group):
        """ Hide all popup pages in a popup group on all devices.
        """
        for obj in self.Objects:
            obj.HidePopupGroup(group)

    def PlaySound(self, filename):
        """ Play a sound file identified by filename on all devices.
        """
        for obj in self.Objects:
            obj.PlaySound(filename)

    def SetAutoBrightness(self, state):
        """ Set the auto brightness state on all devices.
        """
        for obj in self.Objects:
            obj.SetAutoBrightness(state)

    def SetBrightness(self, level):
        """ Set the LCD screen brightness level on all devices.
        """
        for obj in self.Objects:
            obj.SetBrightness(level)

    def SetDisplayTimer(self, state, timeout):
        """ Enables or Disables the display timer on all devices.
        """
        for obj in self.Objects:
            obj.SetDisplayTimer(state, timeout)

    def SetInactivityTime(self, times):
        """ Set the inactivity times when the InactivityChanged event will
            trigger for all devices.
        """
        for obj in self.Objects:
            obj.SetInactivityTime(times)

    def SetInput(self, videoInput):
        """ Set the video input on all devices.
        """
        for obj in self.Objects:
            obj.SetInput(videoInput)

    def SetLEDBlinking(self, ledID, rate, stateList):
        """ Set the LED cycle at ADA comliant rates through a list of states
            on all devices.
        """
        for obj in self.Objects:
            obj.SetLEDBlinking(ledID, rate, stateList)

    def SetLEDState(self, ledID, state):
        """ Make the LED to a given color on all devices.
        """
        for obj in self.Objects:
            obj.SetLEDState(ledID, state)

    def SetMotionDecayTime(self, duration):
        """ Set the period of time for the MotionDetected event to trigger for
            all devices.
        """
        for obj in self.Objects:
            obj.SetMotionDecayTime(duration)

    def SetMute(self, name, mute):
        """ Sets the mute state for the given channel on all devices.
        """
        for obj in self.Objects:
            obj.SetMute(name, mute)

    def SetSleepTimer(self, state, duration=None):
        """ Enables or Disables the sleep timer on all devices.
        """
        for obj in self.Objects:
            obj.SetSleepTimer(state, duration)

    def SetVolume(self, name, level):
        """ Sets the volume level for the given channel name on all devices.
        """
        for obj in self.Objects:
            obj.SetVolume(name, level)

    def SetWakeOnMotion(self, state):
        """ Enables or disables wake on motion on all devices.
        """
        for obj in self.Objects:
            obj.SetWakeOnMotion(state)

    def ShowPage(self, page):
        """ Show page on the screen on all devices.
        """
        for obj in self.Objects:
            obj.ShowPage(page)

    def ShowPopup(self, page, duration=0):
        """ Display pop-up page on all devices for a period of time
        """
        for obj in self.Objects:
            obj.ShowPopup(page, duration)

    def Sleep(self):
        """ Forces all devices to sleep immediately
        """
        for obj in self.Objects:
            obj.Sleep()

    def StopSound(self):
        """ Stop playing sound file on all devices
        """
        for obj in self.Objects:
            obj.StopSound()

    def Wake(self):
        """ Forces all devices to wake up immediately
        """
        for obj in self.Objects:
            obj.Wake()

    def CallBrightnessChanged(self, panel, brightness):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__BrightnessChanged(panel, brightness)

    def CallHDCPStatusChanged(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__HDCPStatusChanged(panel, state)

    def CallInactivityChanged(self, panel, time):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__InactivityChanged(panel, time)

    def CallInputPresenceChanged(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__InputPresenceChanged(panel, state)

    def CallLidChanged(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__LidChanged(panel, state)

    def CallLightChanged(self, panel, level):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__LightChanged(panel, level)

    def CallMotionDetected(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__MotionDetected(panel, state)

    def CallSleepChanged(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__InactivityChanged(panel, state)

    # Class Property Callbacks
    ##########################

    @property
    def AmbientLightValue(self):
        """ Defined Property to pass list of Objects' AmbientLightValue
            property
        """
        return [obj.AmbientLightValue for obj in self.Objects]

    @property
    def AutoBrightness(self):
        """ Defined Property to pass list of Objects' AutoBrightness property
        """
        return [obj.AutoBrightness for obj in self.Objects]

    @property
    def Brightness(self):
        """ Defined Property to pass list of Objects' Brightness property
        """
        return [obj.Brightness for obj in self.Objects]

    @property
    def DeviceAlias(self):
        """ Defined Property to pass a list of Objects' DeviceAlias property
        """
        return [obj.DeviceAlias for obj in self.Objects]

    @property
    def DisplayState(self):
        """ Defined Property to pass a list of Objects' Display State property
        """
        return [obj.DisplayState for obj in self.Objects]

    @property
    def DisplayTimer(self):
        """ Defined Property to pass a list of Objects' DisplayTimer property
        """
        return [obj.DisplayTimer for obj in self.Objects]

    @property
    def DisplayTimerEnabled(self):
        """ Defined Property to pass a list of Objects' DisplayTimerEnabled
            property
        """
        return [obj.DisplayTimerEnabled for obj in self.Objects]

    @property
    def FirmwareVersion(self):
        """ Defined Property to pass a list of Objects' FirmwareVersion
            property
        """
        return [obj.FirmwareVersion for obj in self.Objects]

    @property
    def Hostname(self):
        """ Defined Property to pass list of Objects' Hostname property
        """
        return [obj.Hostname for obj in self.Objects]

    @property
    def IPAddress(self):
        """ Defined Property to pass a list of Objects' IPAddress property
        """
        return [obj.IPAddress for obj in self.Objects]

    @property
    def InactivityTime(self):
        """ Defined Property to pass a list of Objects' InactivityTime
            property
        """
        return [obj.InactivityTime for obj in self.Objects]

    @property
    def LidState(self):
        """ Defined Property to pass a list of Objects' LidState property
        """
        return [obj.LidState for obj in self.Objects]

    @property
    def LightDetectedState(self):
        """ Defined Property to pass a list of Objects' LightDetectedState
            property
        """
        return [obj.LightDetectedState for obj in self.Objects]

    @property
    def MACAddress(self):
        """ Defined Property to pass a list of Objects' MACAddress property
        """
        return [obj.MACAddress for obj in self.Objects]

    @property
    def ModelName(self):
        """ Defined Property to pass a list of Objects' ModelName property
        """
        return [obj.ModelName for obj in self.Objects]

    @property
    def MotionDecayTime(self):
        """ Defined Property to pass a list of Objects' MotionDecayTime
            property
        """
        return [obj.MotionDecayTime for obj in self.Objects]

    @property
    def MotionState(self):
        """ Defined Property to pass a list of Objects' MotionState property
        """
        return [obj.MotionState for obj in self.Objects]

    @property
    def PartNumber(self):
        """ Defined Property to pass a list of Objects' PartNumber property
        """
        return [obj.PartNumber for obj in self.Objects]

    @property
    def SerialNumber(self):
        """ Defined Property to pass a list of Objects' SerialNumber property
        """
        return [obj.SerialNumber for obj in self.Objects]

    @property
    def SleepState(self):
        """ Defined Property to pass a list of Objects' SleepState property
        """
        return [obj.SleepState for obj in self.Objects]

    @property
    def SleepTimer(self):
        """ Defined Property to pass a list of Objects' SleepTimer property
        """
        return [obj.SleepTimer for obj in self.Objects]

    @property
    def SleepTimerEnabled(self):
        """ Defined Property to pass a list of Objects' SleepTimerEnabled
            property
        """
        return [obj.SleepTimerEnabled for obj in self.Objects]

    @property
    def UserUsage(self):
        """ Defined Property to pass a list of Objects' UserUsage property
        """
        return [obj.UserUsage for obj in self.Objects]

    @property
    def WakeOnMotion(self):
        """ Defined Property to pass a list of Objects' WakeOnMotion property
        """
        return [obj.WakeOnMotion for obj in self.Objects]

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """ If Module Events are not defined in user code, then do nothing.
        """
        pass

    @property
    def BrightnessChanged(self):
        """ Passback the BrightnessChanged Event
        """
        return self.__BrightnessChanged

    @BrightnessChanged.setter
    def BrightnessChanged(self, handler):
        if callable(handler):
            self.__BrightnessChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def HDCPStatusChanged(self):
        """ Passback the HDCPStatusChanged Event
        """
        return self.__HDCPStatusChanged

    @HDCPStatusChanged.setter
    def HDCPStatusChanged(self, handler):
        if callable(handler):
            self.__HDCPStatusChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def InactivityChanged(self):
        """ Passback the InactivityChanged Event
        """
        return self.__InactivityChanged

    @InactivityChanged.setter
    def InactivityChanged(self, handler):
        if callable(handler):
            self.__InactivityChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def InputPresenceChanged(self):
        """ Passback the InputPresenceChanged Event
        """
        return self.__InputPresenceChanged

    @InputPresenceChanged.setter
    def InputPresenceChanged(self, handler):
        if callable(handler):
            self.__InputPresenceChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def LidChanged(self):
        """ Passback the LidChanged Event
        """
        return self.__LidChanged

    @LidChanged.setter
    def LidChanged(self, handler):
        if callable(handler):
            self.__LidChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def LightChanged(self):
        """ Passback the LightChanged Event
        """
        return self.__LightChanged

    @LightChanged.setter
    def LightChanged(self, handler):
        if callable(handler):
            self.__LightChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def MotionDetected(self):
        """ Passback the MotionDetected Event
        """
        return self.__MotionDetected

    @MotionDetected.setter
    def MotionDetected(self, handler):
        if callable(handler):
            self.__MotionDetected = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def SleepChanged(self):
        """ Passback the SleepChanged Event
        """
        return self.__SleepChanged

    @SleepChanged.setter
    def SleepChanged(self, handler):
        if callable(handler):
            self.__SleepChanged = handler
        else:
            raise ValueError('handler must be a function')


class MirroreBUSDevice():
    """ This class creates an object that contains a list of eBUSDevice
        objects to be used with the Button, Label, Level and Knob classes
        defined in this file.  The class object is also used in place of the
        eBUSDevice object for eBUS panel operations such as timer settings and
        mutes.
    """
    def __init__(self, eBUSList):
        if isinstance(eBUSList, list):
            self.Objects = eBUSList
            for obj in self.Objects:
                obj.InactivityChanged = self.CallInactivityChanged
                obj.LidChanged = self.CallLidChanged
                obj.SleepChanged = self.CallSleepChanged
                obj.MirroredParent = self

            self.InactivityChanged = self.__unassigned
            self.LidChanged = self.__unassigned
            self.SleepChanged = self.__unassigned
        else:
            ProgramLog('Parameter eBUSList is not a list', 'error')

    # Methods:
    # The methods defined here operate the same as the eBUSDevice methods
    # except that the parameters are passed to all of the objects defined in
    # the eBUSList passed to the MirroreBUSDevice object.

    def Click(self, count=1, interval=None):
        """ Play default buzzer sound on all devices
        """
        for obj in self.Objects:
            obj.Click(count, interval)

    def GetMute(self, name):
        """ Returns  a list of the current mute state for the given channel
            name on all devices.
        """
        return [obj.GetMute(name) for obj in self.Objects]

    def SetInactivityTime(self, times):
        """ Set the inactivity times when the InactivityChanged event will
            trigger for all devices.
        """
        for obj in self.Objects:
            obj.SetInactivityTime(times)

    def SetMute(self, name, mute):
        """ Returns a list of the mute state for the given channel name on
            all devices.
        """
        for obj in self.Objects:
            obj.SetMute(name, mute)

    def SetSleepTimer(self, state, time=None):
        """ Enables or Disables the sleep timer on all devices.
        """
        for obj in self.Objects:
            obj.SetSleepTimer(state, time)

    def Sleep(self):
        """ Forces all devices to sleep immediately
        """
        for obj in self.Objects:
            obj.Sleep()

    def Wake(self):
        """ Forces all devices to wake up immediately
        """
        for obj in self.Objects:
            obj.Wake()

    def CallInactivityChanged(self, panel, time):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__InactivityChanged(panel, time)

    def CallLidChanged(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__LidChanged(panel, state)

    def CallSleepChanged(self, panel, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__InactivityChanged(panel, state)

    # Class Property Callbacks
    ##########################

    @property
    def DeviceAlias(self):
        """ Defined Property to pass a list of Objects' DeviceAlias property
        """
        return [obj.DeviceAlias for obj in self.Objects]

    @property
    def Host(self):
        """ Defined Property to pass a list of Objects' Host property
        """
        return [obj.Host for obj in self.Objects]

    @property
    def ID(self):
        """ Defined Property to pass a list of Objects' ID property
        """
        return [obj.ID for obj in self.Objects]

    @property
    def InactivityTime(self):
        """ Defined Property to pass a list of Objects' InactivityTime
            property
        """
        return [obj.InactivityTime for obj in self.Objects]

    @property
    def LidState(self):
        """ Defined Property to pass value of Objects[0]'s LidState property
        """
        return [obj.LidState for obj in self.Objects]

    @property
    def ModelName(self):
        """ Defined Property to pass a list of Objects' ModelName property
        """
        return [obj.ModelName for obj in self.Objects]

    @property
    def PartNumber(self):
        """ Defined Property to pass a list of Objects' PartNumber property
        """
        return [obj.PartNumber for obj in self.Objects]

    @property
    def SleepState(self):
        """ Defined Property to pass a list of Objects' SleepState property
        """
        return [obj.SleepState for obj in self.Objects]

    @property
    def SleepTimer(self):
        """ Defined Property to pass a list of Objects' SleepTimer property
        """
        return [obj.SleepTimer for obj in self.Objects]

    @property
    def SleepTimerEnabled(self):
        """ Defined Property to pass a list of Objects' SleepTimerEnabled
            property
        """
        return [obj.SleepTimerEnabled for obj in self.Objects]

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """ If Module Events are not defined in user code, then do nothing.
        """
        pass

    @property
    def InactivityChanged(self):
        """ Passback the InactivityChanged Event
        """
        return self.__InactivityChanged

    @InactivityChanged.setter
    def InactivityChanged(self, handler):
        if callable(handler):
            self.__InactivityChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def LidChanged(self):
        """ Passback the LidChanged Event
        """
        return self.__LidChanged

    @LidChanged.setter
    def LidChanged(self, handler):
        if callable(handler):
            self.__LidChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def SleepChanged(self):
        """ Passback the SleepChanged Event
        """
        return self.__SleepChanged

    @SleepChanged.setter
    def SleepChanged(self, handler):
        if callable(handler):
            self.__SleepChanged = handler
        else:
            raise ValueError('handler must be a function')


class Button():
    """ This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties,
        methods and events for all Button Objects created within this class.
    """
    def __init__(self, UIHost, ID, holdTime=None, repeatTime=None):
        self.Objects = []
        if isinstance(UIHost, (MirroreBUSDevice, MirrorUIDevice)):
            self.Objects = [OldButton(obj, ID, holdTime, repeatTime) for obj in UIHost.Objects]
        elif isinstance(UIHost, (eBUSDevice, UIDevice)):
            self.Objects = [OldButton(UIHost, ID, holdTime, repeatTime)]

        for obj in self.Objects:
            obj.Pressed = self.CallPressed
            obj.Released = self.CallReleased
            obj.Tapped = self.CallTapped
            obj.Held = self.CallHeld
            obj.Repeated = self.CallRepeated
            obj.MirroredParent = self

        self.Pressed = self.__unassigned
        self.Released = self.__unassigned
        self.Tapped = self.__unassigned
        self.Held = self.__unassigned
        self.Repeated = self.__unassigned

    # Methods:
    # The methods defined here operate the same as the Button methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def CustomBlink(self, rate, stateList):
        """ Makes the buttons on all devices cycle through each of the
            states provided.
        """
        for obj in self.Objects:
            obj.CustomBlink(rate, stateList)

    def SetBlinking(self, rate, stateList):
        """ Makes the buttons on all devices cycle, at ADA compliant rates,
            through each of the states provided.
        """
        for obj in self.Objects:
            obj.SetBlinking(rate, stateList)

    def SetEnable(self, enable):
        """ Enable or disable a UI control object on all devices
        """
        for obj in self.Objects:
            obj.SetEnable(enable)

    def SetState(self, state):
        """ Set the current visual state on all devices
        """
        for obj in self.Objects:
            obj.SetState(state)

    def SetText(self, text):
        """ Specify text to display on the UIObject on all devices
        """
        for obj in self.Objects:
            obj.SetText(text)

    def SetVisible(self, visible):
        """ Change the visibility of a UI control object on all devices
        """
        for obj in self.Objects:
            obj.SetVisible(visible)

    def CallPressed(self, button, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Pressed(button, state)

    def CallReleased(self, button, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Released(button, state)

    def CallTapped(self, button, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Tapped(button, state)

    def CallHeld(self, button, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Held(button, state)

    def CallRepeated(self, button, state):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Repeated(button, state)

    # Class Property Callbacks
    ##########################

    @property
    def BlinkState(self):
        """ Defined Property to pass a list of Objects' BlinkState property
        """
        return [obj.BlinkState for obj in self.Objects]

    @property
    def Enabled(self):
        """ Defined Property to pass a list of Objects' Enabled property
        """
        return [obj.Enabled for obj in self.Objects]

    @property
    def Host(self):
        """ Defined Property to pass a list of Objects' Host property
        """
        return [obj.Host for obj in self.Objects]

    @property
    def ID(self):
        """ Defined Property to pass a list of Objects' ID property
        """
        return [obj.ID for obj in self.Objects]

    @property
    def Name(self):
        """ Defined Property to pass a list of Objects' Name property
        """
        return [obj.Name for obj in self.Objects]

    @property
    def PressedState(self):
        """ Defined Property to pass a list of Objects'PressedState property
        """
        return [obj.PressedState for obj in self.Objects]

    @property
    def State(self):
        """ Defined Property to pass a list of Objects' State property
        """
        return [obj.State for obj in self.Objects]

    @property
    def Visible(self):
        """ Defined Property to pass a list of Objects' Visible property
        """
        return [obj.Visible for obj in self.Objects]

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """ If Module Events are not defined in user code, then do nothing.
        """
        pass

    @property
    def Pressed(self):
        """ Passback the Pressed Event
        """
        return self.__Pressed

    @Pressed.setter
    def Pressed(self, handler):
        if callable(handler):
            self.__Pressed = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Released(self):
        """ Passback the Released Event
        """
        return self.__Released

    @Released.setter
    def Released(self, handler):
        if callable(handler):
            self.__Released = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Tapped(self):
        """ Passback the Tapped Event
        """
        return self.__Tapped

    @Tapped.setter
    def Tapped(self, handler):
        if callable(handler):
            self.__Tapped = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Held(self):
        """ Passback the Held Event
        """
        return self.__Held

    @Held.setter
    def Held(self, handler):
        if callable(handler):
            self.__Held = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Repeated(self):
        """ Passback the Repeated Event
        """
        return self.__Repeated

    @Repeated.setter
    def Repeated(self, handler):
        if callable(handler):
            self.__Repeated = handler
        else:
            raise ValueError('handler must be a function')


class Knob():
    """ This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties,
        methods and events for all Knob Objects created within this class.
    """

    def __init__(self, UIHost, ID, holdTime=None, repeatTime=None):
        self.Objects = []
        if isinstance(UIHost, (MirroreBUSDevice, MirrorUIDevice)):
            self.Objects = [OldKnob(obj, ID) for obj in UIHost.Objects]
        elif isinstance(UIHost, (eBUSDevice, UIDevice)):
            self.Objects = [OldKnob(UIHost, ID)]

        for obj in self.Objects:
            obj.Turned = self.CallTurned
            obj.MirroredParent = self

        self.Turned = self.__unassigned

    # Methods:
    # The methods defined here operate the same as the Knob methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def CallTurned(self, knob, direction):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Turned(knob, direction)

    # Class Property Callbacks
    ##########################

    @property
    def Host(self):
        """ Defined Property to pass a list of Objects' Host property
        """
        return [obj.Host for obj in self.Objects]

    @property
    def ID(self):
        """ Defined Property to pass a list of Objects' ID property
        """
        return [obj.ID for obj in self.Objects]

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """ If Module Events are not defined in user code, then do nothing.
        """
        pass

    @property
    def Turned(self):
        """ Passback the Turned Event
        """
        return self.__Turned

    @Turned.setter
    def Turned(self, handler):
        if callable(handler):
            self.__Turned = handler
        else:
            raise ValueError('handler must be a function')


class Label():
    """ This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties
        and methods for all Label Objects created within this class.
    """

    def __init__(self, UIHost, ID):
        self.Objects = []
        if isinstance(UIHost, MirrorUIDevice):
            self.Objects = [OldLabel(obj, ID) for obj in UIHost.Objects]
        elif isinstance(UIHost, UIDevice):
            self.Objects = [OldLabel(UIHost, ID)]

        for obj in self.Objects:
            obj.MirroredParent = self

    # Methods:
    # The methods defined here operate the same as the Label methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def SetText(self, text):
        """ Specify text to display on the UIObject on all devices
        """
        for obj in self.Objects:
            obj.SetText(text)

    def SetVisible(self, visible):
        """ Change the visibility of a UI control object on all devices
        """
        for obj in self.Objects:
            obj.SetVisible(visible)

    # Class Property Callbacks
    ##########################

    @property
    def Host(self):
        """ Defined Property to pass a list of Objects' Host property
        """
        return [obj.Host for obj in self.Objects]

    @property
    def ID(self):
        """ Defined Property to pass a list of Objects' ID property
        """
        return [obj.ID for obj in self.Objects]

    @property
    def Name(self):
        """ Defined Property to pass a list of Objects' Name property
        """
        return [obj.Name for obj in self.Objects]

    @property
    def Visible(self):
        """ Defined Property to pass a list of Objects' Visible property
        """
        return [obj.Visible for obj in self.Objects]


class Level():
    """ This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties
        and methods for all Level Objects created within this class.
    """

    def __init__(self, UIHost, ID, holdTime=None, repeatTime=None):
        self.Objects = []
        if isinstance(UIHost, (MirroreBUSDevice, MirrorUIDevice)):
            self.Objects = [OldLevel(obj, ID) for obj in UIHost.Objects]
        elif isinstance(UIHost, (eBUSDevice, UIDevice)):
            self.Objects = [OldLevel(UIHost, ID)]

        for obj in self.Objects:
            obj.MirroredParent = self

    # Methods:
    # The methods defined here operate the same as the Level methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def Dec(self):
        """ Nudge the level down a step for all devices
        """
        for obj in self.Objects:
            obj.Dec()

    def Inc(self):
        """ Nudge the level up a step for all devices
        """
        for obj in self.Objects:
            obj.Inc()

    def SetLevel(self, level):
        """ Set the current level for all devices
        """
        for obj in self.Objects:
            obj.SetLevel(level)

    def SetRange(self, Min, Max, Step=1):
        """ Set level object’s allowed range and the step size for all devices
        """
        for obj in self.Objects:
            obj.SetRange(Min, Max, Step)

    def SetVisible(self, visible):
        """ Change the visibility of a UI control object for all devices
        """
        for obj in self.Objects:
            obj.SetVisible(visible)

    # Class Property Callbacks
    ##########################

    @property
    def Host(self):
        """ Defined Property to pass a list of Objects' Host property
        """
        return [obj.Host for obj in self.Objects]

    @property
    def ID(self):
        """ Defined Property to pass a list of Objects' ID property
        """
        return [obj.ID for obj in self.Objects]

    @property
    def Level(self):
        """ Defined Property to pass a list of Objects' Level property
        """
        return [obj.Level for obj in self.Objects]

    @property
    def Max(self):
        """ Defined Property to pass a list of Objects' Max property
        """
        return [obj.Max for obj in self.Objects]

    @property
    def Min(self):
        """ Defined Property to pass a list of Objects' Min property
        """
        return [obj.Min for obj in self.Objects]

    @property
    def Name(self):
        """ Defined Property to pass a list of Objects' Name property
        """
        return [obj.Name for obj in self.Objects]

    @property
    def Visible(self):
        """ Defined Property to pass a list of Objects' Visible property
        """
        return [obj.Visible for obj in self.Objects]


class Slider():
    """ This class takes either a singular UIDevice or a
        MirrorUIDevice object and handles the properties
        and methods for all Level Objects created within this class.
    """

    def __init__(self, UIHost, ID):
        self.Objects = []
        if isinstance(UIHost, MirrorUIDevice):
            self.Objects = [OldSlider(obj, ID) for obj in UIHost.Objects]
        elif isinstance(UIHost, UIDevice):
            self.Objects = [OldSlider(UIHost, ID)]

        for obj in self.Objects:
            obj.Changed = self.CallChanged
            obj.Pressed = self.CallPressed
            obj.Released = self.CallReleased
            obj.MirroredParent = self
            
        self.Changed = self.__unassigned
        self.Pressed = self.__unassigned
        self.Released = self.__unassigned
        
    # Methods:
    # The methods defined here operate the same as the Level methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def SetEnable(self, enable):
        """ Enable or disable a UI control object on all devices
        """
        for obj in self.Objects:
            obj.SetEnable(enable)

    def SetFill(self, Fill):
        """ Set the current fill level for all devices
        """
        for obj in self.Objects:
            obj.SetFill(Fill)

    def SetRange(self, Min, Max, Step=1):
        """ Set slider object’s allowed range and the step size for all devices
        """
        for obj in self.Objects:
            obj.SetRange(Min, Max, Step)

    def SetVisible(self, visible):
        """ Change the visibility of a UI control object for all devices
        """
        for obj in self.Objects:
            obj.SetVisible(visible)
    
    def CallChanged(self, slider, state, value):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Changed(slider, state, value)
    
    def CallPressed(self, slider, state, value):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Pressed(slider, state, value)
    
    def CallReleased(self, slider, state, value):
        """ Callback passed to device list to redirect event to new event call
        """
        self.__Released(slider, state, value)

    # Class Property Callbacks
    ##########################

    @property
    def Enabled(self):
        """ Defined Property to pass a list of Objects' Enabled property
        """
        return [obj.Enabled for obj in self.Objects]

    @property
    def Fill(self):
        """ Defined Property to pass a list of Objects' Fill property
        """
        return [obj.Fill for obj in self.Objects]

    @property
    def Host(self):
        """ Defined Property to pass a list of Objects' Host property
        """
        return [obj.Host for obj in self.Objects]

    @property
    def ID(self):
        """ Defined Property to pass a list of Objects' ID property
        """
        return [obj.ID for obj in self.Objects]

    @property
    def Max(self):
        """ Defined Property to pass a list of Objects' Max property
        """
        return [obj.Max for obj in self.Objects]

    @property
    def Min(self):
        """ Defined Property to pass a list of Objects' Min property
        """
        return [obj.Min for obj in self.Objects]

    @property
    def Name(self):
        """ Defined Property to pass a list of Objects' Name property
        """
        return [obj.Name for obj in self.Objects]

    @property
    def Step(self):
        """ Defined Property to pass a list of Objects' Step property
        """
        return [obj.Step for obj in self.Objects]

    @property
    def Visible(self):
        """ Defined Property to pass a list of Objects' Visible property
        """
        return [obj.Visible for obj in self.Objects]

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """ If Module Events are not defined in user code, then do nothing.
        """
        pass

    @property
    def Changed(self):
        """ Passback the Changed Event
        """
        return self.__Changed

    @Changed.setter
    def Changed(self, handler):
        if callable(handler):
            self.__Changed = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Pressed(self):
        """ Passback the Pressed Event
        """
        return self.__Pressed

    @Pressed.setter
    def Pressed(self, handler):
        if callable(handler):
            self.__Pressed = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Released(self):
        """ Passback the Released Event
        """
        return self.__Released

    @Released.setter
    def Released(self, handler):
        if callable(handler):
            self.__Released = handler
        else:
            raise ValueError('handler must be a function')

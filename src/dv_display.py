# "author": "ted.cygan"

from extronlib import event
from extronlib.system import Timer, Wait
from abstracts import AbstractDvClass
from extronlib.interface import EthernetClientInterface, SerialInterface
from util_stopwatch import StopwatchClass



class SamsungQm75QClass(AbstractDvClass):
    def __init__(self, alias, data, processor):
        AbstractDvClass.__init__(self, alias, data, [])


        # self.driver = EthernetClientInterface(data['switcher'], data[alias])
        self.driver = SerialInterface(processor, data['display1'])

        self.__polling = Timer(60, self.__polling_cb)
        # self.__buffer=bytearray()
        self.__desired = False
        self.__busy = False

        self.__warmcool = StopwatchClass('displaywarmcool', data, 8.0, 1.0)  
        self.__warmcool.subscribe_one(self.__warmcool_event_cb) 
        self.__warmcoollast = None 

        self.__lastsend=None

            
 
        # @event(self.driver, ['Connected', 'Disconnected'])
        # def __driverConnectDisconnect(client, state):
        #     self.print_me('__driverConnectDisconnect status:{} on IP:{}'.format(state, client.IPAddress))
        #     if state=='Connected':
        #         self.online = True
        #     else:
        #         self.online = False
        #     self._raise_event('ConnectionStatus', state, None)


        @event(self.driver, ['Online', 'Offline'])
        def __driveronlineoffline(interface, state):
            self.print_me('__driveronlineoffline state:{}'.format(state))

            if state == 'Online':
                self.online = True
                self._raise_event('ConnectionStatus', 'Connected', None)

            else:
                self.online = False
                self._raise_event('ConnectionStatus', 'Disconnected', None)


        @event(self.driver, 'ReceiveData')
        def __driverReceiveData(client, rcvdata):  #bytes received
            self.print_me('rx <{}>'.format(rcvdata))
    
            try:
                # self.__buffer.append(rcvdata)
                # # if b'\x03\x0c\xf1' in self.__buffer:  #success cmd rx
                # if self.__buffer.find(b'\x03\x0c\xf1'):

                #     self.__buffer = ''
                if self.__lastsend != b'\x08\x22\x0A\x00\x05\x00\xC7':

                    self.power = self.__desired
                    if self.__desired:
                        self._raise_event('Power', 'On', None)
                        if self.__busy:
                            self.__warmcool.start(self._data['warmup'])
                            self.__warmcoollast = 'warmup'
                    else:
                        self._raise_event('Power', 'Off', None)
                        if self.__busy:
                            self.__warmcool.start(self._data['cooldown'])
                            self.__warmcoollast = 'cooldown'
            

            except Exception as e:
                self.print_me('ERR ReceiveData <{}>, err <{}>'.format(rcvdata, type(e)))



# SamsungQn7  display1          -->  power_me:True, ip:172.22.0.43, port:2033
# SamsungQn7  display1          -->  tx <b'\x08"\x00\x00\x00\x02\xd4'>
# SamsungQn7  display2          -->  power_me:True, ip:172.22.0.43, port:2034
# SamsungQn7  display2          -->  tx <b'\x08"\x00\x00\x00\x02\xd4'>
# SamsungQn7  display2          -->  rx <b'\x03\x0c'>
# SamsungQn7  display2          -->  rx <b'\xf1'>
# SamsungQn7  display1          -->  tx <b'\x08"\n\x00\x05\x00\xc7'>
# SamsungQn7  display2          -->  tx <b'\x08"\n\x00\x05\x00\xc7'>
# SamsungQn7  display2          -->  rx <b'\x03\x0c'>
# SamsungQn7  display2          -->  rx <b'\xf1'>
                
# SamsungQn75Q60cafClass display2 --> rx <b'\x00'>   //i'm offline indicator
# issue with displays not turning back on after turning off and staying off for a long time.  Issue not noticed when display is on.  Turning off not issue


    #END CONSTRUCTOR


    def __polling_cb(self, timer, count): 
        self.print_me('__polling_cb online:{}, desired:{}, power:{}, busy:{}'.format(self.online, self.__desired, self.power, self.__busy))
            
        # if self.online != True:
        #     self.__driver_connect()
        # else:
        #     if self.power == False:
        #         self.__send(b'\x08\x22\x0A\x00\x05\x00\xC7')  #hdmi1  keep-alive

        
    # def __driver_connect(self):  
    #     result = self.driver.Connect(5)
    #     self.print_me('Connection attempted')


    
    def power_me(self, desired):
        self.print_me('power_me:{}, ip:{}, port:{}, busy:{}'.format(desired,self._data['switcher'], self._data[self.alias], self.__busy))

        if not self.__busy:
            self.__busy = True

            self.__desired=desired

            if desired:
                if self.online:   
                    self.__send(b'\x08\x22\x00\x00\x00\x02\xD4')   

                @Wait(6)    
                def __powerwaitInput():
                    if self.online:   
                        self.__send(b'\x08\x22\x0A\x00\x05\x00\xC7')  #hdmi1

            else:
                if self.online:   
                    self.__send(b'\x08\x22\x00\x00\x00\x01\xD5')

            @Wait(6)    
            def _waitbeforenextcommand():   
                self.__busy = False
        


    def __send(self, val):
        self.print_me('tx <{}>'.format(val))
        self.__lastsend=val
        self.driver.Send(val)


    def tx_inject(self, val):
        self.__send(val)


    def __warmcool_event_cb(self, command, value, qualifier):
        self.print_me('__warmcool_event_cb > c:{}, v:{}, q:{}'.format(command, value, qualifier))

        if command == 'Running':
            self._raise_event('WARMCOOL'+self.alias[-1],  self.__warmcoollast, value)

        elif command == 'Stopped':
            self._raise_event('WARMCOOL'+self.alias[-1], 'stop', value)


    def warmcool_cancel(self):
        self.__warmcool.stop()


    def forcehdmi(self):
        self.__send(b'\x08\x22\x0A\x00\x05\x00\xC7')  #hdmi1








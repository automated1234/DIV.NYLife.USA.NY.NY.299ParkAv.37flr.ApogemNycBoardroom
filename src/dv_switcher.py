# "author": "ted.cygan"

from abstracts import AbstractDvClass
from extronlib import event
from extronlib.system import Timer
from extronlib.interface import EthernetClientInterface


class AtlonaAtOmeMs42Class(AbstractDvClass):
    def __init__(self, alias, data):
        AbstractDvClass.__init__(self, alias, data, [])
        

        self.driver = EthernetClientInterface(data['switcher'], 9000)
        self.__polling = Timer(60, self.__polling_cb)
        self.__buffer=''


        @event(self.driver, ['Connected', 'Disconnected'])
        def __driverConnectDisconnect(client, state):
            self.print_me('__driverConnectDisconnect status:{} on IP:{}'.format(state, client.IPAddress))
            if state=='Connected':
                self.online = True
            else:
                self.online = False
            self._raise_event('ConnectionStatus', state, None)


        @event(self.driver, 'ReceiveData')
        def __driverReceiveData(client, rcvdata):  #bytes received
            self.print_me('rx <{}>'.format(rcvdata))
            self.__processrx(rcvdata)
    #END CONSTRUCTOR


    def __polling_cb(self, timer, count): 
        self.print_me('__polling_cb online:{}'.format(self.online))
            
        if self.online != True:
            self.__driver_connect()
        else:
            # if self.power == False:
            self.__send('InputStatus\x0d')  

        
    def __driver_connect(self):  
        result = self.driver.Connect(5)
        self.print_me('Connection attempted')

    
    def __send(self, val):
        self.print_me('tx <{}>'.format(val))
        self.driver.Send(val)


    def switch_me(self, innumber, outnumber):
        self.print_me('switch_me > in:{}, out:{}, '.format(innumber, outnumber))

        if innumber <= self._data['switcher_inscount'] and outnumber <= self._data['switcher_outscount']:
            if self.online:
                self.__send('x{}AVx{}\x0d'.format(innumber, outnumber))
            else:
                self._raise_event('MATRIXROUTE', innumber, outnumber)

        else:
            self.print_me('ERR invalid in:{} or out:{}'.format(innumber, outnumber))



    def power_me(self, desired):
        self.print_me('power_me > desired:{}'.format(desired))
        if self.online:
            if desired:
                self.__send('PWON\x0d')
            

    def rx_inject(self, val):  
        self.print_me('TRUE rx_inject (orr) <{}>'.format(val))
        self.__processrx(val)


    def __processrx(self, rcvdata):

        try:
            self.__buffer+=rcvdata.decode()
            # self.__buffer+=rcvdata

        except Exception as e:
            self.print_me('ERR ReceiveData <{}>, err:{}'.format(rcvdata, type(e)))


        while True:
            try:
                # partition() finds the first occurance of '\r' and returns everything
                extracted, delimiter, remainder = self.__buffer.partition('\r\n')

                if not delimiter:
                    break

                # Save any left over data for the next time around the loop.
                self.__buffer = remainder


                if 'Command FAILED' in extracted:
                    self.print_me('ERR:{}'.format(extracted))

                # Switcher    switcher          -->  rx <b'InputStatus 000000\r\n'>
                elif extracted.startswith('InputStatus '):
                    syncs = {
                        1:extracted[12:13],
                        2:extracted[13:14],
                        3:extracted[14:15],
                        4:extracted[15:16],
                        # 5:extracted[16:17],
                    }
                    self._raise_event('INPUTSYNCS', syncs, None)

                elif extracted.startswith('InputStatus'):
                    syncs = {
                        1:extracted[11:12],
                        2:extracted[13:14],
                    }
                    self._raise_event('INPUTSYNC', int(syncs[1]), int(syncs[2]))
                
                # Switcher    switcher          -->  rx <b'x2AVx1,x2AVx2\r\n'>
                elif 'AVx' in extracted:
                    self.print_me('extracted:{}, len:{}'.format(extracted, len(extracted)))
                    outs = []
                    outs = extracted.split(',')

                    for ou in outs:
                        self._raise_event('MATRIXROUTE', int(ou[1:2]), int(ou[-1]))

                    
            except ValueError:
                self.print_me('ERR extracted:{}, len:{}, delimiter:{} something went wrong'.format(extracted, len(extracted), repr(delimiter)))


            # AtlonaAtOm    switcher          -->  tx <x1AVx1\x0d>
            # AtlonaAtOm    switcher          -->  rx <b'Command FAILED: (]x1AVx1)\r\n'>

            # AtlonaAtOm    switcher          -->  switch_me > in:HDBaseT 2, out:HDMI,
            # AtlonaAtOm    switcher          -->  tx <x2AVx2\x0d>
            # AtlonaAtOm    switcher          -->  rx <b'x2AVx1,x2AVx2\r\n'>
            # AtlonaAtOm    switcher          -->  switch_me > in:HDBaseT 2, out:HDBaseT,
            # AtlonaAtOm    switcher          -->  tx <x2AVx1\x0d>
            # AtlonaAtOm    switcher          -->  rx <b'x2AVx1,x2AVx2\r\n'>

            # AtlonaAtOm    switcher          -->  tx <InputStatus\x0d>
            # AtlonaAtOm    switcher          -->  rx <b'InputStatus 000000\r\n'>
            # AtlonaAtOm  switcher          -->  __polling_cb online:True
            # AtlonaAtOm  switcher          -->  tx <InputStatus\x0d>
            # AtlonaAtOm  switcher          -->  rx <b'InputStatus 100000\r\n'>

            # AtlonaAtOm  switcher          -->  rx <b'InputStatus1 0\r\n'>
            # AtlonaAtOm  switcher          -->  ERR ReceiveData <b'InputStatus1 0\r\n'>, err:<class 'TypeError'>
            # AtlonaAtOm  switcher          -->  rx <b'InputStatus1 1\r\n'>
            # AtlonaAtOm  switcher          -->  ERR ReceiveData <b'InputStatus1 1\r\n'>, err:<class 'TypeError'>


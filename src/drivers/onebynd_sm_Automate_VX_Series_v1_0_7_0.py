from extronlib.system import Wait, ProgramLog
import base64
import urllib.error
import urllib.request
import json

class DeviceClass:
    def __init__(self, ipAddress, port, deviceUsername=None, devicePassword=None):
        
        self.Subscription = {}
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.IPAddress = ipAddress
        self.DefaultPort = port
        
        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        
        self.RootURL = 'http://{0}:{1}/'.format(ipAddress, port)
        if deviceUsername is not None and devicePassword is not None:
            self.base64Auth = base64.b64encode(deviceUsername.encode() + b':' + devicePassword.encode())
        else:
            self.base64Auth = None
        self.Opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler()) 
        
        self.Models = {}

        self.Commands = {
            'AutoSwitch' : {'Status': {}},
            'ConnectionStatus' : {'Status': {}},
            'CameraPresetRecall' : {'Parameters':['Camera'], 'Status': {}},
            'ForceRoomConfiguration' : {'Status': {}},
            'ISORecording' : {'Status': {}},
            'Layout' : {'Status': {}},
            'Output' : {'Status': {}},
            'Record' : {'Status': {}},
            'RoomConfiguration' : {'Status': {}},
            'Scenario' : {'Parameters':['ID'], 'Status': {}},
            'Sleep' : {'Status': {}},
            'Stream' : {'Status': {}},
            'SwitchCamera' : {'Status': {}},
            'Wake' : {'Status': {}}
        }

        self.Authenticated = False
        self.Token = None

    def TokenRequest(self, value, qualifier):

        self.TokenRequestHandler()

    def TokenRequestHandler(self):

        cmdString = 'get-token' # login command
        res = self.__SetHelper('TokenRequest', None, None, url=cmdString)
        if res:
            try:
                self.Token = res['token'] # store token
                self.Authenticated = True # set to True if token in response
            except KeyError:
                self.Error(['Failed to obtain token'])
                self.TokenRequest( None, None)
    
    def SetAutoSwitch(self, value, qualifier):

        ValueStateValues = {
            'On'  : 'api/StartAutoSwitch',
            'Off' : 'api/StopAutoSwitch'
        }

        self.__SetHelper('AutoSwitch', value, qualifier, ValueStateValues[value])

    def UpdateAutoSwitch(self, value, qualifier):

        ValueStateValues = {
            'true'  : 'On',
            'false' : 'Off',
            True    : 'On',
            False   : 'Off'
        }

        AutoSwitchCmdString = 'api/AutoSwitchStatus'
        res = self.__UpdateHelper('AutoSwitch', value, qualifier, AutoSwitchCmdString)
        if res:
            try:
                value = ValueStateValues[res['results']]
                self.WriteStatus('AutoSwitch', value, qualifier)
            except KeyError:
                self.Error(['Auto Switch: Invalid/unexpected response'])

    def SetCameraPresetRecall(self, value, qualifier):

        if 1 <= int(value) <= 255 and 1 <= int(qualifier['Camera']) <= 255:
            data = {
                'cam' : qualifier['Camera'],
                'pre' : value
            }

            CameraPresetRecallCmdString = 'api/CallCameraPreset'
            self.__SetHelper('CameraPresetRecall', value, qualifier, CameraPresetRecallCmdString, data)
        else:
            self.Discard('Invalid Command for SetCameraPresetRecall')

    def SetForceRoomConfiguration(self, value, qualifier):

        if 1 <= int(value) <= 99:
            data = {
                'id' : value
            }
            ForceRoomConfigurationCmdString = 'api/ForceChangeRoomConfig'
            self.__SetHelper('ForceRoomConfiguration', value, qualifier, ForceRoomConfigurationCmdString, data)
        else:
            self.Discard('Invalid Command for SetForceRoomConfiguration')

    def SetISORecording(self, value, qualifier):

        ValueStateValues = {
            'Start' : 'api/StartISORecord',
            'Stop'  : 'api/StopISORecord'
        }

        self.__SetHelper('ISORecording', value, qualifier, ValueStateValues[value])

    def UpdateISORecording(self, value, qualifier):

        ValueStateValues = {
            'true'  : 'Start',
            'false' : 'Stop',
            True    : 'Start',
            False   : 'Stop'
        }

        ISORecordingCmdString = 'api/ISORecordStatus'
        res = self.__UpdateHelper('ISORecording', value, qualifier, ISORecordingCmdString)
        if res:
            try:
                value = ValueStateValues[res['results']]
                self.WriteStatus('ISORecording', value, qualifier)
            except KeyError:
                self.Error(['ISO Recording: Invalid/unexpected response'])

    def SetLayout(self, value, qualifier):

        if value in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            data = {
                'id' : value
            }

            LayoutCmdString = 'api/ChangeLayout'
            self.__SetHelper('Layout', value, qualifier, LayoutCmdString, data)
        else:
            self.Discard('Invalid Command for SetLayout')

    def SetOutput(self, value, qualifier):

        ValueStateValues = {
            'On'  : 'api/StartOutput',
            'Off' : 'api/StopOutput'
        }

        if value in ValueStateValues:
            self.__SetHelper('Output', value, qualifier, ValueStateValues[value])
        else:
            self.Discard('Invalid Command for SetOutput')
        
    def UpdateOutput(self, value, qualifier):

        ValueStateValues = {
            'true'  : 'On',
            'false' : 'Off',
            True    : 'On',
            False   : 'Off'
        }

        OutputCmdString = 'api/OutputStatus'
        res = self.__UpdateHelper('Output', value, qualifier, OutputCmdString)
        if res:
            try:
                value = ValueStateValues[res['results']]
                self.WriteStatus('Output', value, qualifier)
            except KeyError:
                self.Error(['Output: Invalid/unexpected response'])

    def SetRecord(self, value, qualifier):

        ValueStateValues = {
            'Start' : 'api/StartRecord',
            'Stop'  : 'api/StopRecord'
        }

        if value in ValueStateValues:
            self.__SetHelper('Record', value, qualifier, ValueStateValues[value])
        else:
            self.Discard('Invalid Command for SetRecord')

    def UpdateRecord(self, value, qualifier):

        ValueStateValues = {
            'true'  : 'Start',
            'false' : 'Stop',
            True    : 'Start',
            False   : 'Stop'
        }

        RecordCmdString = 'api/RecordStatus'
        res = self.__UpdateHelper('Record', value, qualifier, RecordCmdString)
        if res:
            try:
                value = ValueStateValues[res['results']]
                self.WriteStatus('Record', value, qualifier)
            except KeyError:
                self.Error(['Record: Invalid/unexpected response'])

    def SetRoomConfiguration(self, value, qualifier):

        if 1 <= int(value) <= 99:
            data = {
                'id' : value
            }

            RoomConfigurationCmdString = 'api/ChangeRoomConfiguration'
            self.__SetHelper('RoomConfiguration', value, qualifier, RoomConfigurationCmdString, data)
        else:
            self.Discard('Invalid Command for SetRoomConfiguration')
    def SetScenario(self, value, qualifier):

        if qualifier['ID']:
            data = {
                'id' : qualifier['ID']
            }

            ScenarioCmdString = 'api/GoToScenario'
            self.__SetHelper('Scenario', value, qualifier, url=ScenarioCmdString, data=data)
        else:
            self.Discard('Invalid Command for SetScenario')

    def SetSleep(self, value, qualifier):

        SleepCmdString = 'api/Sleep'
        self.__SetHelper('Sleep', value, qualifier, url=SleepCmdString)

    def SetStream(self, value, qualifier):

        ValueStateValues = {
            'Start' : 'api/StartStream',
            'Stop'  : 'api/StopStream'
        }

        if value in ValueStateValues:
            self.__SetHelper('Stream', value, qualifier, ValueStateValues[value])
        else:
            self.Discard('Invalid Command for SetStream')

    def UpdateStream(self, value, qualifier):

        ValueStateValues = {
            'true'  : 'Start',
            'false' : 'Stop',
            True    : 'Start',
            False   : 'Stop'
        }

        StreamCmdString = 'api/StreamStatus'
        res = self.__UpdateHelper('Stream', value, qualifier, StreamCmdString)
        if res:
            try:
                value = ValueStateValues[res['results']]
                self.WriteStatus('Stream', value, qualifier)
            except KeyError:
                self.Error(['Stream: Invalid/unexpected response'])

    def SetSwitchCamera(self, value, qualifier):

        if 1 <= int(value) <= 255:
            data = {
                'address' : value
            }

            SwitchCameraCmdString = 'api/ManualSwitchCamera'
            self.__SetHelper('SwitchCamera', value, qualifier, SwitchCameraCmdString, data)
        else:
            self.Discard('Invalid Command for SetSwitchCamera')

    def UpdateSwitchCamera(self, value, qualifier):

        SwitchCameraCmdString = 'api/CameraStatus'
        res = self.__UpdateHelper('SwitchCamera', value, qualifier, url=SwitchCameraCmdString)
        if res:
            try:
                value = res['address']
                if 1 <= int(value) <= 255:
                    self.WriteStatus('SwitchCamera', value, qualifier)
            except (KeyError, IndexError, AttributeError):
                self.Error(['Switch Camera: Invalid/unexpected response'])

    def SetWake(self, value, qualifier):

        WakeCmdString = 'api/Wake'
        self.__SetHelper('Wake', value, qualifier, url=WakeCmdString)

    def __CheckResponseForErrors(self, sourceCmdName, response):

        try:
            res = json.loads(response.read().decode())
            if res['status'] == 'Error':
                self.Error(['Error:', res['err']])
                return ''
            return res
        except TypeError:
            self.Error(['Invalid Response'])

    def __SetHelper(self, command, value, qualifier, url='', data=None):

        self.Debug = True

        if self.Authenticated or command == 'TokenRequest':
            url = '{0}{1}'.format(self.RootURL, url)
            if data: # if command body exists
                data = json.dumps(data).encode() # encode it

            if command == 'TokenRequest':  # if login command, don't include token
                headers = {
                    'Content-Type'      : 'application/json',
                    'Authorization'     : self.base64Auth
                }
            else:
                headers = {
                    'Content-Type'      : 'application/json',
                    'Authorization'     : self.Token
                }

            my_request = urllib.request.Request(url, data=data, headers=headers, method='POST')

            try:
                res = self.Opener.open(my_request, timeout=10)  # open() returns a http.client.HTTPResponse object if successful
            except urllib.error.HTTPError as err:  # includes HTTP status codes 101, 300-505
                self.Error(['{0} {1} - {2}'.format(command, err.code, err.reason)])
                res = ''
            except urllib.error.URLError as err:  # received if can't reach the server (times out)
                self.Error(['{0} {1}'.format(command, err.reason)])
                res = ''
            except Exception as err:  # includes HTTP status code 100 and any invalid status code
                res = ''
            else:
                if res.status not in (200, 202):
                    self.Error(['{0} {1} - {2}'.format(command, res.status, res.msg)])
                    res = ''
                else:
                    res = self.__CheckResponseForErrors(command, res)
            return res
        else:
            self.Discard('Invalid Command')
            self.TokenRequest(None, None)

    def __UpdateHelper(self, command, value, qualifier, url='', data=None):

        if self.Authenticated:
            if self.initializationChk:
                self.OnConnected()
                self.initializationChk = False

            self.counter = self.counter + 1
            if self.counter > self.connectionCounter and self.connectionFlag:
                self.OnDisconnected()

            url = '{0}{1}'.format(self.RootURL, url)
            headers = {
                'Content-Type'      : 'application/json',
                'Authorization'     : self.Token
            }

            my_request = urllib.request.Request(url, data=data, headers=headers, method='POST')

            try:
                res = self.Opener.open(my_request, timeout=10) # open() returns a http.client.HTTPResponse object if successful
            except urllib.error.HTTPError as err: # includes HTTP status codes 101, 300-505
                self.Error(['{0} {1} - {2}'.format(command, err.code, err.reason)])
                res = ''
            except urllib.error.URLError as err: # received if can't reach the server (times out)
                self.Error(['{0} {1}'.format(command, err.reason)])
                res = ''
            except Exception as err: # includes HTTP status code 100 and any invalid status code
                res = ''
            else:
                if res.status not in (200, 202):
                    self.Error(['{0} {1} - {2}'.format(command, res.status, res.msg)])
                    res = ''
                else:
                    res = self.__CheckResponseForErrors(command, res)
            return res
        else:
            self.Error(['Token not obtained'])
            self.TokenRequest( None, None)

    def OnConnected(self):

        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0

        self.TokenRequest(None, None)

    def OnDisconnected(self):

        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

        self.Token = None
        self.Authenticated = False

    ######################################################    
    # RECOMMENDED not to modify the code below this point
    ######################################################

    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = getattr(self, 'Set%s' % command, None)
        if method is not None and callable(method):
            method(value, qualifier)
        else:
            raise AttributeError(command + 'does not support Set.')


    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = getattr(self, 'Update%s' % command, None)
        if method is not None and callable(method):
            method(None, qualifier)
        else:
            raise AttributeError(command + 'does not support Update.')

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback 
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command, None)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method':{}}
        
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
        
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return
        
            Method['callback'] = callback
            Method['qualifier'] = qualifier    
        else:
            raise KeyError('Invalid command for SubscribeStatus ' + command)

    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription :
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)  

    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return  
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands.get(command, None)
        if Command:
            Status = Command['Status']
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Status = Status[qualifier[Parameter]]
                    except KeyError:
                        return None
            try:
                return Status['Live']
            except:
                return None
        else:
            raise KeyError('Invalid command for ReadStatus: ' + command)


    def MissingCredentialsLog(self, credential_type):
        if isinstance(self, EthernetClientInterface):
            port_info = 'IP Address: {0}:{1}'.format(self.IPAddress, self.IPPort)
        elif isinstance(self, SerialInterface):
            port_info = 'Host Alias: {0}\r\nPort: {1}'.format(self.Host.DeviceAlias, self.Port)
        else:
            return 
        ProgramLog("{0} module received a request from the device for a {1}, "
                   "but device{1} was not provided.\n Please provide a device{1} "
                   "and attempt again.\n Ex: dvInterface.device{1} = '{1}'\n Please "
                   "review the communication sheet.\n {2}"
                   .format(__name__, credential_type, port_info), 'warning') 

class HTTPClass(DeviceClass):
    def __init__(self, ipAddress, port, deviceUsername=None, devicePassword=None, Model=None):
        self.ConnectionType = 'HTTP'
        DeviceClass.__init__(self, ipAddress, port, deviceUsername, devicePassword)
        # Check if Model belongs to a subclass      
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')             
            else:
                self.Models[Model]()

    def Error(self, message):
        portInfo = 'IP Address/Host: {0}'.format(self.RootURL)
        print('Module: {}'.format(__name__), portInfo, 'Error Message: {}'.format(message[0]), sep='\r\n')
  
    def Discard(self, message):
        self.Error([message])
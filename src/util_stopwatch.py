# "author": "ted.cygan"

from extronlib.system import Timer
from abstracts import AbstractDvClass


class StopwatchClass(AbstractDvClass):   
    def __init__(self, alias, data, steps, freq): 
        AbstractDvClass.__init__(self, alias, data, [])
        # if step = .5, total=60  //pulse every .5s 60 times = 30s
        self.__sec = 0
        self.__min = 0
        self.__hour = 0
        self.online=True
        self.power=''
        self.__steps = steps
        self.__freq = freq

        self.__timer =  Timer(self.__freq, self.__offtimer_cb)
        self.__timer.Stop()


    def start(self, st2):
        self.print_me('start > old steps:{}, new steps:{}'.format(self.__steps, st2))

        if st2 != self.__steps:
            self.__steps = st2
            # self.__timer.Change(st2)
        self.__timer.Restart()


    def stop(self):
        self.print_me('stop')
        if self.__timer.State == 'Running' or self.__timer.State == 'Paused':
            self.__timer.Stop()
            


    def __offtimer_cb(self, timer, count):
        if self.__timer.State == 'Running':
            self.__sec =+ 1

            if self.__sec >= 60:
                self.__min += 1
                self.__sec=0

            if self.__min >= 60:
                self.__hour += 1
                self.__min =0  
        else:
            self.__sec = 0
            self.__min = 0
            self.__hour = 0

        if self.__steps != None:
            if count >= self.__steps:
                self.__timer.Stop()

        self.print_me('__offtimer_cb > count:{}, state:{},  clock:{:0>2}:{:0>2}:{:0>2}'.format(count, self.__timer.State, self.__hour, self.__min, self.__sec))
        self._raise_event_one(self.__timer.State, count, '{:0>2}:{:0>2}:{:0>2}'.format(self.__hour, self.__min, self.__sec))






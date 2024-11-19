# "author": "ted.cygan"


class DebugClass:

    def __init__(self, alias):
        self.debug = False
        self.alias = alias


    def print_me(self, val):
        if val.startswith('ERR'):
            self.__print_me(val)

        elif val.startswith('TRUE'): 
            self.__print_me(val[5:])

        elif self.debug:
            self.__print_me(val)


    def __print_me(self, val):       
        print('{} --> {}'.format(self.__fix_len(self.__class__.__name__, self.alias), val))


    def __fix_len(self, nam1, nam2):
        return '{} {}'.format(nam1, nam2).ljust(30)


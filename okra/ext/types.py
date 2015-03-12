import re

from abc import ABCMeta, abstractmethod


try:
    # Python 2.x
    _basestring = basestring
except:
    # Python 3.x
    _basestring = (str, bytes)


class ExtensionType(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def constructor(loader, node): pass

    @staticmethod
    @abstractmethod
    def represeter(dumper, data): pass

    @staticmethod
    @abstractmethod
    def register(): pass

    @staticmethod
    @abstractmethod
    def is_type(obj): pass


class long(int, ExtensionType):
    TAG = '!long'
    
    def __new__(cls, number):
        print(repr(number))
        if not isinstance(number, int) and isinstance(number, _basestring):
            number = int(number[:-1])
            
        return int.__new__(cls, number)

    def __repr__(self):
        return 'long({})'.format(self)

    @staticmethod
    def constructor(loader, node):
        return long(loader.construct_scalar(node))

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(long.TAG, '{}L'.format(data))
        
    @staticmethod
    def register():
        yaml.add_representer(long, long.representer)
        yaml.add_constructor(long.TAG, long.constructor)
        yaml.add_implicit_resolver(long.TAG, re.compile('\d+L'))


    @staticmethod
    def is_typed(obj):

        try:
            long(obj)
        except: 
            return False

        return True


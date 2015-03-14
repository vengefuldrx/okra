import re
import logging

from abc import ABCMeta, abstractmethod
from collections import OrderedDict

import yaml

try:
    # Python 2.x
    _basestring = basestring
except:
    # Python 3.x
    _basestring = (str, bytes)

Log = logging.getLogger(__name__)

class ExtensionType(object, metaclass = ABCMeta):
    @staticmethod
    @abstractmethod
    def constructor(loader, node): 
        raise NotImplemented()

    @staticmethod
    @abstractmethod
    def represeter(dumper, data):
        raise NotImplemented()

    @staticmethod
    @abstractmethod
    def register():
        raise NotImplemented()

    @staticmethod
    @abstractmethod
    def is_type(obj): 
        raise NotImplemented()


class Long(int, ExtensionType):
    """
    Class for representing Longs for languages that distinguish between normal and Long integer types.
    """
    NAME = 'long'
    TAG = '!long'


    def __new__(cls, number):

        if not isinstance(number, int) and isinstance(number, _basestring):
            number = int(number[:-1])
            
        return int.__new__(cls, number)

    def __repr__(self):
        return 'Long({})'.format(self)

    @staticmethod
    def constructor(loader, node):
        return Long(loader.construct_scalar(node))

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(Long.TAG, '{}L'.format(data))
        
    @staticmethod
    def register():
        Log.debug('Registering extension type: {}'.format(Long))

        yaml.add_representer(Long, Long.representer)
        yaml.add_constructor(Long.TAG, Long.constructor)
        yaml.add_implicit_resolver(Long.TAG, re.compile('\d+L'))

    @staticmethod
    def is_type(obj):

        try:
            Long(obj)
        except: 
            return False

        return True


class Duration(object):
    """
    """
    NAME = 'duration'
    TAG = '!duration'

    MINUTES_PER_HOUR = 60
    SECONDS_PER_MINUTE = 60
    MILLIS_PER_SECOND = 1000


    def __init__(self, hours=0, minutes=0, seconds=0, millis=0):

        
        mins = minutes + (hours * Duration.MINUTES_PER_HOUR)
        seconds = seconds + (mins * Duration.SECONDS_PER_MINUTE)
        self.millis = millis + (seconds * Duration.MILLIS_PER_SECOND)
        

    def __repr__(self):
        return 'Duration(millis={})'.format(self.millis)

    def __str__(self):
        return '{}ms'.format(self.millis)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Duration.parse_type(value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(Duration.TAG, '{}'.format(data))

    @staticmethod
    def register():
        Log.debug('Registering extension type: {}'.format(Duration))

        yaml.add_representer(Duration, Duration.representer)
        yaml.add_constructor(Duration.TAG, Duration.constructor)
        yaml.add_implicit_resolver(Duration.TAG, re.compile('\d+ms'))

    @staticmethod
    def parse_type(value):
        value = str(value).strip()
        millis = re.sub(r'ms', '', value)
        if millis.isdigit():
            return Duration(millis=int(millis))

        raise ValueError()


    @staticmethod
    def is_type(obj):
        try:
            Duration.parse_type(obj)
        except: 
            return False

        return True


_extension_types = OrderedDict([
    (Long.NAME, Long),
    (Duration.NAME, Duration),
])

for _et in _extension_types.values():
    _et.register()

def is_extension_type(type):
    return type in _extension_types

extension_tt = OrderedDict([ (name, ext_type.is_type) for name, ext_type in _extension_types.items() ])

# -*- coding: utf-8 -*-
'''DelogX.utils.compat

Utils about compatibility of OS and Python.
'''
from __future__ import unicode_literals

import codecs
import os
import platform
import sys


class Compat(object):
    '''Compatibility utils.'''

    @classmethod
    def version(cls):
        '''Return the major version of Python.

        Returns:

            int: Major version of Python.
        '''
        return sys.version_info.major

    @classmethod
    def sys(cls):
        '''Return the name of the operating system.

        Returns:

            str: Name of the operating system.
        '''
        return platform.system()

    @classmethod
    def is_wsl(cls):
        '''Whether DelogX is running on WSL (Windows Subsystem for Linux).'''
        def _read_file(filename):
            if not os.path.isfile(filename):
                return ''
            with codecs.open(filename, encoding='utf-8') as some_file:
                lines = some_file.readlines()
            return ''.join(lines)
        if Compat.sys() != 'Linux':
            return False
        version = _read_file('/proc/version')
        osrelease = _read_file('/proc/sys/kernel/osrelease')
        if 'Microsoft' in version or 'Microsoft' in osrelease:
            return True
        return False

    @classmethod
    def unicode_convert(cls, string, to_byte=True):
        '''Convert a string to unicode or byte.

        Args:

            string (str): String needs to convert.
            to_byte (bool): Whether convert to byte, defaults True.

        Returns:

            str: Converted string.
        '''
        if Compat.version() < 3:
            if to_byte:
                return string.encode('utf-8')
            else:
                return string.decode('utf-8')
        return string

    @classmethod
    def cmp_to_key(cls):
        '''Return a class which convert cmp function to key function.

        Returns:

            class: Class to convert cmp function to key function.
        '''
        return CmpToKey


class CmpToKey(object):
    '''Convert cmp function to key function in `sorted()`.'''

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return self.sort_compare(self.obj, other.obj) < 0

    def __gt__(self, other):
        return self.sort_compare(self.obj, other.obj) > 0

    def __eq__(self, other):
        return self.sort_compare(self.obj, other.obj) == 0

    def __le__(self, other):
        return self.sort_compare(self.obj, other.obj) <= 0

    def __ge__(self, other):
        return self.sort_compare(self.obj, other.obj) >= 0

    def __ne__(self, other):
        return self.sort_compare(self.obj, other.obj) != 0

    @classmethod
    def sort_compare(cls, item_a, item_b):
        '''The cmp function to compare `DelogX.entity.item.Page`.

        Args:

            item_a (object): First object to compare.
            item_b (object): Second object.

        Returns:

            int: 0 is `a = b`, positive is `a > b`, negative is `a < b`.
        '''
        a_sort = item_a[1].sort
        b_sort = item_b[1].sort
        if a_sort is not None and b_sort is not None:
            return a_sort - b_sort
        elif a_sort is None and b_sort is None:
            return 0
        elif a_sort is None:
            return 1
        else:
            return -1

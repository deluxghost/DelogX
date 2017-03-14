# -*- coding: utf-8 -*-
'''The class, definition and interface of Error.'''
from __future__ import unicode_literals


class Error(Exception):
    '''Base class to define the errors of DelogX.'''

    def __init__(self, value):
        super(Error, self).__init__()
        self.value = value

    def __str__(self):
        return self.value

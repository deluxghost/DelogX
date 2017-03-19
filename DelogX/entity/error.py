# -*- coding: utf-8 -*-
'''DelogX.entity.error

Define error interface of DelogX.
'''
from __future__ import unicode_literals


class Error(Exception):
    '''Base class to define the errors of DelogX.'''

    def __init__(self, value):
        super(Error, self).__init__()
        self.value = value

    def __str__(self):
        return self.value

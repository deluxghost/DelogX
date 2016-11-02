# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class DelogXError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
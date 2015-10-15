# -*- coding: utf-8 -*-
class DelogXError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
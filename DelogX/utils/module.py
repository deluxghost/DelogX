# -*- coding: utf-8 -*-
'''DelogX.entity.module

Class to check whether modules ready.
'''
from __future__ import unicode_literals


class Module(object):
    '''Module checker of DelogX

    Attributes:

        modules_require (list of str): Required modules.
    '''
    modules_require = [
        'flask',
        'watchdog',
        'markdown'
    ]

    @classmethod
    def has(cls, module):
        '''Check whether a module is installed.

        Args:

            module (str): Name of the module.

        Returns:

            bool: Whether the module is installed.
        '''
        try:
            __import__(module)
            return True
        except ImportError:
            return False

    @classmethod
    def ready(cls):
        '''Check whether all required modules are installed.

        Returns:

            bool: Whether all required modules are installed.
        '''
        return Module.missing() is None

    @classmethod
    def missing(cls):
        '''Return names of the missing modules.

        Returns:

            list of str: Names of the missing modules.
        '''
        modules_missing = list()
        for module in Module.modules_require:
            if not Module.has(module):
                modules_missing.append(module)
        if modules_missing:
            return modules_missing
        return None

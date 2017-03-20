# -*- coding: utf-8 -*-
'''DelogX.utils.i18n

Utils about i18n, an i18n manager.
'''
from __future__ import unicode_literals

import os
from string import Formatter

from DelogX.entity.config import Config
from DelogX.utils.compat import Compat


class I18nFormatter(Formatter):
    '''Formatter which added default value support.'''

    def __init__(self, default=''):
        self.default = default

    def get_value(self, key, args, kwargs):
        default = self.default
        if Compat.version() == 2:
            if isinstance(key, int) or isinstance(key, long):
                return args[key] if -len(args) <= key < len(args) else default
            elif isinstance(key, str) or isinstance(key, unicode):
                return kwargs.get(key, self.default)
            else:
                super(I18nFormatter, self).get_value(key, args, kwargs)
        else:
            if isinstance(key, int):
                return args[key] if -len(args) <= key < len(args) else default
            elif isinstance(key, str):
                return kwargs.get(key, self.default)
            else:
                super(I18nFormatter, self).get_value(key, args, kwargs)


class I18n(object):
    '''I18n manager of DelogX.

    Attributes:

        directory (str): Name of the i18n directory.
        locale (str): Current locale.
        data (Config): Message data of the current locale.
    '''
    directory = None
    locale = None
    data = None

    def __init__(self, directory, locale):
        '''Initialize i18n manager.

        Args:

            directory (str): Name of the i18n directory.
            locale (str): Current locale.
        '''
        self.directory = directory
        self.locale = locale
        self.data = Config(os.path.join(directory, locale, 'locale.json'))

    def get(self, key, *args):
        '''Return a message by a message key.

        If no such message, return the key.

        Args:

            key (str): Message key.
            *args: Format substitutions.

        Returns:

            str: Formatted message.
        '''
        fmt = I18nFormatter()
        data = self.data
        local_key = data.get(key) if data.get(key) is not None else key
        try:
            return fmt.format(local_key, *args)
        except (KeyError, IndexError, ValueError):
            return local_key

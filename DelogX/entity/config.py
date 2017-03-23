# -*- coding: utf-8 -*-
'''DelogX.entity.config

Class to load, save and modify json config files.
'''
from __future__ import unicode_literals

import codecs
import errno
import json
import os

from collections import OrderedDict


class Config(object):
    '''Config manager of DelogX.

    Attributes:

        configfile (str): Name of the config file.
        config (object): Config data object.
    '''
    configfile = None
    config = None

    def __init__(self, filename=None):
        '''Initialize config manager.

        Args:

            filename (str, optional): Name of the config file.
        '''
        if filename is None:
            self.config = OrderedDict()
        else:
            self.configfile = filename
            if not self.load():
                self.config = OrderedDict()

    def __str__(self):
        try:
            return json.dumps(self.config, indent=4)
        except TypeError:
            return None

    def load(self, loadfrom=None):
        '''Load data from a json file.

        Args:

            loadfrom (str): If set, load from this file.

        Returns:

            bool: Whether load successful.
        '''
        if loadfrom is None:
            loadfrom = self.configfile
        if loadfrom is None or not os.path.isfile(loadfrom):
            return False
        with codecs.open(loadfrom, encoding='utf-8') as load_file:
            lines = load_file.readlines()
        if not lines:
            return False
        try:
            content = ''.join(lines)
            self.config = json.loads(content, object_pairs_hook=OrderedDict)
            return True
        except ValueError:
            return False

    def save(self, saveto=None):
        '''Save data to a json file.

        Args:

            saveto (str): If set, save to this file.

        Returns:

            bool: Whether save successful.
        '''
        if saveto is None:
            saveto = self.configfile
        if saveto is None:
            return False
        try:
            content = json.dumps(self.config, indent=4, separators=(',', ': '))
        except TypeError:
            return False
        saveto_dir = os.path.dirname(saveto)
        if saveto_dir and not os.path.exists(saveto_dir):
            try:
                os.makedirs(saveto_dir)
            except OSError as exception:
                if (exception.errno != errno.EEXIST or
                        not os.path.isdir(saveto_dir)):
                    return False
        with codecs.open(saveto, 'w', encoding='utf-8') as save_file:
            try:
                save_file.write(content)
                return True
            except IOError:
                return False

    def let(self, key, value):
        '''Set the data of a config entry.

        Args:

            key (str): Key of the entry.
            value (object): Value needs to set.

        Returns:

            object: If set successful return the value.
        '''
        return self._let_config(self.config, key, value)

    def get(self, key, default=None):
        '''Get the value of a config entry.

        Args:

            key (str): Key of the entry.
            default (object, optional): Return default value if no such entry.

        Returns:

            object: Value of the entry.
        '''
        value = self._get_config(self.config, key)
        return value if value is not None else default

    def delete(self, key):
        '''Delete the data of a config entry.

        Args:

            key (str): Key of the entry.

        Returns:

            object: If delete successful return the value of the entry.
        '''
        return self._delete_config(self.config, key)

    def _let_config(self, item, key, value):
        if not isinstance(item, OrderedDict):
            return None
        if '.' in key:
            k, rest = key.split('.', 1)
            if k not in item:
                item[k] = OrderedDict()
            return self._let_config(item[k], rest, value)
        else:
            item[key] = value
            return value

    def _get_config(self, item, key):
        if not isinstance(item, OrderedDict):
            return None
        if '.' in key:
            k, rest = key.split('.', 1)
            if k not in item:
                return None
            else:
                return self._get_config(item[k], rest)
        else:
            if key in item:
                return item[key]
            else:
                return None

    def _delete_config(self, item, key):
        if not isinstance(item, OrderedDict):
            return None
        if '.' in key:
            k, rest = key.split('.', 1)
            if k not in item:
                return None
            else:
                return self._delete_config(item[k], rest)
        else:
            if key in item:
                return item.pop(key, None)
            else:
                return None

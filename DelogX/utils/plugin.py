# -*- coding: utf-8 -*-
'''DelogX.utils.plugin

Base class of any plugin and a plugin manager.
'''
from __future__ import unicode_literals

import errno
import importlib
import os
import re
import sys

from DelogX.entity.config import Config


class Plugin(object):
    '''Base class and interface of any DelogX plugin.

    Attributes:

        app (DelogX): DelogX object.
        manager (PluginManager): PluginManager object of DelogX.
        name (str): Name of this plugin and its directory.
        workspace (str): Path of the directory of this plugin.
    '''
    app = None
    manager = None
    name = 'Plugin'
    workspace = None

    def __init__(self, app):
        '''Iniitialize plugin.

        Args:

            app (DelogX): DelogX object.
        '''
        self.app = app
        self.manager = app.plugin_manager

    def run(self):
        '''Method to call when this plugin is enabled.'''
        pass

    def version(self):
        '''Get the version of plugin itself.

        This is a example to show how to get the meta of plugin itself.

        Returns:

            str: Version of this plugin.
        '''
        info = self.manager.plugins.get(self.name)
        if info and info.get('version'):
            return info.get('version')
        return ''


class PluginManager(object):
    '''Plugin manager of DelogX.

    Attributes:

        directory (str): Absolute path of the plugin directory.
        plugins (dict): Loaded plugins.
        filters (dict): Registered filter hooks.
        actions (dict): Registered action hooks.

    Formats:

        plugins: {
            'plugin_name': {
                'entry': entry,
                'author': author,
                'version': version,
                'description': description
            },
            ...
        }

        filters: {
            'hook_name': [
                (func, priority),
                ...
            ],
            ...
        }

        actions: {
            'hook_name': [
                (func, priority),
                ...
            ],
            ...
        }
    '''
    directory = None
    plugins = None
    filters = None
    actions = None

    def __init__(self, app, directory):
        '''Initialize plugin manager.

        Args:

            app (DelogX): DelogX object.
            directory (str): Name of the plugins directory.
        '''
        self.app = app
        self.plugins = dict()
        self.filters = dict()
        self.actions = dict()
        self.directory = directory
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as exception:
                if (exception.errno != errno.EEXIST or
                        not os.path.isdir(directory)):
                    raise exception
        init_py = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_py):
            open(init_py, 'a').close()
        sys.path.append(directory)

    def load_all(self):
        '''Load all plugins in the plugin directory.'''
        plugin_list = os.listdir(self.directory)
        for plugin in plugin_list:
            self.load(plugin)

    def enable_all(self):
        '''Enable allloaded plugins.'''
        for plugin in self.plugins:
            self.enable(plugin)

    def load(self, plugin_name):
        '''Load a plugin by name.

        Args:

            plugin_name (str): Name of the plugin.

        Returns:

            object: Entry object of the plugin.
        '''
        plugin_dir = os.path.join(self.directory, plugin_name)
        plugin_meta = os.path.join(plugin_dir, 'plugin.json')
        name_re = re.compile(r'^[A-Za-z_][0-9A-Za-z_]*$')
        if (not os.path.isfile(plugin_meta) or
                name_re.match(plugin_name) is None):
            return None
        init_py = os.path.join(plugin_dir, '__init__.py')
        if not os.path.exists(init_py):
            open(init_py, 'a').close()
        meta = Config(plugin_meta)
        entry_name = meta.get('entry').strip(". \n\r\t")
        author = meta.get('author', '')
        version = meta.get('version', '')
        description = meta.get('description', '')
        if not entry_name or plugin_name in self.plugins:
            return None
        module_name = [plugin_name]
        module_name.extend(entry_name.split('.')[:-1])
        module_name = '.'.join(module_name)
        class_name = ''.join(entry_name.split('.')[-1:])
        module = importlib.import_module(module_name)
        entry = getattr(module, class_name)(self.app)
        entry.name = plugin_name
        entry.workspace = plugin_dir
        self.plugins[plugin_name] = {
            'entry': entry,
            'author': author,
            'version': version,
            'description': description
        }
        return entry

    def enable(self, plugin_name):
        '''Call `run()` method of the plugin entry object.'''
        if plugin_name in self.plugins:
            self.plugins[plugin_name]['entry'].run()

    def add_filter(self, hook_name, func, priority=10):
        '''Register a filter function on a hook.

        Args:

            hook_name (str): Name of the hook registered on.
            func (function): Function needs to register.
            priority (int): Priority of the function on the hook, defaults 10.
        '''
        if not isinstance(self.filters.get(hook_name), list):
            self.filters[hook_name] = list()
        self.filters[hook_name].append((func, priority))
        self.filters[hook_name] = sorted(
            self.filters[hook_name], key=lambda x: x[1])

    def add_action(self, hook_name, func, priority=10):
        '''Register an action function on a hook.

        Args:

            hook_name (str): Name of the hook registered on.
            func (function): Function needs to register.
            priority (int): Priority of the function on the hook, defaults 10.
        '''
        if not isinstance(self.actions.get(hook_name), list):
            self.actions[hook_name] = list()
        self.actions[hook_name].append((func, priority))
        self.actions[hook_name] = sorted(
            self.actions[hook_name], key=lambda x: x[1])

    def do_filter(self, hook_name, item):
        '''Call a filter hook to filter an object.

        Args:

            hook_name (str): Name of the hook to call.
            item (object): Object to be filtered.

        Returns:

            object: Filtered object.
        '''
        if hook_name not in self.filters:
            return item
        for hook in self.filters[hook_name]:
            item = hook[0](item)
        return item

    def do_action(self, hook_name, *args, **kwargs):
        '''Call an action hook to do an action.

        Args:

            hook_name (str): Name of the hook to call.
            *args: Parameters.
            **kwargs: Keyword parameters.
        '''
        if hook_name not in self.actions:
            return
        for hook in self.actions[hook_name]:
            hook[0](*args, **kwargs)

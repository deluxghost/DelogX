# -*- coding: utf-8 -*-
'''DelogX.utils.watch

The watchdog handler of DelogX bundles.
'''
from __future__ import unicode_literals

import os

from watchdog.events import PatternMatchingEventHandler


class Watch(PatternMatchingEventHandler):
    '''Event handler to watch file changing event in some directory.

    Attributes:

        bundle (Bundle): Bundle object relates to the watched directory.
    '''
    bundle = None

    def __init__(self, app, bundle, patterns, is_page=False):
        '''Initialize changing event handler.

        Args:

            app (DelogX): DelogX object.
            bundle (Bundle): Bundle object relates to the watched directory.
            patterns (list of str): Patterns to allow matching event paths.
            is_page (bool): Whether the bundle is a PageBundle.
        '''
        super(Watch, self).__init__(
            patterns=patterns, ignore_directories=True)
        self.app = app
        self.bundle = bundle
        self.is_page = is_page

    def on_created(self, event):
        self.do_update(os.path.split(event.src_path)[1])

    def on_deleted(self, event):
        self.do_remove(os.path.split(event.src_path)[1])

    def on_modified(self, event):
        self.do_update(os.path.split(event.src_path)[1])

    def on_moved(self, event):
        self.do_remove(os.path.split(event.src_path)[1])
        self.do_update(os.path.split(event.dest_path)[1])

    def do_update(self, filename):
        '''Update or Add a file to bundle.

        If the bundle is a PageBundle, update the header.

        Args:

            filename (str): Name of the file.
        '''
        self.bundle.update(filename)
        if self.is_page:
            self.app.update_header()

    def do_remove(self, filename):
        '''Remove a file in bundle.

        If the bundle is a PageBundle, update the header.

        Args:

            filename (str): Name of the file.
        '''
        self.bundle.remove(filename)
        if self.is_page:
            self.app.update_header()

# -*- coding: utf-8 -*-
'''DelogX.entity.bundle

Define class and interface of a bundle.

A bundle is a set of items.
'''
from __future__ import unicode_literals

import errno
import os
from collections import OrderedDict

from DelogX.entity.item import Post, Page
from DelogX.utils.compat import Compat
from DelogX.utils.path import Path


class Bundle(object):
    '''Base class of bundles.

    Attributes:

        bundle_list (list of Item): List of items in a bundle.
    '''
    bundle_list = None

    def __str__(self):
        return '{0}({1})'.format(
            self.__class__.__name__, repr(list(self.bundle_list.keys())))

    def sort(self):
        '''Sort the list of the bundle.'''
        pass

    def get(self, url):
        '''Return an item by its name(url).

        Args:

            url (str): Name or URL of the item.
        '''
        pass

    def get_list(self):
        '''Return a list of multiple items.'''
        pass


class DelogXBundle(Bundle):
    '''Base class of DelogX bundles.

    Attributes:

        directory (str): Absolute path of the bundle directory.
    '''
    directory = None

    def __init__(self, app, app_path, directory):
        '''Initialize a DelogX bundle.

        Args:

            app (DelogX): DelogX object.
            app_path (str): Absolute path of the blog application.
            directory (str): Name of items directory.
        '''
        self.app = app
        self.bundle_list = OrderedDict()
        self.directory = Path.abs_path(app_path, directory)
        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
            except OSError as exception:
                if (exception.errno != errno.EEXIST or
                        not os.path.isdir(self.directory)):
                    raise exception
        for filename in os.listdir(self.directory):
            real_path = os.path.join(self.directory, filename)
            if (os.path.isfile(real_path) and
                    os.path.splitext(filename)[1] == '.md'):
                self.update(filename)
        self.sort()

    def update(self, filename):
        '''Update an item in DelogX bundle.

        Args:

            filename (str): Name of the file needs to be updated.
        '''
        pass

    def remove(self, filename):
        '''Remove an item in DelogX bundle.

        Args:

            filename (str): Name of the file needs to be removed.

        Returns:

            bool: Whether the file is removed successfully.
        '''
        if filename in self.bundle_list:
            self.bundle_list.pop(filename)
            return True
        return False

    def sort(self):
        '''Sort the list of the DelogX bundle.'''
        pass

    def get(self, url):
        '''Return an item by its name(url).

        If cannot find item, try to return a hidden item have the same name.

        Args:

            url (str): Name or URL of the item.

        Returns:

            Item: Item found.
        '''
        finder = list()
        finder_hidden = list()
        for item in self.bundle_list.values():
            if item.url != url:
                continue
            if item.hidden:
                finder_hidden.append(item)
            else:
                finder.append(item)
        if finder:
            return finder[0]
        elif finder_hidden:
            return finder_hidden[0]
        else:
            return None

    def get_list(self):
        '''Return a list of multiple items.

        Returns:

            list of Item: List of these items.
        '''
        return list(self.bundle_list.values())


class PostBundle(DelogXBundle):
    '''A set of posts.

    Attributes:

        list_size (int): Count of posts per page .
    '''
    list_size = 10

    def __init__(self, app, app_path, post_dir, list_size=10):
        '''Initialize a post bundle.

        Args:

            app (DelogX): DelogX object.
            app_path (str): Absolute path of the blog application.
            post_dir (str): Name of posts directory.
            list_size (int): Count of posts per page, defaults 10.
        '''
        self.list_size = list_size
        super(PostBundle, self).__init__(app, app_path, post_dir)

    def update(self, filename):
        '''Update an post in bundle.

        Args:

            filename (str): Name of the file needs to be updated.

        Returns:

            bool: Whether the file is updated successfully.
        '''
        post = Post(self.app, filename, self.directory)
        if post.valid():
            self.bundle_list[filename] = post
            self.sort()
            return True
        return False

    def sort(self):
        '''Sort the list of the post bundle by modification time reversed.'''
        self.bundle_list = OrderedDict(sorted(
            self.bundle_list.items(), key=lambda x: x[1].time, reverse=True))

    def get_list_count(self, post_count=None, list_size=None):
        '''Return the count of posts list.

        Args:

            post_count (int): If set, use it as customize count of posts.
            list_size (int): If set, use it as customize size of list.

        Returns:

            int: Count of posts list.
        '''
        if list_size is None:
            list_size = self.list_size
        import math
        if post_count is None:
            post_count = len([
                post for post in self.bundle_list.values() if not post.hidden
            ])
        return int(math.ceil(float(post_count) / float(list_size)))

    def get_list(self, number=0, list_size=None):
        '''Return a list of multiple posts.

        If param number is 0, return the entire bundle.

        Args:

            number (int): Page number of the list, defaults 0.
            list_size (int): If set, use it as customize size of list.

        Returns:

            list of Post: List of these posts.
        '''
        if list_size is None:
            list_size = self.list_size
        if number:
            post_list = [
                post for post in self.bundle_list.values() if not post.hidden
            ]
            list_count = self.get_list_count(len(post_list), list_size)
            if not 0 < number <= list_count:
                return None
            if post_list and list_count > 0:
                post_list = post_list[
                    list_size * (number - 1):list_size * number
                ]
                return post_list
            else:
                return list()
        else:
            return super(PostBundle, self).get_list()


class PageBundle(DelogXBundle):
    '''A set of pages.'''

    def update(self, filename):
        '''Update an page in bundle.

        Args:

            filename (str): Name of the file needs to be updated.

        Returns:

            bool: Whether the file is updated successfully.
        '''
        page = Page(self.app, filename, self.directory)
        if page.valid():
            self.bundle_list[filename] = page
            self.sort()
            return True
        return False

    def sort(self):
        '''Sort the list of the page bundle by customize order.'''
        self.bundle_list = OrderedDict(sorted(
            self.bundle_list.items(), key=Compat.cmp_to_key()))

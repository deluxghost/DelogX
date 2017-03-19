# -*- coding: utf-8 -*-
'''DelogX.utils.path

Utils and functions about path.
'''
from __future__ import unicode_literals

import codecs
import os

from DelogX.utils.compat import Compat


class Path(object):
    '''Some useful path and URL utils and functions.'''

    @classmethod
    def format_url(cls, *args):
        '''Join strings to an URL and ensure the URL starts with a slash.

        Args:

            *args: strings need to be joined.

        Returns:

            str: Formatted URL.
        '''
        if Compat.sys() == 'Windows':
            return os.path.join('/', *args).replace('\\', '/')
        else:
            return os.path.join('/', *args)

    @classmethod
    def urlencode(cls, url):
        '''Return an encoded URL.

        Args:

            url (str): URL needs to be encoded.

        Returns:

            str: Encoded URL.
        '''
        if Compat.version() < 3:
            import urllib
        else:
            import urllib.parse as urllib
        return urllib.quote(Compat.unicode_convert(url))

    @classmethod
    def urldecode(cls, url):
        '''Return an decoded URL.

        Args:

            url (str): URL needs to be decoded.

        Returns:

            str: Decoded URL.
        '''
        if Compat.version() < 3:
            import urllib
        else:
            import urllib.parse as urllib
        return urllib.unquote(Compat.unicode_convert(url))

    @classmethod
    def abs_path(cls, prefix, path):
        '''If the path is not an absolute path, convert it to absolute.

        Args:

            prefix (str): Directory to be added if the path is not absolute.
            path (str): Path needs to check.

        Returns:

            str: Converted absolute path.
        '''
        if not os.path.isabs(path):
            path = os.path.join(prefix, path)
        return os.path.abspath(path)

    @classmethod
    def read_file(cls, filename):
        '''Read the content of a file (UTF-8).

        Args:

            filename (str): Name of the file.

        Returns:

            list of str: Content of the file.
        '''
        if not os.path.isfile(filename):
            return None
        with codecs.open(filename, encoding='utf-8') as some_file:
            lines = some_file.readlines()
        return lines

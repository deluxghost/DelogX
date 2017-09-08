# -*- coding: utf-8 -*-
'''DelogX.entity.item

Define class and interface of an item.

An item is a post or page.
'''
import os
import re

from DelogX.utils.parser import Markdown
from DelogX.utils.path import Path


class Item(object):
    '''Base class of items.

    Attributes:

        filename (str): Name of the item file.
        path (str): Absolute path of the item file.
        hidden (bool): Whether this item is hidden.
        markdown (str): Markdown content of this item.
        content (str): Parsed content of this item.
        url (str): Clean URL of this item.
        cooked_url (str): Encoded URL of this item.
        title (str): Title of this item.
        title_line (int): Start line number of content.
        plugin_manager (PluginManager): Plugin manager of DelogX.
    '''
    filename = None
    path = None
    hidden = False
    markdown = None
    content = None
    url = None
    title = None
    title_line = 0
    plugin_manager = None

    def __init__(self, blog, filename, path):
        '''Initialize and load an item.

        Args:

            blog (DelogX): DelogX object.
            filename (str): Name of this item file.
            path (str): Name of items directory.
        '''
        self.blog = blog
        self.filename = filename
        self.path = os.path.join(path, filename)
        self.plugin_manager = blog.plugin_manager
        self.update()

    def __str__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(self.filename))

    def update(self):
        '''Load the meta and content of this item.'''
        self.load_meta()
        self.load_content()

    def valid(self):
        '''Return whether this item exists and is valid.

        Returns:

            bool: Whether the item is valid.
        '''
        return self.filename is not None and os.path.isfile(self.path)

    def load_meta(self):
        '''Load the meta of this item, include `hidden`, `url` and `title`.'''
        if not self.valid():
            return
        self.hidden = self.filename.startswith('.')
        self.url = os.path.splitext(self.filename)[0]
        if self.hidden:
            self.url = self.url[1:]
        atx_re = re.compile(r'^\s*#\s*([^#]+)\s*#*\s*$')
        setext_re = re.compile(r'^\s*=+\s*$')
        lines = Path.read_file(self.path)
        first_line = Path.get_first_line(lines)
        line1 = lines[first_line] if first_line < len(lines) else ''
        line2 = lines[first_line + 1] if first_line + 1 < len(lines) else ''
        line1 = line1.strip('\n').strip('\r')
        line2 = line2.strip('\n').strip('\r')
        atx_match = atx_re.match(line1)
        setext_match = setext_re.match(line2)
        if atx_match and atx_match.group(1):
            self.title = atx_match.group(1)
            self.title_line = first_line + 1
        elif setext_match and line1.strip():
            self.title = line1
            self.title_line = first_line + 2
        else:
            self.title = self.url
            self.title_line = 0

    def load_content(self):
        '''Load and parse the content of this item.'''
        lines = Path.read_file(self.path)
        if lines is None:
            self.markdown = None
        lines = lines[self.title_line:]
        self.markdown = ''.join(lines)
        self.content = Markdown.markdown(self.markdown, self.blog.markdown_ext)


class Post(Item):
    '''A post.

    Attributes:

        time (float): Modification timestamp of this post.
        cooked_time (str): Formatted modification time.
    '''
    time = None

    def update(self):
        '''Load the meta and content of this post.'''
        super(Post, self).update()
        self.plugin_manager.do_action('dx_post_update', post=self)

    def load_meta(self):
        '''Load the meta of this post, include timestamp `time`.'''
        super(Post, self).load_meta()
        self.time = os.path.getmtime(self.path)


class Page(Item):
    '''A page.

    Attributes:

        sort (int): Customize sort order of this page.
    '''
    sort = None

    def update(self):
        '''Load the meta and content of this page.'''
        super(Page, self).update()
        self.plugin_manager.do_action('dx_page_update', page=self)

    def load_meta(self):
        '''Load the meta of this page, include sort order `sort`.'''
        super(Page, self).load_meta()
        sort_re = re.compile(r'^\.\d+$')
        match = sort_re.match(os.path.splitext(self.url)[1])
        if match:
            self.url = os.path.splitext(self.url)[0]
            if self.title_line == 0:
                self.title = self.url
            self.sort = int(match.group()[1:])

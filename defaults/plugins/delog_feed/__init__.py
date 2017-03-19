# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from flask import request
from werkzeug.contrib.atom import AtomFeed

from DelogX.entity.config import Config
from DelogX.utils.path import Path
from DelogX.utils.plugin import Plugin


class DelogFeed(Plugin):

    config = None
    feed_url = None
    feed_limit = 10

    def run(self):
        self.config = Config(os.path.join(self.workspace, 'config.json'))
        self.feed_url = self.config.get('delog_feed.url')
        self.feed_limit = self.config.get('delog_feed.limit')
        if not self.feed_url:
            self.feed_url = '/feed'
        if not self.feed_limit:
            self.feed_limit = 10
        self.feed_url = Path.format_url(self.feed_url)
        if not self.feed_url.endswith('/'):
            self.feed_url += '/'
        self.app.add_url_rule(self.feed_url, 'delog_feed', self.make_feed)
        self.manager.add_filter('dx_render', self.add_link)

    def add_link(self, render):
        site_name = self.app.default_conf('site.name')
        copy = render.lower()
        search = '<head>'
        tag = (
            '<link href="{href}" rel="alternate" '
            'title="{title}" type="application/atom+xml">').format(
                href=self.feed_url, title=site_name)
        try:
            index = copy.index(search) + len(search)
            render = render[:index] + tag + render[index:]
        except ValueError:
            render = render + tag
        return render

    def make_feed(self):
        site_name = self.app.default_conf('site.name')
        feed = AtomFeed(site_name, feed_url=request.url, url=request.url_root)
        posts = self.app.post_bundle.get_list(1, self.feed_limit)
        for post in posts:
            post = self.manager.do_filter('dx_post', post)
            ext_url = request.url_root
            if ext_url.endswith('/'):
                ext_url = ext_url[:-1]
            ext_url = ext_url + post.cooked_url
            update_time = datetime.datetime.fromtimestamp(post.time)
            feed.add(
                title=post.title, title_type='text',
                content=post.content, content_type='html',
                url=ext_url, author=site_name,
                updated=update_time, published=update_time)
        return feed.get_response()

# -*- coding: utf-8 -*-
import os

from DelogX.utils.config import Config
from DelogX.utils.path import Path
from DelogX.utils.plugin import Plugin


class DelogTags(Plugin):

    config = None
    tags_url = None

    def run(self):
        self.config = Config(os.path.join(self.workspace, 'config.json'))
        self.tags_url = self.config.get('delog_tags.url')
        if not self.tags_url:
            self.tags_url = '/tag'
        self.tags_url = Path.format_url(self.tags_url)
        tag_rule = Path.format_url(self.tags_url, '<tag_id>/')
        self.blog.add_url_rule(tag_rule, 'delog_tag', self.make_tag)
        self.manager.add_filter('dx_post', self.load_tags)

    def load_tags(self, post):
        # TODO
        if not post:
            return None
        post.tags = list()
        return post

    def make_tag(self, tag_id):
        # TODO
        pass

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
        tag_list_rule = Path.format_url(tag_rule, '<int:number>/')
        self.blog.add_url_rule(tag_rule, 'delog_tag', self.make_tag)
        self.blog.add_url_rule(
            tag_list_rule, 'delog_tag_list', self.make_tag_list)
        self.manager.add_action('dx_post_update', self.load_tags)

    def load_tags(self, *args, **kwargs):
        post = kwargs.get('post')
        if not post:
            return
        post.tags = list()
        title = post.title
        title_split = title.split('::', 1)
        if title_split:
            post.title = title_split[0].strip()
            tags = ''.join(title_split[1:]).split(',')
            post.tags = list(filter(None, list(map(str.strip, tags))))
            tags_link = list()
            tags_html = '<div class="post-tags">{0}</div>'
            for tag in post.tags:
                tags_link.append('<a href="{0}">{1}</a>'.format(
                    Path.format_url(self.tags_url, Path.urlencode(tag)), tag))
            if tags_link:
                tags_html = tags_html.format(' '.join(tags_link))
                post.content = tags_html + post.content

    def make_tag(self, tag_id):
        return self.make_tag_list(tag_id, 1)

    def make_tag_list(self, tag_id, number):
        # TODO
        pass

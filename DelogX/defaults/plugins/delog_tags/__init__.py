# -*- coding: utf-8 -*-
import math
import os

from flask import abort

from DelogX.utils.config import Config
from DelogX.utils.i18n import I18n
from DelogX.utils.path import Path
from DelogX.utils.plugin import Plugin


class DelogTags(Plugin):

    config = None
    tags_url = None
    i18n = None

    def run(self):
        conf = self.blog.default_conf
        self.config = Config(os.path.join(self.workspace, 'config.json'))
        self.i18n = I18n(
            Path.format_url(self.workspace, 'locale'), conf('local.locale'))
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
        title_split = list(filter(None, title.split('::', 1)))
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
        tag_id = Path.urldecode(tag_id)
        conf = self.blog.default_conf
        list_size = conf('local.list_size')
        bundle = self.blog.post_bundle.bundle_list
        tagged = [
            post for post in bundle.values()
            if not post.hidden and tag_id in post.tags
        ]
        list_count = int(math.ceil(float(len(tagged)) / float(list_size)))
        if not 0 < number <= list_count:
            abort(404)
        if tagged is None or list_count < 1:
            abort(404)
        post_list = tagged[
            list_size * (number - 1):list_size * number
        ]
        for post in post_list:
            post = self.blog.plugin_manager.do_filter('dx_post', post)
        prev_page = next_page = True
        if number == 1:
            prev_page = False
        if number == list_count:
            next_page = False
        list_url = Path.format_url(self.tags_url, tag_id)
        url = list_url if list_url.endswith('/') else list_url + '/'
        web_title = self.i18n.get('{0} - Page {1}', tag_id, number)
        return self.blog.get_render(
            'list.html', posts=post_list,
            list_id=number, list_url=url,
            prev_page=prev_page, next_page=next_page,
            web_title=web_title)

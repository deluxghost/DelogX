# -*- coding: utf-8 -*-
import re

from DelogX.utils.i18n import I18n
from DelogX.utils.path import Path
from DelogX.utils.plugin import Plugin


class DelogReadMore(Plugin):

    i18n = None

    def run(self):
        conf = self.blog.default_conf
        self.i18n = I18n(
            Path.format_url(self.workspace, 'locale'), conf('local.locale'))
        self.manager.add_action('dx_post_update', self.parse_readmore)

    def parse_readmore(self, post):
        if not post:
            return
        content_split = re.split(r'<[Hh][Rr](?:\s+\/)?>', post.content, 1)
        if len(content_split) == 2:
            summary, more = content_split
        else:
            summary = content_split[0]
            more = ''
        post_url = self.blog.runtime.get('url_prefix.post')
        post_url = Path.format_url(post_url, Path.urlencode(post.url))
        content = '''{0}
        <div class="{1}"><a href="{2}">{3}</a></div>
        <div class="post-more">{4}</div>
        '''
        more_class = ['read-more']
        if not more:
            more_class.append('no-more-content')
        more_class = ' '.join(more_class)
        content = content.format(
            summary, more_class, post_url, self.i18n.get('Read More'), more)
        post.content = content

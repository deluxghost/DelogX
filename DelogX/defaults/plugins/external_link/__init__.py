# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from DelogX.utils.plugin import Plugin


class ExternalLink(Plugin):

    def run(self):
        self.manager.add_filter('dx_page', self.load_link)

    @classmethod
    def load_link(cls, page):
        if not page:
            return None
        link_re = re.compile(
            r'^(?:\<p\>)?\<a[^>]*\shref="([^"]*)"[^>]*\>([^<>]*)'
            r'\<\/a\>(?:\<\/p\>)?$',
            re.IGNORECASE)
        target_re = re.compile(r'target="([^"]*)"', re.IGNORECASE)
        content = page.content.replace('\n', ' ').strip()
        link_match = link_re.match(content)
        if link_match:
            page.link = link_match.group(1).strip()
            link_title = link_match.group(2).strip()
            page.title = link_title if link_title else page.title
            target_search = target_re.search(content)
            page.target = ''
            if target_search:
                page.target = target_search.group(1).replace('\n', '').strip()
            return None
        return page

# -*- coding: utf-8 -*-
from markdown.extensions import Extension

from DelogX.utils.plugin import Plugin


class ExternalLink(Plugin):

    def run(self):
        self.manager.add_filter('dx_page', self.load_link)
        self.blog.markdown_ext.append(DelExtension)


class DelExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        '''Add `<del>` tag support to markdown.'''
        from markdown.inlinepatterns import SimpleTagPattern
        md_del_re = r'(\~\~)(.+?)(\~\~)'
        md.inlinePatterns.add(
            'del', SimpleTagPattern(md_del_re, 'del'), '<not_strong')

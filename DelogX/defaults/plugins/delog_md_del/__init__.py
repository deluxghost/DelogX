# -*- coding: utf-8 -*-
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

from DelogX.utils.plugin import Plugin


class DelogMdDel(Plugin):

    def run(self):
        self.blog.markdown_ext.append(DelExtension())


class DelExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md_del_re = r'(\~\~)(.+?)(\~\~)'
        md.inlinePatterns.add(
            'del', SimpleTagPattern(md_del_re, 'del'), '<not_strong')

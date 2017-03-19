# -*- coding: utf-8 -*-
'''DelogX.utils.parser

Utils of markdown parser.
'''
from __future__ import unicode_literals

import markdown
from markdown.extensions import Extension


class Markdown(object):
    '''Include the markdown parser method.'''

    @classmethod
    def markdown(cls, text, exts=None):
        '''Parse markdown text to HTML5.

        Args:

            text (str): Raw markdown text.
            ext (list of str/class): Extensions of markdown module.

        Returns:

            str: Parsed HTML text.
        '''
        ext_list = [
            'markdown.extensions.attr_list',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            DelExtension()
        ]
        if exts and isinstance(exts, list):
            ext_list.extend(exts)
        elif exts:
            ext_list.append(exts)
        return markdown.markdown(
            text,
            output_format='html5',
            tab_length=4,
            extensions=ext_list
        )


class DelExtension(Extension):
    '''Extension to provide `<del>` tag support.'''

    def extendMarkdown(self, md, md_globals):
        '''Add `<del>` tag support to markdown.'''
        from markdown.inlinepatterns import SimpleTagPattern
        md_del_re = r'(\~\~)(.+?)(\~\~)'
        md.inlinePatterns.add(
            'del', SimpleTagPattern(md_del_re, 'del'), '<not_strong')

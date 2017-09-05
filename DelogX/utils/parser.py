# -*- coding: utf-8 -*-
'''DelogX.utils.parser

Utils of markdown parser.
'''
import markdown


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
            'markdown.extensions.fenced_code'
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

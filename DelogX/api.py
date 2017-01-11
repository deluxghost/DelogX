# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from DelogX.error import DelogXError

class DelogXAPI():

    global_posts = [] # format: [{'url': 'url', 'hidden': False, 'time': time, 'title': 'title'}, ...]
    global_pages = [] # format: [{'url': 'url', 'sort': 0, 'hidden': False, 'title': 'title'}, ...]
    
    _post_dir = './posts/'
    _page_dir = './pages/'
    _post_url = '/posts/'
    _page_url = '/pages/'
    _page_size = 10

    def __init__(self, site_info=None):
        if site_info:
            self._post_dir = site_info['POST_DIR']
            self._page_dir = site_info['PAGE_DIR']
            self._post_url = site_info['POST_URL']
            self._page_url = site_info['PAGE_URL']
            self._page_size = site_info['PAGE_SIZE']
            if self._page_size <= 0:
                self._page_size = 10
        self.update_list()

    def get_header(self):
        page_list = []
        for page in self.global_pages:
            if page['hidden']:
                continue
            else:
                page_info = {
                    'url': self._page_url + page['url'],
                    'title': page['title']
                }
                if not page['title']:
                    page_info['title'] = page['url']
                page_list.append(page_info)
        return page_list

    def get_post_list(self, page_number):
        import math
        if page_number < 1:
            return None, 0
        post_list = [post for post in self.global_posts if not post['hidden']]
        if post_list:
            max_page_number = int(math.ceil(float(len(post_list)) / float(self._page_size)))
            if page_number > max_page_number:
                return None, max_page_number
            post_list = post_list[self._page_size*(page_number-1):self._page_size*page_number]
            post_list = [self.get_post(post['url']) for post in post_list]
            return post_list, max_page_number
        else:
            if page_number == 1:
                return [], 1
            else:
                return None, 1
        

    def get_post(self, post_url):
        finder = [post for post in self.global_posts if post['url'] == post_url]
        if finder:
            post = finder[0]
            post_filename = post['url']
            if post['hidden']:
                post_filename = '.' + post_filename
            post_filename = os.path.join(self._post_dir, post_filename + '.md')
            post_info = {
                'url': self._post_url + post['url'],
                'title': post['title'],
                'time': post['time'],
                'content': self._get_file(post_filename, post['title'])
            }
            if not post['title']:
                post_info['title'] = post['url']
            if post_info['content'] is None:
                return None
            return post_info
        else:
            return None

    def get_page(self, page_url):
        finder = [page for page in self.global_pages if page['url'] == page_url]
        if finder:
            page = finder[0]
            page_filename = page['url']
            if page['hidden']:
                page_filename = '.' + page_filename
            if page['sort'] is not None:
                page_filename += '.' + str(page['sort'])
            page_filename = os.path.join(self._page_dir, page_filename + '.md')
            page_info = {
                'url': self._page_url + page['url'],
                'title': page['title'],
                'content': self._get_file(page_filename, page['title'])
            }
            if not page['title']:
                page_info['title'] = page['url']
            if page_info['content'] is None:
                return None
            return page_info
        else:
            return None
    
    def _get_file(self, filename, title=None):
        import codecs
        error = False
        if os.path.isfile(filename):
            f = codecs.open(filename, encoding='utf-8')
            try:
                lines = f.readlines()
                if title and title.endswith('\n'):
                    lines = lines[2:]
                elif title:
                    lines = lines[1:]
            except:
                lines = []
                error = True
            finally:
                f.close()
            if error:
                return None
            else:
                return self.markdown_parser(''.join(lines))
        else:
            return None

    def get_post_title(self, filename):
        return self._get_title(os.path.join(self._post_dir, filename))
    
    def get_page_title(self, filename):
        return self._get_title(os.path.join(self._page_dir, filename))

    def _get_title(self, filename):
        import re, codecs
        if os.path.isfile(filename):
            pattern1 = re.compile(r'^\s*#\s*([^#]+)\s*#*\s*$')
            pattern2 = re.compile(r'^\s*=+\s*$')
            f = codecs.open(filename, encoding='utf-8')
            try:
                line1 = f.readline().strip('\n').strip('\r')
                line2 = f.readline().strip('\n').strip('\r')
            except:
                line1 = ''
                line2 = ''
            finally:
                f.close()
            match1 = pattern1.match(line1)
            if match1 and match1.group(1):
                return match1.group(1)
            else:
                match2 = pattern2.match(line2)
                if match2 and line1.strip():
                    return line1 + '\n'
                return None
        else:
            return None

    def update_list(self):
        self._update_post_list()
        self._update_page_list()

    def _update_post_list(self):
        del self.global_posts[:]
        if not os.path.exists(self._post_dir):
            raise DelogXError(self._post_dir + ' Not Found')
        def _get_sort_key(post):
            return post['time']
        for filename in os.listdir(self._post_dir):
            if os.path.isfile(os.path.join(self._post_dir, filename)) and os.path.splitext(filename)[1] == '.md':
                post_meta = {
                    'url': os.path.splitext(filename)[0],
                    'title': self.get_post_title(filename),
                    'time': os.path.getmtime(os.path.join(self._post_dir, filename)),
                    'hidden': False
                }
                if filename.startswith('.'):
                    post_meta['url'] = post_meta['url'][1:]
                    post_meta['hidden'] = True
                self.global_posts.append(post_meta)
            else:
                continue
        self.global_posts = sorted(self.global_posts, key=_get_sort_key, reverse=True)

    def _update_page_list(self):
        import re
        pattern = re.compile(r'^\.\d+$')
        del self.global_pages[:]
        if not os.path.exists(self._page_dir):
            raise DelogXError(self._page_dir + ' Not Found')
        def _sort_compare(a, b):
            a_sort = a['sort']
            b_sort = b['sort']
            if a_sort is not None and b_sort is not None:
                if a_sort == b_sort:
                    return 0
                elif a_sort > b_sort:
                    return 1
                else:
                    return -1
            else:
                if a_sort is None and not b_sort is None:
                    return 0
                elif a_sort is None:
                    return 1
                else:
                    return -1
        def _cmp_to_key(orig_cmp):
            class C(object):
                def __init__(self, obj, *args):
                    self.obj = obj
                def __lt__(self, other):
                    return orig_cmp(self.obj, other.obj) < 0
                def __gt__(self, other):
                    return orig_cmp(self.obj, other.obj) > 0
                def __eq__(self, other):
                    return orig_cmp(self.obj, other.obj) == 0
                def __le__(self, other):
                    return orig_cmp(self.obj, other.obj) <= 0  
                def __ge__(self, other):
                    return orig_cmp(self.obj, other.obj) >= 0
                def __ne__(self, other):
                    return orig_cmp(self.obj, other.obj) != 0
            return C
        for filename in os.listdir(self._page_dir):
            if os.path.isfile(os.path.join(self._page_dir, filename)) and os.path.splitext(filename)[1] == '.md':
                page_meta = {
                    'url': os.path.splitext(filename)[0],
                    'title': self.get_page_title(filename),
                    'sort': None,
                    'hidden': False
                }
                if filename.startswith('.'):
                    page_meta['url'] = page_meta['url'][1:]
                    page_meta['hidden'] = True
                match = pattern.match(os.path.splitext(page_meta['url'])[1])
                if match:
                    page_meta['url'] = os.path.splitext(page_meta['url'])[0]
                    page_meta['sort'] = int(match.group()[1:])
                self.global_pages.append(page_meta)
            else:
                continue
        self.global_pages = sorted(self.global_pages, key=_cmp_to_key(_sort_compare))
    
    def unicode_convert(self, uni, tobyte=True):
        import sys
        if sys.version_info.major < 3:
            if tobyte:
                return uni.encode('utf-8')
            else:
                return uni.decode('utf-8')                
        return uni
    
    def markdown_parser(self, input_md):
        try:
            import markdown
        except ImportError:
            raise DelogXError('Import markdown Failed')
        from markdown.extensions.headerid import HeaderIdExtension
        #from markdown.extensions.fenced_code import FencedCodeExtension, FencedBlockPreprocessor
        #class CodeExt(FencedCodeExtension):
            #def extendMarkdown(self, md, md_globals):
                #md.registerExtension(self)
                #md.preprocessors.add('fenced_code_block', CodeExtPreprocesser(md), ">normalize_whitespace")
        #class CodeExtPreprocesser(FencedBlockPreprocessor):
            #LANG_TAG = ' class="language-%s"'
        class DelExtension(markdown.extensions.Extension):
            def extendMarkdown(self, md, md_globals):
                from markdown.inlinepatterns import SimpleTagPattern
                DEL_RE = r"(\~\~)(.+?)(\~\~)"
                md.inlinePatterns.add('del', SimpleTagPattern(DEL_RE, 'del'), '<not_strong')
        return markdown.markdown(input_md,
            output_format='html5',
            tab_length=4,
            extensions=[
                'markdown.extensions.attr_list',
                'markdown.extensions.tables',
                HeaderIdExtension(forceid=False),
                'markdown.extensions.fenced_code',
                DelExtension()
            ])

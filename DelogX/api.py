# -*- coding: utf-8 -*-
from DelogX.error import DelogXError

class DelogXAPI():

    global_posts = []
    global_pages = []
    
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
            post_filename = self._post_dir + post_filename + '.md'
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
            page_filename = self._page_dir + page_filename + '.md'
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
        import os
        error = False
        if os.path.isfile(filename):
            f = open(filename)
            try:
                lines = f.readlines()
                if title:
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
        return self._get_title(self._post_dir + filename)
    
    def get_page_title(self, filename):
        return self._get_title(self._page_dir + filename)

    def _get_title(self, filename):
        import os
        import re
        if os.path.isfile(filename):
            pattern = re.compile(r'^#\s*([^#]+)$')
            f = open(filename)
            try:
                line = f.readline().strip('\n')
            except:
                line = ''
            finally:
                f.close()
            match = pattern.match(line)
            if match and match.group(1):
                return match.group(1)
            else:
                return None
        else:
            return None

    def update_list(self):
        self._update_post_list()
        self._update_page_list()

    def _update_post_list(self):
        import os
        del self.global_posts[:]
        if not os.path.exists(self._post_dir):
            raise DelogXError(self._post_url + ' Not Found')
        def _get_sort_key(post):
            return post['time']
        for filename in os.listdir(self._post_dir):
            if os.path.isfile(self._post_dir + filename) and os.path.splitext(filename)[1] == '.md':
                post_meta = {
                    'url': os.path.splitext(filename)[0],
                    'title': self.get_post_title(filename),
                    'time': os.path.getmtime(self._post_dir + filename),
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
        import os
        import re
        pattern = re.compile(r'^\.\d+$')
        del self.global_pages[:]
        if not os.path.exists(self._page_dir):
            raise DelogXError(self._page_url + ' Not Found')
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
        for filename in os.listdir(self._page_dir):
            if os.path.isfile(self._page_dir + filename) and os.path.splitext(filename)[1] == '.md':
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
        self.global_pages = sorted(self.global_pages, cmp=_sort_compare)
    
    def markdown_parser(self, input_md):
        try:
            import markdown
            from markdown.extensions.headerid import HeaderIdExtension
        except ImportError:
            raise DelogXError('Import markdown Failed')
        return markdown.markdown(input_md.decode('utf-8'),
            output_format='html5',
            extensions=[
                'markdown.extensions.attr_list',
                'markdown.extensions.tables',
                HeaderIdExtension(forceid=False)
            ]).encode('utf-8')
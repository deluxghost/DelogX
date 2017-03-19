# -*- coding: utf-8 -*-
'''The class, definition and interface of DelogX.'''
from __future__ import unicode_literals

import os
import time

from flask import render_template, abort, send_from_directory
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from DelogX.entity.bundle import PostBundle, PageBundle
from DelogX.entity.config import Config
from DelogX.utils.compat import Compat
from DelogX.utils.i18n import I18n
from DelogX.utils.path import Path
from DelogX.utils.plugin import PluginManager
from DelogX.utils.watch import Watch


class DelogX(object):
    '''The entry and interface of DelogX.

    Attributes:

        framework (Flask): Flask application object.
        config (Config): Config manager of DelogX.
        runtime (Config): Runtime config manager of DelogX.
        header (list of Page): Pages shown in navbar.
        post_bundle (Bundle): Item bundle of DelogX posts.
        page_bundle (Bundle): Item bundle of DelogX pages.
        observer (Observer): Observer of watchdog module.
        i18n (I18n): I18n manager of DelogX.
        markdown_ext (list of str/class): Extensions of markdown module.
        plugin_manager (PluginManager): Plugin manager of DelogX.
    '''

    def __init__(self, app_path, framework, config='config.json'):
        '''Initialize DelogX object.

        Args:

            app_path (str): Absolute path of the blog application.
            framework (Flask): Flask application object.
            config (str): Config file of DelogX, defaults `config.json`.
        '''
        self.framework = framework
        app_path = os.path.realpath(app_path)
        config = Path.abs_path(app_path, config)
        config = Config(config)
        runtime = Config()
        module_path = os.path.dirname(os.path.realpath(__file__))
        runtime.let('path.app', app_path)
        runtime.let('path.module', module_path)
        self.config = config
        self.runtime = runtime
        self.markdown_ext = list()
        self.init_runtime()
        self.init_route()
        self.init_plugins()
        self.update_header()

    def init_runtime(self):
        '''Initialize runtime environments of DelogX.'''
        conf = self.default_conf
        runtime = self.runtime
        app_path = runtime.get('path.app')
        module_path = runtime.get('path.module')
        init_path_list = [
            'directory.post',
            'directory.page',
            'directory.static',
            'directory.themes',
            'directory.plugins'
        ]
        init_url_list = [
            'url_prefix.post',
            'url_prefix.page',
            'url_prefix.static',
            'url_prefix.post_list'
        ]
        for key in init_path_list:
            runtime.let(key, Path.abs_path(app_path, conf(key)))
        for key in init_url_list:
            runtime.let(key, Path.format_url(conf(key)))
        post_dir = runtime.get('directory.post')
        page_dir = runtime.get('directory.page')
        themes_dir = runtime.get('directory.themes')
        theme = conf('local.theme')
        theme = 'default' if not theme else theme
        theme_path = os.path.join(themes_dir, theme)
        self.framework.template_folder = theme_path
        self.post_bundle = PostBundle(
            self, app_path, post_dir, conf('local.list_size'))
        self.page_bundle = PageBundle(self, app_path, page_dir)
        post_watch = Watch(self, self.post_bundle, ['*.md'])
        page_watch = Watch(self, self.page_bundle, ['*.md'], is_page=True)
        watch_polling = conf('local.watch_polling')
        watch_polling = True if Compat.is_wsl() else watch_polling
        self.observer = PollingObserver() if watch_polling else Observer()
        self.observer.setDaemon(True)
        self.observer.schedule(post_watch, post_dir)
        self.observer.schedule(page_watch, page_dir)
        self.observer.start()
        self.i18n = I18n(
            Path.format_url(module_path, 'locale'), conf('local.locale'))

    def init_route(self):
        '''Initialize URL routes of DelogX.'''
        runtime = self.runtime
        static_rule = Path.format_url(
            runtime.get('url_prefix.static'), '<static_file>')
        list_rule = Path.format_url(
            runtime.get('url_prefix.post_list'), '<int:number>/')
        item_rule = Path.format_url(
            runtime.get('url_prefix.page'), '<item_id>/')
        page_rule = Path.format_url(
            runtime.get('url_prefix.page'), '<page_id>/')
        post_rule = Path.format_url(
            runtime.get('url_prefix.post'), '<post_id>/')
        icon_rule = Path.format_url(
            runtime.get('url_prefix.static'), 'favicon.ico')
        self.add_url_rule('/', 'delogx_index', self.route_index)
        self.add_url_rule(static_rule, 'delogx_static', self.route_static)
        self.add_url_rule(list_rule, 'delogx_list', self.route_list)
        if runtime.get('url_prefix.post') == runtime.get('url_prefix.page'):
            self.add_url_rule(item_rule, 'delogx_page', self.route_item)
        else:
            self.add_url_rule(page_rule, 'delogx_page', self.route_page)
            self.add_url_rule(post_rule, 'delogx_post', self.route_post)
        self.framework.add_url_rule(
            '/favicon.ico', 'delogx_favicon', redirect_to=icon_rule)
        self.framework.errorhandler(404)(self.route_not_found)

    def init_plugins(self):
        '''Initialize plugin manager of DelogX.'''
        plugins_dir = self.runtime.get('directory.plugins')
        self.plugin_manager = PluginManager(self, plugins_dir)
        manager = self.plugin_manager
        manager.add_filter('dx_page', self.cook_page, 0)
        manager.add_filter('dx_post', self.cook_post, 0)
        manager.add_filter('dx_static', self.cook_static, 0)
        manager.load_all()
        manager.enable_all()

    def default_conf(self, key):
        '''Get a config with default value.

        Args:

            key (str): Key of the config entry.

        Returns:

            object: Value of the config entry.
        '''
        conf = self.config.get
        default_dict = {
            'site.name': 'DelogX',
            'site.subname': 'Yet another Markdown based blog',
            'local.theme': 'default',
            'local.locale': 'en_US',
            'local.list_size': 10,
            'local.watch_polling': False,
            'local.time_format': '%Y-%m-%d %H:%M',
            'url_prefix.post': '/post',
            'url_prefix.page': '/page',
            'url_prefix.post_list': '/list',
            'url_prefix.static': '/static',
            'directory.post': 'posts',
            'directory.page': 'pages',
            'directory.static': 'static',
            'directory.themes': 'themes',
            'directory.plugins': 'plugins',
            'static.css': [],
            'static.js': [],
            'debug.host': '0.0.0.0',
            'debug.port': 8000
        }
        return default_dict.get(key) if conf(key) is None else conf(key)

    def add_url_rule(self, rule, endpoint, func):
        '''Add an URL route rule to Flask object.

        Args:

            rule (str): URL rule string.
            endpoint (str): Endpoint for the registered URL rule.
            func (function): Function to call when request.
        '''
        self.framework.add_url_rule(rule, endpoint, func)

    def update_header(self):
        '''Reload pages shown in navbar.

        Hidden pages will be ignored.
        '''
        header = self.page_bundle.get_list()
        if header is None:
            header = list()
        for page in header:
            page = self.plugin_manager.do_filter('dx_page', page)
        self.plugin_manager.do_action('dx_header')
        self.header = self.plugin_manager.do_filter('dx_header', header)

    def get_render(self, template, **context):
        '''Return rendered HTML content.

        Args:

            template (str): Filename of the template.
            **context: Context of the template.

        Returns:

            str: rendered HTML.

        Contexts:

            app: DelogX itself.
            _g: Method to get i18n text.
            _c: Method to get config.
            _rt: Method to get runtime config.
            _css: CSS list of site.
            _js: JS list of site.
        '''
        conf = self.default_conf
        render = render_template(
            template,
            app=self,
            _g=self.i18n.get,
            _c=self.default_conf,
            _rt=self.runtime.get,
            _css=self.get_static(conf('static.css')),
            _js=self.get_static(conf('static.js')),
            **context)
        self.plugin_manager.do_action('dx_render')
        return self.plugin_manager.do_filter('dx_render', render)

    def get_page(self, page_id):
        '''Return cooked Page object by id.

        Args:

            page_id (str): Request ID of the page.

        Returns:

            Page: Cooked Page object.
        '''
        page_id = Path.urldecode(page_id)
        page = self.page_bundle.get(page_id)
        self.plugin_manager.do_action('dx_page')
        page = self.plugin_manager.do_filter('dx_page', page)
        return page

    def cook_page(self, page):
        '''Cook a Page.

        Add prefix to the URL of the Page.

        Args:

            page (Page): Page needs to cook.

        Returns:

            Page: Cooked Page.
        '''
        runtime = self.runtime.get
        if not page:
            return None
        page_url = runtime('url_prefix.page')
        page.cooked_url = Path.format_url(page_url, Path.urlencode(page.url))
        return page

    def get_post(self, post_id):
        '''Return cooked Post object by id.

        Args:

            post_id (str): Request ID of the post.

        Returns:

            Post: Cooked Post object.
        '''
        post_id = Path.urldecode(post_id)
        post = self.post_bundle.get(post_id)
        self.plugin_manager.do_action('dx_post')
        return self.plugin_manager.do_filter('dx_post', post)

    def cook_post(self, post):
        '''Cook a Post.

        Add prefix to the URL of the Post and convert timestamp to string.

        Args:

            post (Post): Post needs to cook.

        Returns:

            Post: Cooked Post.
        '''
        conf = self.config.get
        runtime = self.runtime.get
        if not post:
            return None
        post_url = runtime('url_prefix.post')
        time_format = conf('local.time_format')
        post.cooked_url = Path.format_url(post_url, Path.urlencode(post.url))
        post.cooked_time = time.strftime(
            Compat.unicode_convert(time_format),
            time.localtime(post.time))
        post.cooked_time = Compat.unicode_convert(
            post.cooked_time,
            to_byte=False)
        return post

    def get_static(self, statics):
        '''Return a list of static files.

        Args:

            statics (list of str): Static files.

        Returns:

            list: Cooked static files.
        '''
        self.plugin_manager.do_action('dx_static')
        return self.plugin_manager.do_filter('dx_static', statics)

    def cook_static(self, statics):
        '''Cook a list of static files.

        Convert all relative links to absolute.

        Args:

            statics (list of str): Static files.

        Returns:

            list: Cooked list of static files.
        '''
        runtime = self.runtime.get
        static_url = runtime('url_prefix.static')
        if not statics:
            statics = list()
        for i, link in enumerate(statics):
            if not link.startswith(('/', 'http://', 'https://')):
                statics[i] = Path.format_url(static_url, link)
        return statics

    def route_static(self, static_file):
        '''Response a static file.

        Search the file in static directory firstly, then search in
        theme directory.

        Args:

            static_file (str): Relative path of the static file.

        Returns:

            object: Static file.

        Abort:

            404: No such static file.
        '''
        static_dir = self.runtime.get('directory.static')
        themes_dir = self.framework.template_folder
        static_path = os.path.join(static_dir, static_file)
        themes_path = os.path.join(themes_dir, 'static', static_file)
        if os.path.isfile(static_path):
            return send_from_directory(
                os.path.dirname(static_path),
                os.path.basename(static_path))
        elif os.path.isfile(themes_path):
            return send_from_directory(
                os.path.dirname(themes_path),
                os.path.basename(themes_path))
        abort(404)

    def route_index(self):
        '''Response the home page.

        Home page, i.e. the first page of posts.

        Returns:

            str: Rendered HTML of the home page.
        '''
        return self.route_list(1)

    def route_list(self, number):
        '''Response a list of posts.

        Hidden posts will be ignored.

        Args:

            number (int): Page number of the list.

        Returns:

            str: Rendered HTML of the posts list.

        Abort:

            404: No such page of posts list.
        '''
        runtime = self.runtime.get
        post_count = self.post_bundle.get_list_count()
        post_list = self.post_bundle.get_list(number)
        if post_list is None:
            abort(404)
        for post in post_list:
            post = self.plugin_manager.do_filter('dx_post', post)
        prev_page = next_page = True
        if number == 1:
            prev_page = False
        if number == post_count:
            next_page = False
        list_url = Path.format_url(runtime('url_prefix.post_list'))
        url = list_url if list_url.endswith('/') else list_url + '/'
        return self.get_render(
            'list.html', posts=post_list,
            list_id=number, list_url=url,
            prev_page=prev_page, next_page=next_page)

    def route_page(self, page_id):
        '''Response a page.

        Args:

            page_id (str): Request ID of the page.

        Returns:

            str: Rendered HTML of the page.

        Abort:

            404: No such page.
        '''
        page = self.get_page(page_id)
        if page:
            return self.get_render('page.html', page=page)
        abort(404)

    def route_post(self, post_id):
        '''Response a post.

        Args:

            post_id (str): Request ID of the post.

        Returns:

            str: Rendered HTML of the post.

        Abort:

            404: No such post.
        '''
        post = self.get_post(post_id)
        if post:
            return self.get_render('post.html', post=post)
        abort(404)

    def route_item(self, item_id):
        '''Response a page or post.

        Args:

            item_id (str): Request ID of the item.

        Returns:

            str: Rendered HTML of item.

        Abort:

            404: No such item.
        '''
        page = self.get_page(item_id)
        post = self.get_post(item_id)
        if page:
            return self.get_render('page.html', page=page)
        elif post:
            return self.get_render('post.html', post=post)
        abort(404)

    def route_not_found(self, error):
        '''Response `404 Not Found` page.

        Args:

            error (object): Error code of the request.

        Returns:

            str: Rendered HTML of 404.
        '''
        return self.get_render('404.html'), error.code

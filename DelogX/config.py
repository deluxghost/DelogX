# -*- coding: utf-8 -*-

class DelogXConfig():
    site_info = {
        'SITE_NAME': 'DelogX',
        'SITE_SUBNAME': 'Another Markdown Blog, Written in Python',
        'CSS_LIST': [
            '/static/style.css',
            '/static/highlight.css'
        ],
        'JS_LIST': [
            '/static/highlight.js',
            '/static/highlight.init.js'
        ],
        'POST_DIR': '/path/to/your/blog/posts/',
        'PAGE_DIR': '/path/to/your/blog/pages/',
        'POST_URL': '/posts/',
        'PAGE_URL': '/pages/',
        'POST_LIST_URL': '/n/',
        'PAGE_SIZE': 10,
        'LOCALE': 'zh_Hans',
        'TIME_FORMAT': '%Y-%m-%d %H:%M'
    }
    app_info = {
        'HOST': '0.0.0.0',
        'PORT': 8000
    }

# -*- coding: utf-8 -*-
from DelogX.error import DelogXError

try:
    from watchdog.observers import Observer
except ImportError:
    raise DelogXError('Import watchdog Failed')
try:
    from flask import Flask
    from flask.ext.babel import Babel
except ImportError:
    raise DelogXError('Import Flask Failed')

from DelogX import config
from DelogX.api import DelogXAPI
from DelogX.watch import BlogHandler

observer = Observer()
observer.setDaemon(True)
observer.schedule(BlogHandler(patterns=['*.md']), config.site_info['POST_DIR'])
observer.schedule(BlogHandler(patterns=['*.md']), config.site_info['PAGE_DIR'])
observer.start()

app = Flask(__name__, static_url_path='/static')
babel = Babel(app)
api = DelogXAPI(config.site_info)

from DelogX import route

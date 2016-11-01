# -*- coding: utf-8 -*-
import os
from DelogX.error import DelogXError

try:
    from watchdog.observers import Observer
except ImportError:
    raise DelogXError('Import watchdog Failed')
try:
    from flask import Flask
    from flask_babel import Babel
except ImportError:
    raise DelogXError('Import Flask Failed')

from DelogX.config import DelogXConfig as config
from DelogX.api import DelogXAPI
from DelogX.watch import BlogHandler

if not os.path.exists(config.site_info['POST_DIR']):
    raise DelogXError(config.site_info['POST_DIR'] + ' Not Found')
if not os.path.exists(config.site_info['PAGE_DIR']):
    raise DelogXError(config.site_info['PAGE_DIR'] + ' Not Found')

observer = Observer()
observer.setDaemon(True)
observer.schedule(BlogHandler(patterns=['*.md']), config.site_info['POST_DIR'])
observer.schedule(BlogHandler(patterns=['*.md']), config.site_info['PAGE_DIR'])
observer.start()

app = Flask(__name__, static_url_path='/static')
babel = Babel(app)
api = DelogXAPI(config.site_info)

from DelogX import route

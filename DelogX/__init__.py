# -*- coding: utf-8 -*-
from DelogX.error import DelogXError

try:
    import pyinotify
except ImportError:
    raise DelogXError('Import pyinotify Failed')
try:
    from flask import Flask
    from flask.ext.babel import Babel
except ImportError:
    raise DelogXError('Import Flask Failed')

from DelogX import config
from DelogX.api import DelogXAPI
from DelogX.inotify import FileEventHandler

wm = pyinotify.WatchManager()
mask = pyinotify.ALL_EVENTS
notifier = pyinotify.ThreadedNotifier(wm, FileEventHandler())
notifier.setDaemon(True)
wm.add_watch(config.site_info['POST_DIR'], mask, rec=True)
wm.add_watch(config.site_info['PAGE_DIR'], mask, rec=True)
notifier.start()

app = Flask(__name__, static_url_path='/static')
babel = Babel(app)
api = DelogXAPI(config.site_info)

from DelogX import route

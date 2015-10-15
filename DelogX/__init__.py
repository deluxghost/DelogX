# -*- coding: utf-8 -*-
from DelogX import config
from DelogX.error import DelogXError
from DelogX.api import DelogXAPI
from DelogX.inotify import FileEventHandler

try:
    import pyinotify
except ImportError:
    raise DelogXError('Import pyinotify Failed')
try:
    from flask import Flask
except ImportError:
    raise DelogXError('Import Flask Failed')

wm = pyinotify.WatchManager()
mask = pyinotify.ALL_EVENTS
notifier = pyinotify.ThreadedNotifier(wm, FileEventHandler())
notifier.setDaemon(True)
wm.add_watch(config.site_info['POST_DIR'], mask, rec=True)
wm.add_watch(config.site_info['PAGE_DIR'], mask, rec=True)
notifier.start()

app = Flask(__name__)
api = DelogXAPI(config.site_info)

from DelogX import route
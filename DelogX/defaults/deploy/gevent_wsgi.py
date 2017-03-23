#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Run DelogX in Gevent.'''
from __future__ import unicode_literals

import os
import sys

from gevent.pywsgi import WSGIServer
from flask import Flask
from DelogX import DelogX

CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD)
os.chdir(CWD)

app = Flask(__name__)
delogx = DelogX(CWD, app)
host = delogx.default_conf('debug.host')
port = delogx.default_conf('debug.port')

http_server = WSGIServer((host, port), delogx.framework)
http_server.serve_forever()

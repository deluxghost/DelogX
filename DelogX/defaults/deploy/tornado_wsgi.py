#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Run DelogX in Tornado.'''
from __future__ import unicode_literals

import os
import sys

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import Flask
from DelogX import DelogX

CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD)
os.chdir(CWD)

app = Flask(__name__)
delogx = DelogX(CWD, app)
host = delogx.default_conf('debug.host')
port = delogx.default_conf('debug.port')

http_server = HTTPServer(WSGIContainer(delogx.framework))
http_server.listen(port, address=host)
IOLoop.instance().start()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Run DelogX in shell directly.

**Do not use this in production environment.**

Run `python debug.py` in your terminal, and open `http://127.0.0.1:8000`.
'''
from __future__ import unicode_literals

import os
import sys

from flask import Flask
from DelogX import DelogX

CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD)
os.chdir(CWD)

app = Flask(__name__)
delogx = DelogX(CWD, app)
debug_host = delogx.default_conf('debug.host')
debug_port = delogx.default_conf('debug.port')

delogx.framework.run(host=debug_host, port=debug_port)

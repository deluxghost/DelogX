#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Run DelogX in shell directly.

**Do not use this in production environment.**

Run `python debug.py` in your terminal, and open `http://127.0.0.1:8000`.
'''
from __future__ import unicode_literals

import os

from flask import Flask

from DelogX import DelogX

CWD = os.path.dirname(os.path.realpath(__file__))
os.chdir(CWD)

app = Flask(__name__)
delogx = DelogX(CWD, app)

delogx.framework.run(host="0.0.0.0", port=8000)

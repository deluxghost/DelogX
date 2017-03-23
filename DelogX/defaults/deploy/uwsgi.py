# -*- coding: utf-8 -*-
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

application = delogx.framework

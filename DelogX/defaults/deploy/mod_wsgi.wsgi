# -*- coding: utf-8 -*-
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD)
os.chdir(CWD)

ACTIVATE = [
    os.path.join(CWD, 'env/bin/activate_this.py'),
    os.path.join(CWD, 'venv/bin/activate_this.py')
]
for activate_this in ACTIVATE:
    if os.path.exists(activate_this):
        execfile(activate_this, dict(__file__=activate_this))
        break

from flask import Flask
from DelogX import DelogX
app = Flask(__name__)
delogx = DelogX(CWD, app)
application = delogx.framework

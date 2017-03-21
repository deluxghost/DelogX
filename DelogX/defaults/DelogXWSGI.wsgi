import os
import sys
from flask import Flask
CWD = os.path.dirname(os.path.realpath(__file__))
os.chdir(CWD)
ACTIVATE = [
    os.path.join(CWD, 'env/bin/activate_this.py'),
    os.path.join(CWD, 'venv/bin/activate_this.py')
]
for activate_this in ACTIVATE:
    if os.path.exists(activate_this):
        execfile(activate_this, dict(__file__=activate_this))
        break
sys.path.append(CWD)
from DelogX import DelogX
app = Flask(__name__)
delogx = DelogX(CWD, app)
application = app

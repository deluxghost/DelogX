activate_this = '/home/ghost/DelogX/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/ghost/DelogX')
from DelogX import app as application

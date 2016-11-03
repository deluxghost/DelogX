import sys, os
cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)
activate_this = os.path.join(cwd, 'env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, cwd)
from DelogX import app as application

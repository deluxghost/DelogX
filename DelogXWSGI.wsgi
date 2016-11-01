activate_this = '/path/to/your/blog/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/path/to/your/blog')
from DelogX import app as application

import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

import web
application = web.app
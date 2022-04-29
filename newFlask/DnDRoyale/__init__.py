"""
The flask application package.
"""

from distutils.log import debug
from flask import Flask
import os #temp debugging

breadcrumb = os.getcwd()
print("initializing __init__.py from " + str(breadcrumb))

app = Flask(__name__)
print("got to init, app created")
app.config["DEBUG"] = False #False for Production
import DnDRoyale.views



"""
The flask application package.
"""

from distutils.log import debug
from flask import Flask
import os #temp debugging

breadcrumb = os.listdir()
print("initializing __init__.py from " + str(breadcrumb))

app = Flask(__name__)
print("got to init, app created")
app.config["DEBUG"] = True
import DnDRoyale.views
#print("just finished importing views.py") #for debugging



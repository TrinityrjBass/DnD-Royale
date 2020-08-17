"""
The flask application package.
"""

from flask import Flask
import os #temp debugging

breadcrumb = os.listdir()
print("initializing init.py from " + str(breadcrumb))

app = Flask(__name__)
print("got to init, app created")

#import DnDRoyale.views
#print("just finished importing views.py") #for debugging



"""
The flask application package.

this file was formerly called "__init__.py"
"""
import os

from flask import Flask


app = Flask(__name__)
print("got to init, app created")

import DnDRoyale.views
print("just finished importing views.py") #for debugging
if __name__ == '__main__':
    app.run(debug=True)


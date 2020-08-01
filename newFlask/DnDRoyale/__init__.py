"""
The flask application package.

this file was formerly called "__init__.py"
"""
import os

from flask import Flask


app = Flask(__name__)

import DnDRoyale.views



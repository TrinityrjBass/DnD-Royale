from flask import Flask
from . import app
import os


breadcrumb = os.listdir()
print("running run.py from : " + str(breadcrumb))
if __name__ == '__main__':
    app.run(debug=True)

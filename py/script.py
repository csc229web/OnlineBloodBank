# Python 3 Flask
# Online Blood Bank
# Lynn & Joshua
# V1.0.0

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
from flask import Flask, request, session, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from . import app

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

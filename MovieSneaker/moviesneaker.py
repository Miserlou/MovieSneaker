from flask import Flask, request, session, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('moviesneaker.cfg')
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
